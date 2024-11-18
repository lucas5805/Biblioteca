from fastapi import APIRouter, HTTPException, Depends, Body
from pydantic import BaseModel
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from passlib.context import CryptContext
from Proyecto.BasedeDatos import conectarbd
from typing import Optional

router = APIRouter()

# Configuración JWT
CLAVE_SECRETA = "50yun93n10"
ALGORITMO = "HS256"
TIEMPO_EXPIRACION_TOKEN_MINUTOS = 30

# Contexto de encriptación para las contraseñas
contexto_contraseña = CryptContext(schemes=["bcrypt"], deprecated="auto")
esquema_oauth2 = OAuth2PasswordBearer(tokenUrl="token")

# Clase para el login del usuario
class DatosLogin(BaseModel):
    usuario: str
    contraseña: str

# Función para obtener el usuario desde la base de datos
def obtener_usuario_por_nombreusuario(nombre_usuario: str):
    conexion_bd = conectarbd()
    cursor = conexion_bd.cursor(dictionary=True)
    cursor.execute("USE Biblioteca")
    cursor.execute("SELECT * FROM Usuarios WHERE usuario = %s", (nombre_usuario,))
    usuario = cursor.fetchone()
    cursor.close()
    conexion_bd.close()
    return usuario

# Función para generar un token JWT
def crear_token_acceso(datos: dict, expira_delta: Optional[timedelta] = None):
    datos_a_codificar = datos.copy()
    if expira_delta:
        expira = datetime.utcnow() + expira_delta
    else:
        expira = datetime.utcnow() + timedelta(minutes=15)
    datos_a_codificar.update({"exp": expira})
    token_jwt_codificado = jwt.encode(datos_a_codificar, CLAVE_SECRETA, algorithm=ALGORITMO)
    return token_jwt_codificado

# Función para verificar la contraseña
def verificar_contraseña(contraseña_plana: str, contraseña_hash: str) -> bool:
    return contexto_contraseña.verify(contraseña_plana, contraseña_hash)

# En el login
@router.post("/token")
async def login_para_token_acceso(datos_formulario: DatosLogin):
    usuario = obtener_usuario_por_nombreusuario(datos_formulario.usuario)

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verificar que la contraseña ingresada coincide con el hash almacenado
    if not verificar_contraseña(datos_formulario.contraseña, usuario['contraseña']):
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_expira_en = timedelta(minutes=TIEMPO_EXPIRACION_TOKEN_MINUTOS)
    token_acceso = crear_token_acceso(
        datos={"sub": usuario["usuario"], "rol": usuario["rol"]},
        expira_delta=token_expira_en
    )

    return {"token_acceso": token_acceso, "tipo_token": "bearer"}

# Función para validar el token JWT
async def get_current_user(token: str = Depends(esquema_oauth2)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="No se pueden validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, CLAVE_SECRETA, algorithms=[ALGORITMO])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = obtener_usuario_por_nombreusuario(username)
    if user is None:
        raise credentials_exception
    return user

# Endpoint protegido que retorna la información del usuario autenticado
@router.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user

async def get_current_user_with_role(token: str = Depends(esquema_oauth2), required_role: str = None):
    credentials_exception = HTTPException(
        status_code=401,
        detail="No se pueden validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, CLAVE_SECRETA, algorithms=[ALGORITMO])
        username: str = payload.get("sub")
        user_role: str = payload.get("rol")
        if username is None or user_role is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = obtener_usuario_por_nombreusuario(username)
    if user is None:
        raise credentials_exception
    if required_role and user_role != required_role:
        raise HTTPException(status_code=403, detail="No tiene permisos suficientes")
    return user


@router.get("/admin-only")
async def admin_only(current_user: dict = Depends(lambda: get_current_user_with_role(required_role="admin"))):
    return {"message": "Esto solo es accesible para administradores."}

@router.post("/change-role")
async def change_user_role(
        username: str = Body(..., embed=True),
        new_role: str = Body(..., embed=True),
        current_user: dict = Depends(lambda: get_current_user_with_role(token=Depends(esquema_oauth2), required_role="admin"))
):
    mydb = conectarbd()
    mycursor = mydb.cursor()
    mycursor.execute("USE Biblioteca")
    mycursor.execute("UPDATE inicio SET rol = %s WHERE usuario = %s", (new_role, username))
    mydb.commit()
    mycursor.close()
    mydb.close()
    return {"message": f"Rol de {username} cambiado a {new_role}"}
