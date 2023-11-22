from django.shortcuts import render
from django.db import connection

# Create your views here.

def get_actors(request):
    with connection.cursor() as cursor:
        cursor.execute("""SELECT A.Nume, A.Prenume, AR.Rol
                          FROM Angajati A
                          INNER JOIN AngajatiActori AA
                          ON A.AngajatID = AA.AngajatID
                          INNER JOIN ActoriReprezentatii AR
                          ON AA.AngajatiActoriID = AR.AngajatiActoriID;""")
        actori = cursor.fetchall()
        return render(request, "theater/actori.html", {
            "actori": actori
        })
    
def actor_detail(request, slug):
    with connection.cursor() as cursor:
        cursor.execute("""SELECT A.Nume,
                                 A.Prenume
                           FROM Angajati A
                           INNER JOIN AngajatiActori AA
                           ON A.AngajatID = AA.AngajatID
                           INNER JOIN ActoriReprezentanti AR
                           ON A.AngajatID = AR.AngajatID""")
        actori = cursor.fetchall()
        print(actori)
        return render(request, "theater/actori.html", {
            "actori": actori
        })