from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse
from Proyecto.BasedeDatos import conectarbd
from passlib.context import CryptContext
import mysql.connector

router = APIRouter()

# Definir el contexto de encriptación
contexto_contraseña = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para hashear la contraseña
def generar_hash_contraseña(contraseña_plana: str) -> str:
    return contexto_contraseña.hash(contraseña_plana)

# Clase para manejar el modelo de Login
class Login(BaseModel):
    action: str
    id: int = None
    nombre: str = None
    usuario: str = None
    contraseña: str = None

# Endpoint para agregar o modificar usuarios
@router.post("/inicio")
async def manage_inicio(login: Login):
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")

        # Hashear la contraseña antes de insertarla/actualizarla
        hashed_password = generar_hash_contraseña(login.contraseña)

        if login.action == "add_modify":
            if login.id:
                # Actualizar el usuario existente
                mycursor.execute(
                    "UPDATE Usuarios SET nombre = %s, usuario = %s, contraseña = %s WHERE id = %s",
                    (login.nombre, login.usuario, hashed_password, login.id)
                )
                mydb.commit()
                return PlainTextResponse("Usuario actualizado con éxito", status_code=200)
            else:
                # Insertar nuevo usuario
                mycursor.execute(
                    "INSERT INTO Usuarios (nombre, usuario, contraseña) VALUES (%s, %s, %s)",
                    (login.nombre, login.usuario, hashed_password)
                )
                mydb.commit()
                return PlainTextResponse("Usuario insertado con éxito", status_code=200)

    except Exception as e:
        return PlainTextResponse(f"Error: {str(e)}", status_code=500)

    finally:
        if mycursor:
            mycursor.close()
        if mydb:
            mydb.close()

# Obtener todos los usuarios
@router.get("/api/inicio", response_class=PlainTextResponse)
async def get_inicio():
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")
        mycursor.execute("SELECT id, nombre, usuario, contraseña FROM Usuarios")
        inicio = mycursor.fetchall()

        inicio_list = [
            f"id: {login[0]}, nombre: {login[1]}, usuario: {login[2]}, contraseña: {login[3]} "
            for login in inicio
        ]

        return "\n".join(inicio_list)

    except Exception as e:
        return PlainTextResponse(f"Error: {str(e)}", status_code=500)

    finally:
        if mycursor:
            mycursor.close()
        if mydb:
            mydb.close()

# Obtener usuario por ID
@router.get("/inicio/{inicio_id}", response_class=PlainTextResponse)
async def get_inicio_by_id(inicio_id: int):
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")

        mycursor.execute("SELECT id, nombre, usuario, contraseña FROM Usuarios WHERE id = %s", (inicio_id,))
        login = mycursor.fetchone()

        if not login:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        login_info = f"id: {login[0]}, nombre: {login[1]}, usuario: {login[2]}, contraseña: {login[3]}"
        return PlainTextResponse(login_info, status_code=200)

    except HTTPException as e:
        return PlainTextResponse(e.detail, status_code=e.status_code)

    except Exception as e:
        return PlainTextResponse(f"Error: {str(e)}", status_code=500)

    finally:
        if mycursor:
            mycursor.close()
        if mydb:
            mydb.close()

# Eliminar usuario por ID
@router.delete("/inicio/{inicio_id}", response_class=PlainTextResponse)
async def delete_inicio(inicio_id: int):
    try:
        mydb = conectarbd()
        mycursor = mydb.cursor()
        mycursor.execute("USE Biblioteca")

        mycursor.execute("DELETE FROM Usuarios WHERE id = %s", (inicio_id,))
        if mycursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        mydb.commit()
        return PlainTextResponse("Usuario eliminado con éxito", status_code=200)

    except HTTPException as e:
        return PlainTextResponse(e.detail, status_code=e.status_code)

    except Exception as e:
        return PlainTextResponse(f"Error: {str(e)}", status_code=500)

    finally:
        if mycursor:
            mycursor.close()
        if mydb:
            mydb.close()



