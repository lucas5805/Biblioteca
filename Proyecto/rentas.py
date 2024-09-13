from fastapi import  APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse, JSONResponse
from Proyecto.BasedeDatos import conectarbd
import mysql.connector


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
class Renta(BaseModel):
    action: str
    id: int = None
    fechainicio: str = None
    fechadevolucion: str = None
    id_cliente: int = None
    id_libro: int = None


@router.post("/rentas")
async def manage_Rentas(renta: Renta):
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")

        if renta.action == "add_modify":
            if renta.id:
                mycursor.execute(
                    "UPDATE Rentas SET fechainicio = %s, fechadevolucion = %s, id_cliente = %s, id_libro = %s WHERE id = %s",
                    (renta.fechainicio, renta.fechadevolucion, renta.id_cliente, renta.id_libro, renta.id)
                )
                if mycursor.rowcount == 0:
                    return PlainTextResponse("Error: ID no encontrado para la modificación", status_code=404)

                mydb.commit()
                return PlainTextResponse("Renta actualizada con éxito", status_code=200)

            else:
                mycursor.execute(
                    "INSERT INTO Rentas (fechainicio, fechadevolucion, id_cliente, id_libro) VALUES (%s, %s, %s, %s)",
                    (renta.fechainicio, renta.fechadevolucion, renta.id_cliente, renta.id_libro)
                )
                new_id = mycursor.lastrowid
                mydb.commit()
                return PlainTextResponse(f"Éxito, la renta fue insertada y ahora su ID es: {new_id}", status_code=200)

        return PlainTextResponse("Acción no reconocida", status_code=400)

    except mysql.connector.Error as err:
        return PlainTextResponse(f"Error en la base de datos: {str(err)}", status_code=500)

    except Exception as e:
        return PlainTextResponse(f"Error: {str(e)}", status_code=500)

    finally:
        if mycursor:
            mycursor.close()
        if mydb:
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
