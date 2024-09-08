from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from Proyecto.BasedeDatos import conectarbd

app = FastAPI()


#templates = Jinja2Templates(directory="templates")


#app.mount("/static", StaticFiles(directory="Proyecto/static"), name="static")




########################################################################################
################################# Libros ###############################################
########################################################################################

#Peticiones/formato
class Libro(BaseModel):
    action: str
    id: int = None
    nombre: str = None
    disponibilidad: bool = None
@app.get("/api/libros", response_class=PlainTextResponse)
async def get_libros():
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")
        mycursor.execute("SELECT id, nombre, disponibilidad FROM libros")
        libros = mycursor.fetchall()

        # Le da un formato de lista a la columna
        libros_list = [
            f"ID: {libro[0]}, Nombre: {libro[1]}, Disponibilidad: {'Sí' if libro[2] else 'No'}"
            for libro in libros
        ]

        # une las columnas y les da formato
        libros_text = "\n".join(libros_list)
        return libros_text

    except Exception as e:
        print(f"Exception: {e}")
        return PlainTextResponse("No se pudo cargar, compruebe la conexión", status_code=400)

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
                # Insertar un nuevo libro y capturar la ID generada
                mycursor.execute(
                    "INSERT INTO libros (nombre, disponibilidad) VALUES (%s, %s)",
                    (libro.nombre, libro.disponibilidad)
                )
                new_id = mycursor.lastrowid  # Captura la nueva ID

        mydb.commit()
        mycursor.close()
        mydb.close()

        # Retorna la ID en caso de inserción de un nuevo libro
        if libro.action == "add_modify" and not libro.id:
            return PlainTextResponse(f"Éxito, el libro insertado ahora tiene la siguiente ID: {new_id}", status_code=200)

        return PlainTextResponse("Éxito", status_code=200)

    except Exception as e:
        return PlainTextResponse(f"Error: {str(e)}", status_code=500)



@app.delete("/libros/{libro_id}", response_class=PlainTextResponse)
async def delete_libro(libro_id: int):
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")

        # Ejecuta la eliminación del libro por ID
        mycursor.execute("DELETE FROM libros WHERE id = %s", (libro_id,))

        # Verifica si se eliminó algún registro
        if mycursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Libro no encontrado")

        mydb.commit()
        return PlainTextResponse("Libro eliminado con éxito", status_code=200)

    except HTTPException as e:
        return PlainTextResponse(e.detail, status_code=e.status_code)

    except Exception as e:
        return PlainTextResponse(f"Error: {str(e)}", status_code=500)


#Buscar
@app.get("/libros/{libro_id}", response_class=PlainTextResponse)
async def get_libro_by_id(libro_id: int):
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")

        # Consulta para obtener el libro por ID
        mycursor.execute("SELECT id, nombre, disponibilidad FROM libros WHERE id = %s", (libro_id,))
        libro = mycursor.fetchone()

        # Verifica si se encontró el libro
        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado")

        # Formatea la información del libro
        libro_info = f"ID: {libro[0]}, Nombre: {libro[1]}, Disponibilidad: {'Sí' if libro[2] else 'No'}"
        return PlainTextResponse(libro_info, status_code=200)

    except HTTPException as e:
        return PlainTextResponse(e.detail, status_code=e.status_code)

    except Exception as e:
        return PlainTextResponse(f"Error: {str(e)}", status_code=500)

    finally:
        if mycursor is not None:
            mycursor.close()
        if mydb is not None:
            mydb.close()


########################################################################################
################################# Empleados #############################################
########################################################################################

class EmpleadoRequest(BaseModel):
    action: str
    id: int = None
    apellido_nombre: str = None
    direccion: str = None
    telefono: str = None
    Dias: str = None
    Horarios: str = None


@app.get("/api/empleados", response_class=PlainTextResponse)
async def get_empleados():
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")
        mycursor.execute("SELECT id, apellido_nombre, direccion, Telefono, Dias, Horarios FROM empleados")
        empleados = mycursor.fetchall()

        empleados_list = [
            f"id: {empleado[0]}, apellido_nombre: {empleado[1]},direccion: {empleado[2]}, Telefono: {empleado[3]},Dias: {empleado[4]}, Horarios: {empleado[5]}, "
            for empleado in empleados
        ]

        emp_text = "\n".join(empleados_list)
        return emp_text

    except Exception as e:
        print(f"Exception: {e}")
        return PlainTextResponse("No se pudo cargar, compruebe la conexión", status_code=400)

    finally:
        if mycursor is not None:
            mycursor.close()
        if mydb is not None:
            mydb.close()



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

        mydb.commit()
        return PlainTextResponse(message, status_code=200)

    except Exception as e:
        print(f"Exception: {e}")
        return PlainTextResponse(f"Error: {str(e)}", status_code=500)


    finally:
        mycursor.close()
        mydb.close()


@app.delete("/empleados/{empleado_id}", response_class=PlainTextResponse)
async def deleteemp(empleado_id: int):
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")

        # Ejecuta la eliminación del empleado por ID
        mycursor.execute("DELETE FROM empleados WHERE id = %s", (empleado_id,))

        # Verifica si se eliminó algún registro
        if mycursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")

        mydb.commit()
        return PlainTextResponse("Empleado eliminado con éxito", status_code=200)

    except HTTPException as e:
        return PlainTextResponse(e.detail, status_code=e.status_code)

    except Exception as e:
        return PlainTextResponse(f"Error: {str(e)}", status_code=500)


