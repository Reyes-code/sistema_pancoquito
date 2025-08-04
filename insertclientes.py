import mysql.connector
import random

nombres = [
    "Juan", "María", "José", "Luisa", "Carlos", "Ana", "Pedro", "Sofía", "Miguel", "Isabella",
    "Jorge", "Carmen", "Luis", "Valentina", "Diego", "Lucía", "Fernando", "Camila", "Ricardo", "Elena",
    "Andrés", "Gabriela", "Roberto", "Daniela", "Raúl", "Paula", "Manuel", "Adriana", "Santiago", "Alejandra",
    "Héctor", "Rosa", "Francisco", "Patricia", "Antonio", "Mariana", "Alberto", "Guadalupe", "David", "Teresa",
    "Javier", "Verónica", "Arturo", "Liliana", "Mario", "Claudia", "Oscar", "Ximena", "Pablo", "Natalia",
    "Enrique", "Silvia", "Rafael", "Angélica", "Gustavo", "Beatriz", "Eduardo", "Diana", "Víctor", "Rocío",
    "Alfredo", "Monica", "Gerardo", "Alicia", "Rodrigo", "Carolina", "Felipe", "Esther", "Joaquín", "Julia",
    "Salvador", "Lorena", "Emilio", "Rebeca", "Hugo", "Olivia", "Ignacio", "Noemí", "César", "Irene",
    "Ramón", "Consuelo", "Sergio", "Miriam", "Martín", "Leticia", "Ernesto", "Yolanda", "Julio", "Esperanza",
    "Agustín", "Perla", "Guillermo", "Pilar", "Ramiro", "Amalia", "Federico", "Rosario", "Baltazar", "Inés"
]

apellidos = [
    "García", "Rodríguez", "Martínez", "Hernández", "López", "González", "Pérez", "Sánchez", "Ramírez", "Torres",
    "Flores", "Rivera", "Gómez", "Díaz", "Cruz", "Morales", "Reyes", "Ortiz", "Jiménez", "Vásquez",
    "Castillo", "Romero", "Álvarez", "Mendoza", "Ruiz", "Chávez", "Ramos", "Ortega", "Medina", "Guerrero",
    "Paredes", "Silva", "Vega", "Rojas", "Salazar", "Castro", "Núñez", "Delgado", "Acosta", "Miranda",
    "Cabrera", "Valdez", "Cortés", "Bravo", "Franco", "León", "Aguilar", "Molina", "Suárez", "Vargas",
    "Cárdenas", "Quiroz", "Espinoza", "Campos", "Santos", "Peña", "Aguirre", "Fuentes", "Navarro", "Serrano"
]




def generar_nombre():
    nombre = random.choice(nombres)
    apellido1 = random.choice(apellidos)
    apellido2 = random.choice(apellidos)
    return f"{nombre} {apellido1} {apellido2}"
def generar_email(nombre):
    dominios = ["gmail.com", "hotmail.com", "yahoo.com", "outlook.com"]
    nombre = nombre.replace(" ", "").lower()
    return f"{nombre.lower()}{random.randint(10, 99)}@{random.choice(dominios)}"


def generar_telefono():
    return f"+57 {random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

def generar_cedula():
    return random.randint(1000000000,1000999999)

conexion = mysql.connector.connect(
    host="localhost",
    user="soter_admin",  
    password="admin123",  
    database="soter_pedidos"  
)

cursor = conexion.cursor()
for _ in range(100):
    nombre = generar_nombre()
    email = generar_email(nombre)
    telefono = generar_telefono()
    cedula = generar_cedula()

    query = "INSERT INTO cliente (Nombre, Email, Telefono, Cedula) VALUES (%s, %s, %s,%s)"
    valores = (nombre, email, telefono, cedula)
    cursor.execute(query, valores)

conexion.commit()
cursor.close()
conexion.close()

print("100 registros insertados correctamente.")