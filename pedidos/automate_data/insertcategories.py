import mysql.connector

# Configuración de conexión
conexion = mysql.connector.connect(
    host="localhost",
    user="soter_admin",
    password="admin123",
    database="pancoquito"
)
cursor = conexion.cursor()

# Datos de categorías tech
categorias = [
    ("Pan Congelado", "Congelado"),
    ("Hojaldres Congelados", "Congelado"),
    ("Fritos Congelados", "Congelados"),
    ("Panes", "Normal"),
    ("Hojaldres", "Normal"),
    ("Fritos", "Normal"),
    ("Postres", "Postres"),
    ("Galletas", "Galletas")
]

# Insertar categorías
query = "INSERT INTO categoria (Categoria_nombre, Categoria_Tipo) VALUES (%s, %s)"
cursor.executemany(query, categorias)

conexion.commit()
cursor.close()
conexion.close()

print(f"{len(categorias)} categorías tech insertadas correctamente.")