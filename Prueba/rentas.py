from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse, JSONResponse
from Proyecto.BasedeDatos import conectarbd



router = APIRouter()



@router.get("/api/rentas", response_class=PlainTextResponse)
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

@router.post("/rentas")
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



@router.delete("/rentas/{renta_id}", response_class=PlainTextResponse)
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


@router.get("/rentas/{renta_id}", response_class=PlainTextResponse)
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
