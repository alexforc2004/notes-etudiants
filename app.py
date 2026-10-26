
# =================================================================
# Application de consultation des notes des étudiants
# =================================================================

import os
import math
import sqlite3
import auth

from flask import Flask, jsonify, request

app = Flask(__name__)
DB = "notes.db"


def init_db():
    with sqlite3.connect(DB) as con:
        con.execute(
            "CREATE TABLE IF NOT EXISTS notes "
            "(id INTEGER PRIMARY KEY, etudiant TEXT, module TEXT, note REAL)"
        )

        if con.execute("SELECT COUNT(*) FROM notes").fetchone()[0] == 0:
            con.execute(
                "INSERT INTO notes (etudiant, module, note) VALUES (?, ?, ?)",
                ("Amina", "DevSecOps", 15.5),
            )
            con.execute(
                "INSERT INTO notes (etudiant, module, note) VALUES (?, ?, ?)",
                ("Youssef", "DevSecOps", 12.0),
            )


init_db()


@app.route("/")
def accueil():
    return (
        "<!DOCTYPE html><html lang='fr'><head><meta charset='utf-8'>"
        "<title>Notes des etudiants</title></head><body>"
        "<h1>Consultation des notes</h1>"
        "<p><a href='/notes'>Voir les notes</a></p></body></html>"
    )


@app.route("/health")
def health():
    return jsonify(status="ok", version="1.0")


@app.route("/notes", methods=["GET"])
def lister_notes():
    etudiant = request.args.get("etudiant", "")

    try:
        with sqlite3.connect(DB) as con:
            rows = con.execute(
                "SELECT id, etudiant, module, note "
                "FROM notes WHERE etudiant LIKE ?",
                (f"%{etudiant}%",),
            ).fetchall()

        return jsonify([
            {
                "id": r[0],
                "etudiant": r[1],
                "module": r[2],
                "note": r[3],
            }
            for r in rows
        ])

    except sqlite3.Error:
        return jsonify(erreur="Erreur interne du serveur"), 500


@app.route("/notes/<int:note_id>", methods=["PUT"])
def modifier_note(note_id):
    # 1. Vérifier l'identification
    utilisateur = auth.utilisateur_connecte()

    if utilisateur is None:
        return jsonify(erreur="Authentification requise"), 401

    # 2. Vérifier le rôle
    if utilisateur.get("role") != "enseignant":
        return jsonify(erreur="Accès interdit"), 403

    # 3. Vérifier la validité de la note
    donnees = request.get_json(silent=True)

    if not isinstance(donnees, dict) or "note" not in donnees:
        return jsonify(erreur="Note invalide"), 400

    note = donnees["note"]

    if (
        isinstance(note, bool)
        or not isinstance(note, (int, float))
        or not math.isfinite(note)
        or not 0 <= note <= 20
    ):
        return jsonify(
            erreur="La note doit être un nombre entre 0 et 20"
        ), 400

    # 4. Vérifier le module et modifier la note
    try:
        with sqlite3.connect(DB) as con:
            ligne = con.execute(
                "SELECT module FROM notes WHERE id = ?",
                (note_id,),
            ).fetchone()

            if ligne is None:
                return jsonify(erreur="Note introuvable"), 404

            if utilisateur.get("module") != ligne[0]:
                return jsonify(
                    erreur="Accès interdit à ce module"
                ), 403

            con.execute(
                "UPDATE notes SET note = ? WHERE id = ?",
                (note, note_id),
            )

        return jsonify(message="Note modifiée avec succès"), 200

    except sqlite3.Error:
        # Ne pas exposer les détails techniques
        return jsonify(erreur="Erreur interne du serveur"), 500


if __name__ == "__main__":
    app.run(
        host=os.environ.get("APP_HOST", "127.0.0.1"),
        port=5000,
    )
