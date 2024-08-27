from ..BasedeDatos import conectarbd


class Rentas:
    def __init__(self, fechainicio, fechadevolucion, id_cliente, id_libro):
        self.fechainicio = fechainicio
        self.fechadevolucion = fechadevolucion
        self.id_cliente = id_cliente
        self.id_libro = id_libro

    def insert(self):
        mydb = conectarbd()
        mycursor = mydb.cursor()
        sql = "INSERT INTO rentas (fechainicio, fechadevolucion, id_cliente, id_libro) VALUES (%s, %s, %s, %s)"
        val = (self.fechainicio, self.fechadevolucion, self.id_cliente, self.id_libro)
        mycursor.execute(sql, val)
        mydb.commit()
        print("Renta insertado.")
        mycursor.close()
        mydb.close()
