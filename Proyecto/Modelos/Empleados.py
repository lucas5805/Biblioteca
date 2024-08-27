from ..BasedeDatos import conectarbd

class Empleados:
    def __init__(self,id, apellido_nombre, direccion, telefono, Dias, Horarios):
        self.apellido_nombte = apellido_nombre
        self.direccion = direccion
        self.telefono = telefono
        self.Dias = Dias
        self.Horarios = Horarios

    def insert(self):
        mydb = conectarbd()
        mycursor = mydb.cursor()
        sql = "INSERT INTO empleados (apellido_nombre, direccion, telefono, Dias, Horarios) VALUES (%s, %s, %s, %s, %s)"
        val = (self.apellido_nombre, self.direccion, self.telefono, self.Dias, self.Horarios)
        mycursor.execute(sql, val)
        mydb.commit()
        print("Empleado insertado.")
        mycursor.close()
        mydb.close()

