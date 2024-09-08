from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse, JSONResponse
from Proyecto.BasedeDatos import conectarbd


router = APIRouter()

#Peticiones/formato
class Libro(BaseModel):
    action: str
    id: int = None
    nombre: str = None
    disponibilidad: bool = None
@router.get("/api/libros", response_class=PlainTextResponse)
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

@router.post("/libros")
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



@router.delete("/libros/{libro_id}", response_class=PlainTextResponse)
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
@router.get("/libros/{libro_id}", response_class=PlainTextResponse)
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
