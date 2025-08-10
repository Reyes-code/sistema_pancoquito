import mysql.connector
import random
from datetime import datetime,timedelta

# Configuración de la conexión
conexion = mysql.connector.connect(
    host="localhost",
    user="soter_admin",
    password="admin123",
    database="soter_pedidos"
)
cursor = conexion.cursor()

cursor.execute("SELECT Producto_ID FROM Productos")
categorias =  cursor.fetchall()
ids= []
for i in categorias:
    ids.append(i[0]) 
print(ids)

cantidad_minima = [random.randint(2, 10) for _ in range(len(ids))]
print(cantidad_minima)

cantidad_disponible = [random.randint(20, 100) for _ in range(len(ids))]
print(f"{cantidad_disponible}+{len(cantidad_disponible)}")


hoy = datetime.now()
fechas_actualizacion = [hoy - timedelta(days=random.randint(1, 30)) for _ in range(len(ids))]
print(fechas_actualizacion)

for index, product_id in enumerate(ids):
    query_orden = """
    INSERT INTO Inventario (Producto_Id, Cantidad_Disponible, Cantidad_Minima, Ultima_Actualizacion)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query_orden, (
        product_id,
        cantidad_disponible[index],  
        cantidad_minima[index],     
        fechas_actualizacion[index] 
    ))

conexion.commit()
cursor.close()
conexion.close()