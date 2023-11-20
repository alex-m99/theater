from django.shortcuts import render
from django.db import connection

# Create your views here.

def get_actors(request):
    with connection.cursor() as cursor:
        cursor.execute("""SELECT A.Nume,
                                 A.Prenume
                           FROM Angajati A
                           INNER JOIN AngajatiActori AA
                           ON A.AngajatID = AA.AngajatID""")
        actori = cursor.fetchall()
        return render(request, "theater/actori.html", {
            "actori": actori
        })
