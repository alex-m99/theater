from django.shortcuts import render
from django.db import connection

# Create your views here.

def get_actors(request):
    with connection.cursor() as cursor:
        # cursor.execute("""SELECT 
        #                     A.Nume, 
        #                     A.Prenume, 
        #                     STUFF((
        #                         SELECT ', ' + AR.Rol
        #                         FROM AngajatiActori AA
        #                         INNER JOIN ActoriReprezentatii AR ON AA.AngajatiActoriID = AR.AngajatiActoriID
        #                         WHERE A.AngajatID = AA.AngajatID
        #                         FOR XML PATH(''), TYPE
        #                     ).value('.', 'NVARCHAR(MAX)'), 1, 2, '') AS CombinedRoles
        #                   FROM Angajati A; """)

        cursor.execute("""SELECT 
                          A.Nume, 
                          A.Prenume, 
                          STUFF((
                          SELECT ', ' + AR.Rol
                          FROM AngajatiActori AA
                          INNER JOIN ActoriReprezentatii AR ON AA.AngajatiActoriID = AR.AngajatiActoriID
                          WHERE A.AngajatID = AA.AngajatID
                          FOR XML PATH(''), TYPE
                          ).value('.', 'NVARCHAR(MAX)'), 1, 2, '') AS CombinedRoles,
                          AA.StudiiDomeniu
                         FROM Angajati A
                         INNER JOIN AngajatiActori AA ON A.AngajatID = AA.AngajatID; """)
        actori = cursor.fetchall()
        actori_dicts = [{'Nume': actor[0], 'Prenume': actor[1], 'Rol': actor[2], 'Studii': actor[3]} for actor in actori]
        photos = {
           "Ionescu": "ionescu-maria.jpg", 
           "Florescu": "florescu-adrian.jpg", 
           "Radulescu": "radulescu-daniel.jpg"
            }
        return render(request, "theater/actori.html", {
            "actori": actori_dicts,
            "photos": photos
        })
    
def actor_detail(request, name):
    with connection.cursor() as cursor:
        cursor.execute("""SELECT A.Nume,
                                 A.Prenume
                           FROM Angajati A
                           INNER JOIN AngajatiActori AA
                           ON A.AngajatID = AA.AngajatID
                       """)
        actori = cursor.fetchall()
        actori_dicts = [{'Nume': actor[0], 'Prenume': actor[1]} for actor in actori]
        identified_actor = next(actor for actor in actori_dicts if actor['Nume'] == name)
        return render(request, "theater/actor_details.html", {
            "actor": identified_actor
        })