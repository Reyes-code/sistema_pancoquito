import mysql.connector
import random
from datetime import datetime, timedelta

# Configuración de la conexión
conexion = mysql.connector.connect(
    host="localhost",
    user="soter_admin",
    password="admin123",
    database="soter_pedidos"
)
cursor = conexion.cursor()

# 1. Obtener IDs existentes
cursor.execute("SELECT Cliente_ID FROM cliente")
clientes_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT Envio_ID FROM envio")
envios_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT Producto_ID, precio FROM productos WHERE activo = 1")
productos_disponibles = cursor.fetchall()

if not clientes_ids or not envios_ids or not productos_disponibles:
    print("Error: Debe existir al menos 1 cliente, 1 envío y 1 producto activo")
    exit()

# 2. Generar fechas aleatorias (últimos 2 años)
    hoy = datetime.now()
    fechas_orden = [hoy - timedelta(days=random.randint(1, 730)) for _ in range(100)]

# 3. Insertar órdenes y detalles
for i in range(100):
    # Seleccionar aleatoriamente cliente y envío existentes
    cliente_id = random.choice(clientes_ids)
    envio_id = random.choice(envios_ids)
    
    # Insertar orden
    query_orden = """
    INSERT INTO orden (Fecha_Orden, Cliente_ID, Envio_ID)
    VALUES (%s, %s, %s)
    """
    cursor.execute(query_orden, (fechas_orden[i], cliente_id, envio_id))
    pedido_id = cursor.lastrowid
    
    # Insertar detalles de orden (1-5 productos por orden)
    num_productos = random.randint(1, 5)
    productos_seleccionados = random.sample(productos_disponibles, min(num_productos, len(productos_disponibles)))
    
    for producto_id, precio in productos_seleccionados:
        cantidad = random.randint(1, 3)  # Cantidad entre 1 y 3 unidades
        
        query_detalle = """
        INSERT INTO orden_detalle (pedido_id, Producto_ID, cantidad, precio_unitario)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query_detalle, (pedido_id, producto_id, cantidad, precio))

conexion.commit()

# Estadísticas
cursor.execute("SELECT COUNT(*) FROM orden")
total_ordenes = cursor.fetchone()[0]

cursor.execute("""
    SELECT c.Categoria_nombre, COUNT(*) 
    FROM orden_detalle od
    JOIN productos p ON od.Producto_ID = p.Producto_ID
    JOIN categoria c ON p.Categoria_ID = c.Categoria_ID
    GROUP BY c.Categoria_nombre
""")
distribucion_categorias = cursor.fetchall()

print(f"\nSe crearon {total_ordenes} órdenes completas")
print("\nDistribución de productos vendidos por categoría:")
for categoria, cantidad in distribucion_categorias:
    print(f"- {categoria}: {cantidad} unidades")

cursor.close()
conexion.close()