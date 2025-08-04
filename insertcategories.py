import mysql.connector

# Configuración de conexión
conexion = mysql.connector.connect(
    host="localhost",
    user="soter_admin",
    password="admin123",
    database="soter_pedidos"
)
cursor = conexion.cursor()

# Datos de categorías tech
categorias_tech = [
    ("Componentes PC", "Hardware"),
    ("Periféricos", "Dispositivos"),
    ("Accesorios PC", "Complementos"),
    ("Cámaras", "Fotografía"),
    ("Drones", "Tecnología Aérea"),
    ("Redes", "Conectividad"),
    ("Procesadores", "Hardware"),
    ("Tarjetas Gráficas", "Hardware"),
    ("Memorias RAM", "Hardware"),
    ("Teclados", "Dispositivos"),
    ("Mouse", "Dispositivos"),
    ("Monitores", "Dispositivos"),
    ("Coolers", "Complementos"),
    ("Gabinetes", "Complementos"),
    ("DSLR", "Fotografía"),
    ("Mirrorless", "Fotografía"),
    ("Lentes", "Fotografía"),
    ("Drones Profesionales", "Tecnología Aérea"),
    ("Drones Recreativos", "Tecnología Aérea"),
    ("Routers", "Conectividad"),
    ("Switches", "Conectividad")
]

# Insertar categorías
query = "INSERT INTO categoria (Categoria_nombre, Categoria_Tipo) VALUES (%s, %s)"
cursor.executemany(query, categorias_tech)

conexion.commit()
cursor.close()
conexion.close()

print(f"{len(categorias_tech)} categorías tech insertadas correctamente.")