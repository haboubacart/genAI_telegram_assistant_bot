def get_all_taches(client, database_id) : 
    list_all_taches = []
    taches = client.databases.query(database_id=database_id)['results']
    for tache in taches : 
        list_all_taches.append({
            "est_archivee" : tache["archived"],
            "nom_tache" : tache["properties"]["Nom de la tâche"]["title"][0]["text"]["content"],
            "statut" : tache["properties"]["Status"]["status"]["name"],
            "echeance" : tache["properties"]["Échéance"]["date"]
        })
    return (taches)

def create_new_tache(client, database_id, nom_tache):
    client.pages.create(
        **{
            "parent": {
                "database_id": database_id
            },
            'properties': {
                'Nom de la tâche': {'title': [{'text': {'content': nom_tache}}]}
            }
        }
    )
