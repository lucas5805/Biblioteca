import mysql.connector

def conectarbd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Biblioteca"
    )
