from fastapi import Request, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.exception_handlers import http_exception_handler
from fastapi import FastAPI
from autenticacion import router as auth_router
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


# Manejar las excepciones globalmente
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 403:
        return PlainTextResponse(f"Acceso denegado: {exc.detail}", status_code=403)
    elif exc.status_code == 404:
        return PlainTextResponse(f"No encontrado: {exc.detail}", status_code=404)
    elif exc.status_code == 400:
        return PlainTextResponse(f"Error de solicitud: {exc.detail}", status_code=400)
    elif exc.status_code == 401:
        return PlainTextResponse(f"Autenticación fallida: {exc.detail}", status_code=401)

    # Para otros errores, devuelves el mensaje de error predeterminado de la excepción
    return PlainTextResponse(f"Error desconocido: {exc.detail}", status_code=exc.status_code)

    # Para otros tipos de error, devolver el comportamiento predeterminado
    return await http_exception_handler(request, exc)
