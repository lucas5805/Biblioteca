from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from Proyecto.BasedeDatos import conectarbd
from Proyecto.Modelos.Libros import Libros
from Proyecto.Modelos.Empleados import Empleados
from Proyecto.Modelos.Miembros import Miembros
from Proyecto.Modelos.Rentas import Rentas

app = FastAPI()


#templates = Jinja2Templates(directory="templates")


app.mount("/static", StaticFiles(directory="Proyecto/static"), name="static")

#Peticiones/formato
class Libro(BaseModel):
    action: str
    id: int = None
    nombre: str = None
    disponibilidad: bool = None


#Formulario de Libros
from fastapi.responses import JSONResponse

@app.get("/api/libros", response_class=JSONResponse)
async def get_libros():
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")
        mycursor.execute("SELECT id, nombre, disponibilidad FROM libros")
        libros = mycursor.fetchall()

        libros_list = [{"id": libro[0], "nombre": libro[1], "disponibilidad": libro[2]} for libro in libros]
        return {"libros": libros_list}

    except Exception as e:
        print(f"Exception: {e}")
        return JSONResponse(content={"error": "No se pudo cargar, compruebe la conexión"}, status_code=400)

    finally:
        if mycursor is not None:
            mycursor.close()
        if mydb is not None:
            mydb.close()


