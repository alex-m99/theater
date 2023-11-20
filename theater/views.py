from django.shortcuts import render
from django.db import connection

# Create your views here.

def get_actors(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Angajati")
        angajati = cursor.fetchall()
        return render(request, "theater/index.html", {
            "angajati": angajati
        })
