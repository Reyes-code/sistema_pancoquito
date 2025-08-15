import mysql.connector
import random

# Configuración de la conexión
conexion = mysql.connector.connect(
    host="localhost",
    user="soter_admin",
    password="admin123",
    database="soter_pedidos"
)
cursor = conexion.cursor()

# Datos para tipos de envío
tipos_envio = [
    "Estándar",
    "Express",
    "Prioritario",
    "Same Day",
    "Internacional",
    "Económico"
]

# Datos para estados de envío
estados_envio = [
    "Pendiente",
    "En preparación",
    "En tránsito",
    "En reparto",
    "Entregado",
    "Retrasado",
    "Devuelto",
    "Cancelado"
]

def generar_envio():
    tipo = random.choice(tipos_envio)
    estado = random.choice(estados_envio)
    return (tipo, estado)

# Insertar 100 registros de envíos
valores_envios = [generar_envio() for _ in range(100)]

query = "INSERT INTO envio (Tipo, Estado) VALUES (%s, %s)"
cursor.executemany(query, valores_envios)

conexion.commit()
cursor.close()
conexion.close()

print(f"Se insertaron {len(valores_envios)} registros en la tabla envio correctamente.")
print("Tipos de envío utilizados:", ", ".join(tipos_envio))
print("Estados de envío utilizados:", ", ".join(estados_envio))