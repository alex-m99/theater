from django.db import connection

with connection.cursor() as cursor:
        cursor.execute("""SELECT A.Nume,
                                 A.Prenume
                           FROM Angajati A
                           INNER JOIN AngajatiActori AA
                           ON A.AngajatID = AA.AngajatID""")
        actori = cursor.fetchall()
        print(actori)