@app.post("/libros")
async def manage_libros(libro: Libro):
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")

        if libro.action == "add_modify":
            if libro.id:
                mycursor.execute(
                    "UPDATE libros SET nombre = %s, disponibilidad = %s WHERE id = %s",
                    (libro.nombre, libro.disponibilidad, libro.id)
                )
            else:
                nuevo_libro = Libros(libro.nombre, libro.disponibilidad)
                nuevo_libro.insert()
        elif libro.action == "delete":
            print(f"Borrando: {libro.id}")  # Debugging line
            mycursor.execute("DELETE FROM libros WHERE id = %s", (libro.id,))

        mydb.commit()
        mycursor.close()
        mydb.close()
        return JSONResponse(content={"message": "Exito"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


# Formulario De Empleados
@app.get("/api/empleados", response_class=JSONResponse)
async def get_empleados():
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")
        mycursor.execute("SELECT id, apellido_nombre, direccion, Telefono, Dias, Horarios FROM empleados")
        Empleados = mycursor.fetchall()

        empleados_list = [
            {"id": Empleado[0], "apellido_nombre": Empleado[1], "direccion": Empleado[2], "Telefono": Empleado[3], "Dias": Empleado[4], "Horarios": Empleado[5]}
            for Empleado in Empleados
        ]

        return {"Empleados": empleados_list}

    except Exception as e:
        print(f"Exception: {e}")
        return JSONResponse(content={"error": "No se pudo cargar, compruebe la conexión"}, status_code=400)

    finally:
        if mycursor is not None:
            mycursor.close()
        if mydb is not None:
            mydb.close()


class EmpleadoRequest(BaseModel):
    action: str
    id: int = None
    apellido_nombre: str = None
    direccion: str = None
    telefono: str = None
    Dias: str = None
    Horarios: str = None

@app.post("/empleados")
async def manage_Empleados(request: EmpleadoRequest):
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")

        if request.action == "add_modify":
            if request.id:
                mycursor.execute(
                    "UPDATE empleados SET apellido_nombre = %s, direccion = %s, telefono = %s, Dias = %s, horarios = %s WHERE id = %s",
                    (request.apellido_nombre, request.direccion, request.telefono, request.Dias, request.Horarios, request.id)
                )
                message = "Empleado actualizado con éxito"
            else:
                mycursor.execute(
                    "INSERT INTO empleados (apellido_nombre, direccion, telefono, Dias, Horarios) VALUES (%s, %s, %s, %s, %s)",
                    (request.apellido_nombre, request.direccion, request.telefono, request.Dias, request.Horarios)
                )
                message = "Empleado añadido con éxito"

        elif request.action == "delete":
            if not request.id:
                return JSONResponse(content={"error": "ID es requerido para borrar"}, status_code=400)

            mycursor.execute("DELETE FROM empleados WHERE id = %s", (request.id,))
            message = "Empleado eliminado con éxito"

        mydb.commit()
        return JSONResponse(content={"message": message}, status_code=200)

    except Exception as e:
        print(f"Exception: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

    finally:
        mycursor.close()
        mydb.close()


# Formulario De Miembros
@app.get("/api/miembros", response_class=JSONResponse)
async def get_miembros():
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")
        mycursor.execute("SELECT id, apellido_nombre, direccion, telefono FROM Miembros")
        Miembros = mycursor.fetchall()


        Miembros_list = [
            {"id": Miembro[0], "apellido_nombre": Miembro[1], "direccion": Miembro[2], "telefono": Miembro[3]}
            for Miembro in Miembros
        ]

        return {"Miembros": Miembros_list}

    except Exception as e:
        print(f"Exception: {e}")
        return JSONResponse(content={"error": "No se pudo cargar, compruebe la conexion"}, status_code=400)

    finally:
        if mycursor is not None:
            mycursor.close()
        if mydb is not None:
            mydb.close()

#Peticion/formato
class MiembroRequest(BaseModel):
    action: str
    id: int = None
    apellido_nombre: str = None
    direccion: str = None
    telefono: str = None

@app.post("/miembros")
async def manage_Miembros(request: MiembroRequest):
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")

        if request.action == "add_modify":
            if request.id:
                mycursor.execute(
                    "UPDATE Miembros SET apellido_nombre = %s, direccion = %s, telefono = %s WHERE id = %s",
                    (request.apellido_nombre, request.direccion, request.telefono, request.id)
                )
            else:
                mycursor.execute(
                    "INSERT INTO Miembros (apellido_nombre, direccion, telefono) VALUES (%s, %s, %s)",
                    (request.apellido_nombre, request.direccion, request.telefono)
                )
            message = "Miembro añadido con éxito"

        elif request.action == "delete":
            if not request.id:
                return JSONResponse(content={"error": "ID es requerido para borrar"}, status_code=400)

            mycursor.execute("DELETE FROM Miembros WHERE id = %s", (request.id,))
            message = "Miembro eliminado con éxito"

        mydb.commit()
        return JSONResponse(content={"message": message}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    finally:
        mycursor.close()
        mydb.close()




# Formulario De Rentas
@app.get("/api/rentas", response_class=JSONResponse)
async def get_rentas():
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")
        mycursor.execute("SELECT id, fechainicio, fechadevolucion, id_cliente, id_libro FROM Rentas")
        Rentas = mycursor.fetchall()

        Rentas_list = [
            {"id": Renta[0], "fechainicio": Renta[1], "fechadevolucion": Renta[2], "id_cliente": Renta[3],  "id_libro": Renta[4]}
            for Renta in Rentas
        ]

        return {"Rentas": Rentas_list}

    except Exception as e:
        print(f"Exception: {e}")  # Print the exception details
        return JSONResponse(content={"error": "No se pudo cargar, compruebe la conexion"}, status_code=400)

    finally:
        if mycursor is not None:
            mycursor.close()
        if mydb is not None:
            mydb.close()


#Peticion/formato
class RentaRequest(BaseModel):
    action: str
    id: int = None
    fechainicio: str = None
    fechadevolucion: str = None
    id_cliente: int = None
    id_libro: int = None

@app.post("/rentas")
async def manage_Rentas(request: RentaRequest):
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")

        if request.action == "add_modify":
            if request.id:
                mycursor.execute(
                    "UPDATE Rentas SET fechainicio = %s, fechadevolucion = %s, id_cliente = %s, id_libro = %s WHERE id = %s",
                    (request.fechainicio, request.fechadevolucion, request.id_cliente, request.id_libro, request.id)
                )
                message = "Renta actualizada con éxito"
            else:
                mycursor.execute(
                    "INSERT INTO Rentas (fechainicio, fechadevolucion, id_cliente, id_libro) VALUES (%s, %s, %s, %s)",
                    (request.fechainicio, request.fechadevolucion, request.id_cliente, request.id_libro)
                )
                message = "Renta añadida con éxito"

        elif request.action == "delete":
            if not request.id:
                return JSONResponse(content={"error": "ID es requerido para borrar"}, status_code=400)

            mycursor.execute("DELETE FROM Rentas WHERE id = %s", (request.id,))
            message = "Renta eliminada con éxito"

        mydb.commit()
        return JSONResponse(content={"message": message}, status_code=200)

    except Exception as e:
        print(f"Exception: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

    finally:
        mycursor.close()
        mydb.close()


def init_db():
    mydb = conectarbd()
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS Biblioteca")
    mycursor.execute("USE Biblioteca")
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS libros (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255),
            disponibilidad BOOLEAN
        )
    """)

    # Crear tabla de Empleados
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS empleados (
            id INT AUTO_INCREMENT PRIMARY KEY,
            apellido_nombre VARCHAR(255),
            direccion VARCHAR(255),
            telefono VARCHAR(20),
            Dias VARCHAR(50),
            Horarios VARCHAR(20)
        )
    """)

    # Crear tabla de Miembros
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS miembros (
            id INT AUTO_INCREMENT PRIMARY KEY,
            apellido_nombre VARCHAR(255),
            direccion VARCHAR(255),
            telefono VARCHAR(20)
        )
    """)

    # Crear tabla de Rentas
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS rentas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fechainicio DATE,
            fechadevolucion DATE,
            id_cliente INT,
            id_libro INT,
            FOREIGN KEY (id_cliente) REFERENCES miembros(id),
            FOREIGN KEY (id_libro) REFERENCES libros(id)
        )
    """)

    mycursor.close()
    mydb.close()


