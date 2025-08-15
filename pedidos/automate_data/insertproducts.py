import mysql.connector
import random
from datetime import datetime

# Configuración de la conexión
conexion = mysql.connector.connect(
    host="localhost",
    user="soter_admin",
    password="admin123",
    database="soter_pedidos"
)
cursor = conexion.cursor()

# Obtener categorías existentes
cursor.execute("SELECT Categoria_ID, Categoria_nombre FROM categoria")
categorias = {nombre: id for id, nombre in cursor.fetchall()}

# Productos por categoría con precios en COP (con 2 decimales)
productos_por_categoria = {
    "Procesadores": [
        ("Intel Core i9-13900K", 4_500_000.00),
        ("AMD Ryzen 9 7950X", 4_200_000.00),
        ("Intel Core i7-13700K", 3_200_000.00),
        ("AMD Ryzen 7 7800X3D", 3_500_000.00)
    ],
    "Tarjetas Gráficas": [
        ("NVIDIA RTX 4090", 12_000_000.00),
        ("AMD RX 7900 XTX", 7_800_000.00),
        ("NVIDIA RTX 4080", 9_200_000.00),
        ("AMD RX 7800 XT", 4_300_000.00)
    ],
    "Memorias RAM": [
        ("Corsair Dominator 32GB DDR5", 1_500_000.00),
        ("G.Skill Trident Z 64GB DDR4", 1_900_000.00),
        ("Kingston Fury 16GB DDR4", 600_000.00),
        ("Crucial Ballistix 32GB DDR4", 1_000_000.00)
    ],
    "Teclados": [
        ("Logitech G915 TKL", 1_800_000.00),
        ("Razer BlackWidow V4 Pro", 1_500_000.00),
        ("Corsair K100 RGB", 1_500_000.00),
        ("Keychron Q3", 1_200_000.00)
    ],
    "Mouse": [
        ("Logitech G Pro X Superlight", 1_200_000.00),
        ("Razer Viper V2 Pro", 1_100_000.00),
        ("SteelSeries Aerox 5", 750_000.00),
        ("Corsair Dark Core RGB Pro", 600_000.00)
    ],
    "Monitores": [
        ("Samsung Odyssey G9", 11_000_000.00),
        ("LG UltraGear 38GN950", 9_800_000.00),
        ("ASUS ROG Swift PG32UQX", 22_500_000.00),
        ("Dell Alienware AW3423DW", 9_800_000.00)
    ],
    "Coolers": [
        ("Noctua NH-D15", 850_000.00),
        ("Corsair iCUE H150i", 1_500_000.00),
        ("Cooler Master Hyper 212", 380_000.00),
        ("NZXT Kraken Z73", 2_300_000.00)
    ],
    "DSLR": [
        ("Canon EOS 5D Mark IV", 9_500_000.00),
        ("Nikon D850", 10_500_000.00),
        ("Canon EOS 90D", 4_500_000.00),
        ("Nikon D7500", 3_800_000.00)
    ],
    "Drones Profesionales": [
        ("DJI Mavic 3 Pro", 8_200_000.00),
        ("DJI Air 2S", 3_800_000.00),
        ("Autel Robotics EVO II", 5_700_000.00),
        ("DJI Phantom 4 Pro V2.0", 6_100_000.00)
    ],
    "Routers": [
        ("ASUS ROG Rapture GT-AX11000", 1_700_000.00),
        ("TP-Link Archer AX6000", 950_000.00),
        ("Netgear Nighthawk AX12", 2_300_000.00),
        ("Linksys Atlas Pro 6", 1_500_000.00)
    ]
}

# Insertar productos
query = "INSERT INTO productos (producto_nombre, Categoria_ID, precio, activo) VALUES (%s, %s, %s, %s)"
valores_productos = []

for categoria_nombre, productos in productos_por_categoria.items():
    categoria_id = categorias.get(categoria_nombre)
    if categoria_id:
        for nombre, precio in productos:
            # 90% de probabilidad de estar activo
            activo = random.random() < 0.90
            valores_productos.append((nombre, categoria_id, precio, activo))

cursor.executemany(query, valores_productos)

conexion.commit()

print(f"Se insertaron {len(valores_productos)} productos tech con precios en COP")
print("Distribución por categoría:")
for cat in categorias:
    cursor.execute("SELECT COUNT(*) FROM productos WHERE Categoria_ID = %s", (categorias[cat],))
    count = cursor.fetchone()[0]
    if count > 0:
        print(f"- {cat}: {count} productos")

cursor.close()
conexion.close()