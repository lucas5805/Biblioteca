from fastapi import FastAPI, Depends
from autenticacion import router as auth_router # Importar autenticación
from libros import router as libros_router
from empleados import router as empleados_router
from miembros import router as miembros_router
from rentas import router as rentas_router
from inicio import router as inicio_router
app = FastAPI()

# Endpoint para obtener el token





# Incluir routers de cada módulo
app.include_router(libros_router)
app.include_router(empleados_router)
app.include_router(miembros_router)
app.include_router(rentas_router)
app.include_router(inicio_router)
app.include_router(auth_router)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
