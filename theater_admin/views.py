from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection, transaction
# Create your views here.


def home(request):
    return render(request, "home.html", {
        "current_tab": "home"
    })

def actors(request):
    return render(request, "actors.html", {
        "current_tab": "adauga-actori"
    })

def shopping(request):
    return HttpResponse("Welcome to shopping")

def save_student(request):
    student_name = request.POST["student_name"]
    return  render(request, "welcome.html", {
        "student_name": student_name
    })

def actors_tab(request):
    with connection.cursor() as cursor:
        cursor.execute("""SELECT A.AngajatID,
                                 A.Nume,
	                             A.Prenume,
	                             A.CNP,
	                             A.Telefon,
	                             A.Email,
	                             AA.StudiiDomeniu
                                 FROM Angajati A
                                 INNER JOIN AngajatiActori AA
                                 ON A.AngajatID = AA.AngajatID; """)
        actors = cursor.fetchall()
        actors_dicts =  [{  'ID': actor[0], 'Nume':actor[1], 'Prenume': actor[2], 'CNP': actor[3], 'Telefon': actor[4], 'Email': actor[5], 'Studii': actor[6]} for actor in actors]

        return render(request, "actors.html", {
            "current_tab": "adauga-actori",
            "actors": actors_dicts,
        })

def save_actor(request):
    if request.method == 'POST':
        # Extract data from the form
        actor_name = request.POST.get('actor_name')
        actor_firstname = request.POST.get('actor_firstname')
        actor_CNP = request.POST.get('actor_CNP')
        actor_phone = request.POST.get('actor_phone')
        actor_email = request.POST.get('actor_email')
        actor_education = request.POST.get('actor_education')

        # Perform the SQL INSERT statement
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute("""INSERT INTO Angajati (Nume, Prenume, CNP, Telefon, Email)
                                  OUTPUT INSERTED.AngajatID
                                  VALUES (%s, %s, %s, %s, %s); """, [actor_name, actor_firstname, actor_CNP, actor_phone, actor_email])
                last_angajat_id = cursor.fetchone()[0]

        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute("""INSERT INTO AngajatiActori (AngajatID, StudiiDomeniu)
                                  VALUES (%s, %s); """, [last_angajat_id, actor_education])

        return redirect('/adauga-actori')  

    return render(request, 'actors.html')

def update_actor(request):
    if request.method == 'POST':
        actor_id = request.POST.get('actor_id')
        actor_name = request.POST.get('actor_name')
        actor_firstname = request.POST.get('actor_firstname')
        actor_CNP = request.POST.get('actor_CNP')
        actor_phone = request.POST.get('actor_phone')
        actor_email = request.POST.get('actor_email')
        actor_education = request.POST.get('actor_education')
       
        with connection.cursor() as cursor:
            cursor.execute("""UPDATE Angajati
                              SET Nume = %s, Prenume = %s, CNP = %s, Telefon = %s, Email = %s
                              WHERE AngajatiID = %s;""", [actor_name, actor_firstname, actor_CNP, actor_phone, actor_email, actor_id])

        with connection.cursor() as cursor:
            cursor.execute("""UPDATE yourapp_angajatiactori
                              SET StudiiSuperioare = %s
                              WHERE AngajatiID = %s;""", [actor_education, actor_id])

        return redirect('/adauga-actori')  
    
    return render(request, 'actors.html')