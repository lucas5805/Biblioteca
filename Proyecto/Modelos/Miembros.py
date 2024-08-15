from ..BasedeDatos import conectarbd


class Miembros:
    def __init__(self, apellido_nombre, direccion, telefono):
        self.apellido_nombre = apellido_nombre
        self.direccion = direccion
        self.telefono = telefono

    def insert(self):
        mydb = conectarbd()
        mycursor = mydb.cursor()
        sql = "INSERT INTO miembros (apellido_nombre, direccion, telefono) VALUES (%s, %s, %s)"
        val = (self.apellido_nombre, self.direccion, self.telefono)
        mycursor.execute(sql, val)
        mydb.commit()
        print("Miembro insertado.")
        mycursor.close()
        mydb.close()
