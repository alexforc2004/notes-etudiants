# Exigences de sécurité de l'application des notes

| # | Exigence : « Le système doit… » | Vérification | Étape du SDLC | Test |
|---|---|---|---|---|
| 1 | résister aux injections SQL lors de la recherche d'un étudiant. | Une recherche malveillante ne doit pas retourner toutes les notes. | Développement et tests | S1 |
| 2 | refuser toute modification de note sans authentification valide. | L'API doit retourner HTTP 401. | Développement et tests | S2 |
| 3 | empêcher un étudiant de modifier une note. | L'API doit retourner HTTP 403. | Développement et tests | S3 |
| 4 | empêcher un enseignant de modifier une note appartenant à un autre module. | L'API doit retourner HTTP 403. | Développement et tests | S4 |
| 5 | refuser les notes hors de l'intervalle 0 à 20 et les valeurs invalides. | L'API doit retourner HTTP 400. | Développement et tests | S5 |
| 6 | autoriser un enseignant à modifier une note uniquement dans son module. | L'API doit retourner HTTP 200 et la note doit être mise à jour. | Développement et tests | S6 |
| 7 | ne pas exposer de détails techniques sensibles en cas d'erreur. | La réponse d'erreur ne doit pas révéler de détails internes de la base de données. | Tests de sécurité | S7 |
