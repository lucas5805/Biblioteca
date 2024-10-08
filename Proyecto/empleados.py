from fastapi import  APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse, JSONResponse
from Proyecto.BasedeDatos import conectarbd
import mysql.connector

router = APIRouter()


class Empleado(BaseModel):
    action: str
    id: int = None
    apellido_nombre: str = None
    direccion: str = None
    telefono: str = None
    Dias: str = None
    Horarios: str = None


@router.get("/api/empleados", response_class=PlainTextResponse)
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



@router.post("/empleados")
async def manage_Empleados(empleado: Empleado):
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")

        if empleado.action == "add_modify":
            if empleado.id:
                mycursor.execute(
                    "UPDATE empleados SET apellido_nombre = %s, direccion = %s, telefono = %s, Dias = %s, horarios = %s WHERE id = %s",
                    (empleado.apellido_nombre, empleado.direccion, empleado.telefono, empleado.Dias, empleado.Horarios, empleado.id)
                )
                if mycursor.rowcount == 0:
                    mycursor.close()
                    mydb.close()
                    return PlainTextResponse("Error: ID no encontrado para la modificación", status_code=404)
                mydb.commit()
                mycursor.close()
                mydb.close()
                return PlainTextResponse("Empleado actualizado con éxito", status_code=200)


            else:
                mycursor.execute(
                    "INSERT INTO empleados (apellido_nombre, direccion, telefono, Dias, Horarios) VALUES (%s, %s, %s, %s, %s)",
                    (empleado.apellido_nombre, empleado.direccion, empleado.telefono, empleado.Dias, empleado.Horarios)
                )
                new_id = mycursor.lastrowid
                mydb.commit()
                mycursor.close()
                mydb.close()

                #retorna la id si es una inserción
                if empleado.action == "add_modify" and not empleado.id:
                    return PlainTextResponse(f"Exito, el empledo fue insertado y ahora su ID es: {new_id}", status_code=200)
                return PlainTextResponse("Exito", status_code=200)
    except Exception as e:
        return PlainTextResponse(f"Error{str(e)}", status_code=500)




@router.delete("/empleados/{empleado_id}", response_class=PlainTextResponse)
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


@router.get("/empleados/{empleado_id}", response_class=PlainTextResponse)
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