from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse, JSONResponse
from Proyecto.BasedeDatos import conectarbd


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
class MiembroRequest(BaseModel):
    action: str
    id: int = None
    apellido_nombre: str = None
    direccion: str = None
    telefono: str = None

@router.post("/miembros")
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


@router.delete("/miembros/{miembro_id}", response_class=PlainTextResponse)
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