@app.get("/empleados/{empleado_id}", response_class=PlainTextResponse)
async def get_empleado_by_id(empleado_id: int):
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")

        # Consulta para obtener el empleado por ID
        mycursor.execute("SELECT id, apellido_nombre, direccion, telefono, Dias, Horarios FROM empleados WHERE id = %s", (empleado_id,))
        empleado = mycursor.fetchone()

        # Verifica si se encontró el empleado
        if not empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")

        # Formatea la información del empleado
        empleado_info = (
            f"ID: {empleado[0]}, Apellido_Nombre: {empleado[1]}, Direccion: {empleado[2]}, "
            f"Telefono: {empleado[3]}, Dias: {empleado[4]}, Horarios: {empleado[5]}"
        )
        return PlainTextResponse(empleado_info, status_code=200)

    except HTTPException as e:
        return PlainTextResponse(e.detail, status_code=e.status_code)

    except Exception as e:
        return PlainTextResponse(f"Error: {str(e)}", status_code=500)

    finally:
        mycursor.close()
        mydb.close()

########################################################################################
################################# Miembros #############################################
########################################################################################
@app.get("/api/miembros", response_class=PlainTextResponse)
async def get_miembros():
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")
        mycursor.execute("SELECT id, apellido_nombre, direccion, telefono FROM Miembros")
        Miembros = mycursor.fetchall()

        miembros_list = [
            f"id: {miembro[0]}, apellido_nombre: {miembro[1]},direccion: {miembro[2]}, Telefono: {miembro[3]} "
            for miembro in Miembros
        ]

        miem_text = "\n".join(miembros_list)
        return miem_text

    except Exception as e:
        print(f"Exception: {e}")
        return PlainTextResponse("No se pudo cargar, compruebe la conexión", status_code=400)

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
            message = "Miembro añadido/modificado con éxito"

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


@app.delete("/miembros/{miembro_id}", response_class=PlainTextResponse)
async def deleteemp(miembro_id: int):
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")

        # Ejecuta la eliminación del miembro por ID
        mycursor.execute("DELETE FROM miembros WHERE id = %s", (miembro_id,))

        # Verifica si se eliminó algún registro
        if mycursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Miembro no encontrado")

        mydb.commit()
        return PlainTextResponse("Miembro eliminado con éxito", status_code=200)

    except HTTPException as e:
        return PlainTextResponse(e.detail, status_code=e.status_code)

    except Exception as e:
        return PlainTextResponse(f"Error: {str(e)}", status_code=500)


@app.get("/miembros/{miembro_id}", response_class=PlainTextResponse)
async def get_miembro_by_id(miembro_id: int):
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")

        mycursor.execute("SELECT id, apellido_nombre, direccion, telefono FROM miembros WHERE id = %s", (miembro_id,))
        miembro = mycursor.fetchone()

        if not miembro:
            raise HTTPException(status_code=404, detail="Miembro no encontrado")


        miembro_info = (
            f"id: {miembro[0]}, apellido_Nombre: {miembro[1]}, direccion: {miembro[2]}, telefono: {miembro[3]}"
        )
        return PlainTextResponse(miembro_info, status_code=200)

    except HTTPException as e:
        return PlainTextResponse(e.detail, status_code=e.status_code)

    except Exception as e:
        return PlainTextResponse(f"Error: {str(e)}", status_code=500)

    finally:
        mycursor.close()
        mydb.close()

########################################################################################
################################# Rentas ###############################################
########################################################################################
@app.get("/api/rentas", response_class=PlainTextResponse)
async def get_rentas():
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")
        mycursor.execute("SELECT id, fechainicio, fechadevolucion, id_cliente, id_libro FROM Rentas")
        Rentas = mycursor.fetchall()

        rentas_list = [
            f"id: {renta[0]}, fechainicio: {renta[1]},fechadevolucion: {renta[2]}, id_cliente: {renta[3]},id_libro: {renta[4]}"
            for renta in Rentas
        ]

        ren_text = "\n".join(rentas_list)
        return ren_text

    except Exception as e:
        print(f"Exception: {e}")
        return PlainTextResponse("No se pudo cargar, compruebe la conexión", status_code=400)

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
                message = "Renta añadido/modificado con éxito"

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



@app.delete("/rentas/{renta_id}", response_class=PlainTextResponse)
async def deleteemp(renta_id: int):
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")


        mycursor.execute("DELETE FROM rentas WHERE id = %s", (renta_id,))


        if mycursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="renta no encontrada")

        mydb.commit()
        return PlainTextResponse("renta eliminada con éxito", status_code=200)

    except HTTPException as e:
        return PlainTextResponse(e.detail, status_code=e.status_code)

    except Exception as e:
        return PlainTextResponse(f"Error: {str(e)}", status_code=500)


@app.get("/rentas/{renta_id}", response_class=PlainTextResponse)
async def get_renta_by_id(renta_id: int):
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")

        mycursor.execute("SELECT id, fechainicio, fechadevolucion, id_cliente, id_libro FROM rentas WHERE id = %s", (renta_id,))
        renta = mycursor.fetchone()

        if not renta:
            raise HTTPException(status_code=404, detail="renta no encontrada")


        renta_info = (
            f"id: {renta[0]}, fechainicio: {renta[1]}, fechadevolucion: {renta[2]}, id_cliente: {renta[3]}, id_libro: {renta[4]}"
        )
        return PlainTextResponse(renta_info, status_code=200)

    except HTTPException as e:
        return PlainTextResponse(e.detail, status_code=e.status_code)

    except Exception as e:
        return PlainTextResponse(f"Error: {str(e)}", status_code=500)

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


