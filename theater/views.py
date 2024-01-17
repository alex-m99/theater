from django.shortcuts import render
from django.db import connection
from .helper_functions import read_actor_description
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
                          AA.AngajatiActoriID,
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
        actori_dicts = [{ 'ID':actor[0], 'Nume': actor[1], 'Prenume': actor[2], 'Rol': actor[3], 'Studii': actor[4]} for actor in actori]
        photos = {
           "Ionescu": "ionescu-maria.jpg", 
           "Florescu": "florescu-adrian.jpg", 
           "Radulescu": "radulescu-daniel.jpg"
            }
        return render(request, "theater/actori.html", {
            "actori": actori_dicts
        })
    
def actor_detail(request, name):
    with connection.cursor() as cursor:
        cursor.execute("""SELECT AA.AngajatiActoriID,
                                 A.Nume,
                                 A.Prenume
                           FROM Angajati A
                           INNER JOIN AngajatiActori AA
                           ON A.AngajatID = AA.AngajatID
                       """)
        actori = cursor.fetchall()
        actori_dicts = [{ 'ID':actor[0],'Nume': actor[1], 'Prenume': actor[2]} for actor in actori]
        full_actor_name = name.split('-')
        
        identified_actor = next(actor for actor in actori_dicts if actor['Nume'] == full_actor_name[0].capitalize() and actor['Prenume']== full_actor_name[1].capitalize())
        print(full_actor_name[0] + full_actor_name[1])
        actor_description = read_actor_description(identified_actor['ID'])
        return render(request, "theater/actor_details.html", {
            "actor": identified_actor,
            "description": actor_description
        })
    
def get_spectacole(request, name):
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
                          AA.AngajatiActoriID,
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
        actori_dicts = [{ 'ID':actor[0], 'Nume': actor[1], 'Prenume': actor[2], 'Rol': actor[3], 'Studii': actor[4]} for actor in actori]
        photos = {
           "Ionescu": "ionescu-maria.jpg", 
           "Florescu": "florescu-adrian.jpg", 
           "Radulescu": "radulescu-daniel.jpg"
            }
        return render(request, "theater/actori.html", {
            "actori": actori_dicts
        })