from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection, transaction
from django.urls import reverse
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
    if 'search_name' in request.GET:
        # Handle the search case
        actor_search = request.GET['search_name']
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
                                     ON A.AngajatID = AA.AngajatID
                                     WHERE A.Nume LIKE %s; """, ['%' + actor_search + '%'])
            actors = cursor.fetchall()
    else:
        # Default case without search
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
            
    actors_dicts =  [{ 'ID': actor[0], 'Nume':actor[1], 'Prenume': actor[2], 'CNP': actor[3], 'Telefon': actor[4], 'Email': actor[5], 'Studii': actor[6]} for actor in actors]
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
                              WHERE AngajatID = %s;""", [actor_name, actor_firstname, actor_CNP, actor_phone, actor_email, actor_id])

        with connection.cursor() as cursor:
            cursor.execute("""UPDATE AngajatiActori
                              SET StudiiDomeniu = %s
                              WHERE AngajatID = %s;""", [actor_education, actor_id])

        return redirect('/adauga-actori')  
    
    return render(request, 'actors.html')

def delete_actor(request):
    if request.method == 'POST':
        actor_id = request.POST.get('actor_id')


        with connection.cursor() as cursor:
            cursor.execute("""DELETE FROM AngajatiActori
                              WHERE AngajatID = %s;""", [actor_id])
        
        with connection.cursor() as cursor:
            cursor.execute("""DELETE FROM Angajati
                              WHERE AngajatID = %s;""", [actor_id])

        

        return redirect('/adauga-actori')  
    
    return render(request, 'actors.html')

def search_actor(request):
    if request.method == 'POST':
        actor_search = request.POST.get('search_name')
        return redirect(reverse('actors_tab') + '?search_name=' + actor_search)   
    
    return render(request, 'actors.html')


def shows_tab(request):
    #get supprort employees
    with connection.cursor() as cursor:
            cursor.execute("""SELECT A.AngajatID,
                              A.Nume + ' ' + A.Prenume AS NumeComplet,
                              Angs.Functie
                              FROM Angajati A
                              INNER JOIN AngajatiSuport AngS
                              ON A.AngajatID = AngS.AngajatID""")
            support = cursor.fetchall()
            
    support_dicts =  [{ 'ID':employee[0],'NumeComplet':employee[1], 'Functie':employee[2]} for employee in support]

    #get shows 
    with connection.cursor() as cursor:
        cursor.execute(""" SELECT 
                            R.ReprezentatieID,
                            R.PiesaID,
                            P.Nume AS PiesaNume,
                            P.Autor,
                            P.GenDramatic,
                            RAS.Regizor AS Regizor,
                            RAS.Scenograf AS Scenograf,
                            RAS.Producator AS Producator,
                            RAS.OperatorSunet AS OperatorSunet,
                            RAS.OperatorLumini AS OperatorLumini,
                            RAS.Costumier AS Costumier
                            FROM Reprezentatii R
                            JOIN Piese P ON R.PiesaID = P.PiesaID
                            LEFT JOIN(SELECT 
                                      RS.ReprezentatieID,
                                      MAX(CASE WHEN ASU.Functie = 'Regizor' THEN A.Nume END) AS Regizor,
                                      MAX(CASE WHEN ASU.Functie = 'Scenograf' THEN A.Nume END) AS Scenograf,
                                      MAX(CASE WHEN ASU.Functie = 'Producator' THEN A.Nume END) AS Producator,
                                      MAX(CASE WHEN ASU.Functie = 'Operator sunet' THEN A.Nume END) AS OperatorSunet,
                                      MAX(CASE WHEN ASU.Functie = 'Operator lumini' THEN A.Nume END) AS OperatorLumini,
                                      MAX(CASE WHEN ASU.Functie = 'Costumier' THEN A.Nume END) AS Costumier
                                      FROM AngajatiSuport ASU
                                      JOIN Angajati A ON ASU.AngajatID = A.AngajatID
                                      JOIN SuportReprezentatii RS ON ASU.AngajatiSuportID = RS.AngajatiSuportID
                                      GROUP BY RS.ReprezentatieID
                            ) RAS ON R.ReprezentatieID = RAS.ReprezentatieID;""")
        shows = cursor.fetchall()

            
    #get plays
    with connection.cursor() as cursor: 
        cursor.execute(""" SELECT P.PiesaID,
                                  P.Nume
                           FROM Piese P;
            """)
        plays = cursor.fetchall()

            
    shows_dicts =  [{ 'ReprezentatieID': show[0], 'PiesaID':show[1], 'Nume':show[2],'Autor':show[3], 'Gen':show[4], 'Regizor':show[5], 'Scenograf':show[6], 'Producator':show[7],'Sunet':show[8],'Lumini':show[9],'Costume':show[10]} for show in shows]
    plays_dicts = [{'ID':play[0], 'Nume': play[1]} for play in plays]

    return render(request, "shows.html", {
            "current_tab": "adauga-spectacole",
            "employees": support_dicts,
            "shows": shows_dicts,
            "plays": plays_dicts
        })


    return render(request, 'shows.html')


def save_show(request):
    if request.method == 'POST':
        # Extract data from the form
        play_name = request.POST.get('play_name')
        director_name = request.POST.get('director_name')
        scenographer_name = request.POST.get('scenographer_name')
        producer_name = request.POST.get('producer_name')
        sound_name = request.POST.get('sound_name')
        lights_name = request.POST.get('lights_name')
        costume_name = request.POST.get('costume_name')

        # Step 1: Get PiesaID for the given play_name
        with connection.cursor() as cursor:
            cursor.execute("SELECT PiesaID FROM Piese WHERE Nume = %s", [play_name])
            piesa_id = cursor.fetchone()
        if piesa_id:
            piesa_id = piesa_id[0]

        # Step 2: Get AngajatSuportID for each role
        support_id_list = []
        with connection.cursor() as cursor:
            roles = {"Regizor": director_name, 
                     "Scenograf": scenographer_name, 
                     "Producator": producer_name, 
                     "Operator sunet": sound_name, 
                     "Operator lumini": lights_name,  
                     "Costumier": costume_name}

            for role in roles:
                cursor.execute(
                        """SELECT ASU.AngajatiSuportID 
                        FROM AngajatiSuport ASU 
                        JOIN Angajati A ON ASU.AngajatID = A.AngajatID 
                        WHERE ASU.Functie = %s AND A.Nume = %s""",
                        [role, roles[role]]
                    )
                support_id = cursor.fetchone()
                if support_id:
                    support_id_list.append(support_id[0])

        # Step 3: Insert a new Reprezentatii record
        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO Reprezentatii (PiesaID)
                   OUTPUT INSERTED.ReprezentatieID
                   VALUES (%s)""",
                [piesa_id]
            )

            reprezentatie_id = cursor.fetchone()[0]

        # Step 4: Insert into SuportReprezentatii
        with connection.cursor() as cursor:
            for support in support_id_list:
                cursor.execute(
                    """INSERT INTO SuportReprezentatii (AngajatiSuportID, ReprezentatieID) 
                       VALUES (%s, %s)""",
                    [support, reprezentatie_id]
                )

        # Commit the transaction
        connection.commit()

        print(request.POST)

        return redirect('/adauga-spectacole')  

    return render(request, 'shows.html')

    