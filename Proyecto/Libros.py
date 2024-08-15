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


templates = Jinja2Templates(directory="templates")


app.mount("/static", StaticFiles(directory="Proyecto/static"), name="static")

class Libro(BaseModel):
    action: str
    id: int = None
    nombre: str = None
    disponibilidad: bool = None

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/libros", response_class=HTMLResponse)
async def read_libros(request: Request):
    return templates.TemplateResponse("libros.html", {"request": request})

@app.get("/rentas", response_class=HTMLResponse)
async def read_rentas(request: Request):
    return templates.TemplateResponse("rentas.html", {"request": request})

@app.get("/miembros", response_class=HTMLResponse)
async def read_miembros(request: Request):
    return templates.TemplateResponse("miembros.html", {"request": request})

@app.get("/empleados", response_class=HTMLResponse)
async def read_empleados(request: Request):
    return templates.TemplateResponse("empleados.html", {"request": request})

#Formulario de Libros
@app.get("/api/libros", response_class=JSONResponse)
async def get_libros():
    mydb = conectarbd()
    mycursor = mydb.cursor()
    mycursor.execute("USE Biblioteca")
    mycursor.execute("SELECT id, nombre, disponibilidad FROM libros")
    libros = mycursor.fetchall()
    mycursor.close()
    mydb.close()

    libros_list = [{"id": libro[0], "nombre": libro[1], "disponibilidad": libro[2]} for libro in libros]
    return {"libros": libros_list}

@app.post("/libros")
async def manage_libros(
        action: str = Form(...),
        id: int = Form(None),
        nombre: str = Form(None),
        disponibilidad: bool = Form(None)
):
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")

        if action == "add_modify":
            if id:
                mycursor.execute(
                    "UPDATE libros SET nombre = %s, disponibilidad = %s WHERE id = %s",
                    (nombre, disponibilidad, id)
                )
            else:
                nuevo_libro = Libros(nombre, disponibilidad)
                nuevo_libro.insert()
        elif action == "delete":
            print(f"Borrando: {id}")  # Debugging line
            mycursor.execute("DELETE FROM libros WHERE id = %s", (id,))

        mydb.commit()
        mycursor.close()
        mydb.close()
        return JSONResponse(content={"message": "Exito"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Formulario De Empleados
@app.get("/api/Empleados", response_class=JSONResponse)
async def get_empleados():
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")
        mycursor.execute("SELECT id, apellido_nombre, direccion, Telefono, Dias, Horarios FROM empleados")
        Empleados = mycursor.fetchall()

        empleados_list = [{"id": Empleado[0], "apellido_nombre": Empleado[1], "direccion": Empleado[2], "Telefono": Empleado[3], "Dias": Empleado[4], "Horarios": Empleado[5]} for Empleado in Empleados]

        return {"Empleados": empleados_list}

    finally:
        mycursor.close()
        mydb.close()

@app.post("/Empleados")
async def manage_Empleados(
        action: str = Form(...),
        id: int = Form(None),
        apellido_nombre: str = Form(None),
        direccion: str = Form(None),
        telefono: str = Form(None),
        dias: str = Form(None),
        horarios: str = Form(None),
):
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")

        if action == "add_modify":
            if id:
                mycursor.execute(
                    "UPDATE empleados SET apellido_nombre = %s, direccion = %s, telefono = %s, dias = %s, horarios = %s WHERE id = %s",
                    (apellido_nombre, direccion, telefono, dias, horarios, id)
                )
            else:

                mycursor.execute(
                    "INSERT INTO empleados (apellido_nombre, direccion, telefono, dias, horarios) VALUES (%s, %s, %s, %s, %s)",
                    (apellido_nombre, direccion, telefono, dias, horarios)
                )

        elif action == "delete":
            mycursor.execute("DELETE FROM empleados WHERE id = %s", (id,))

        mydb.commit()
        return JSONResponse(content={"message": "Exito"}, status_code=200)

    except Exception as e:
        print(f"Exception: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

    finally:
        mycursor.close()
        mydb.close()


# Formulario De Miembros
@app.get("/api/Miembros", response_class=JSONResponse)
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
        return JSONResponse(content={"error": "Ocurrio un error"}, status_code=500)

    finally:
        if mycursor is not None:
            mycursor.close()
        if mydb is not None:
            mydb.close()

@app.post("/Miembros")
async def manage_Miembros(
        action: str = Form(...),
        id: int = Form(None),
        apellido_nombre: str = Form(None),
        direccion: str = Form(None),
        telefono: str = Form(None),
):
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")

        if action == "add_modify":
            if id:
                mycursor.execute(
                    "UPDATE Miembros SET apellido_nombre = %s, direccion = %s,  Telefono = %s WHERE id = %s",
                    (apellido_nombre, direccion, telefono, id)
                )
            else:
                # Insert new employee
                mycursor.execute(
                    "INSERT INTO Miembros (apellido_nombre, direccion, telefono) VALUES (%s, %s, %s)",
                    (apellido_nombre, direccion, telefono)
                )

        elif action == "delete":
            mycursor.execute("DELETE FROM Miembros WHERE id = %s", (id,))

        mydb.commit()
        return JSONResponse(content={"message": "Exito"}, status_code=200)

    except Exception as e:
        print(f"Exception: {e}")  # Print the exception to the console
        return JSONResponse(content={"error": str(e)}, status_code=500)

    finally:
        mycursor.close()
        mydb.close()



# Formulario De Rentas
@app.get("/api/Rentas", response_class=JSONResponse)
async def get_rentas():
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")
        mycursor.execute("SELECT id, fecha_inicio, fecha_devolucion, id_cliente, id_libro FROM Rentas")
        Rentas = mycursor.fetchall()


        Rentas_list = [
            {"id": Renta[0], "fecha_inicio": Renta[1], "fecha_devolucion": Renta[2], "id_cliente": Renta[3],  "id_libro": Renta[4]}
            for Renta in Rentas
        ]

        return {"Rentas": Rentas_list}

    except Exception as e:
        print(f"Exception: {e}")  # Print the exception to the console
        return JSONResponse(content={"error": "Ocurrio un error"}, status_code=500)

    finally:
        if mycursor is not None:
            mycursor.close()
        if mydb is not None:
            mydb.close()

@app.post("/Rentas")
async def manage_Rentas(
        action: str = Form(...),
        id: int = Form(None),
        fecha_inicio: str = Form(None),
        fecha_devolucion: str = Form(None),
        id_cliente: int = Form(None),
        id_libro: int = Form(None),
):
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")

        if action == "add_modify":
            if id:
                mycursor.execute(
                    "UPDATE Rentas SET fecha_inicio = %s, fecha_devoulucion = %s,  id_cliente = %s,  id_libro = %s WHERE id = %s",
                    (fecha_inicio, fecha_devolucion, id_cliente, id_libro, id)
                )
            else:

                mycursor.execute(
                    "INSERT INTO Rentas (apellido_nombre, direccion, telefono) VALUES (%s, %s, %s, %s)",
                    (fecha_inicio, fecha_devolucion, id_cliente, id_libro)
                )

        elif action == "delete":
            mycursor.execute("DELETE FROM Rentas WHERE id = %s", (id,))

        mydb.commit()
        return JSONResponse(content={"message": "Exito"}, status_code=200)

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
    mycursor.close()
    mydb.close()


