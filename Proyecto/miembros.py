from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse, JSONResponse
from Proyecto.BasedeDatos import conectarbd
import mysql.connector

router = APIRouter()



@router.get("/api/miembros", response_class=PlainTextResponse)
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
class Miembro(BaseModel):
    action: str
    id: int = None
    apellido_nombre: str = None
    direccion: str = None
    telefono: str = None

@router.post("/miembros")
async def manage_Miembros(miembro: Miembro):
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")

        if miembro.action == "add_modify":
            if miembro.id:
                mycursor.execute(
                    "UPDATE Miembros SET apellido_nombre = %s, direccion = %s, telefono = %s WHERE id = %s",
                    (miembro.apellido_nombre, miembro.direccion, miembro.telefono, miembro.id)
                )
                if mycursor.rowcount == 0:
                    mycursor.close()
                    mydb.close()
                    return PlainTextResponse("Error: ID no encontrado para la modificación", status_code=404)
                mydb.commit()
                mycursor.close()
                mydb.close()
            else:
                mycursor.execute(
                    "INSERT INTO Miembros (apellido_nombre, direccion, telefono) VALUES (%s, %s, %s)",
                    (miembro.apellido_nombre, miembro.direccion, miembro.telefono)
                )
                new_id = mycursor.lastrowid
                mydb.commit()
                mycursor.close()
                mydb.close()
        if miembro.action == "add_modify" and not miembro.id:
            return PlainTextResponse(f"Éxito, el miembro insertado ahora tiene la siguiente ID: {new_id}", status_code=200)


        return PlainTextResponse("Éxito", status_code=200)

    except Exception as e:
        return PlainTextResponse(f"Error: {str(e)}", status_code=500)




@router.delete("/miembros/{miembro_id}", response_class=PlainTextResponse)
async def deletemiem(miembro_id: int):
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
    except mysql.connector.Error as err:
        if err.errno == 1451: #es para hacer referencia al error en mysql cuando no se respeta una foreign key
            return PlainTextResponse("Error: No se puede eliminar el miembro porque está asociado con registros en otras tablas (por ejemplo, rentas).",status_code=400)#este es el codigo mostrado

    except HTTPException as e:
        return PlainTextResponse(e.detail, status_code=e.status_code)

    except Exception as e:
        return PlainTextResponse(f"Error: {str(e)}", status_code=500)


@router.get("/miembros/{miembro_id}", response_class=PlainTextResponse)
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
