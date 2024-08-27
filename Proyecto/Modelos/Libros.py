from ..BasedeDatos import conectarbd

class Libros:
    def __init__(self, nombre, disponibilidad):
        self.nombre = nombre
        self.disponibilidad = disponibilidad

    def insert(self):
        mydb = conectarbd()
        mycursor = mydb.cursor()
        sql = "INSERT INTO libros (nombre, disponibilidad) VALUES (%s, %s)"
        val = (self.nombre, self.disponibilidad)
        mycursor.execute(sql, val)
        mydb.commit()
        print("Libro insertado.")
        mycursor.close()
        mydb.close()
