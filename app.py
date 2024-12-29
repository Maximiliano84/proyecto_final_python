import sqlite3
from colorama import Fore, Style, init
from tabulate import tabulate
import unicodedata


init(autoreset=True)

def conectar_base_datos():
    """Conecta a la base de datos y crea la tabla si no existe."""
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL CHECK(cantidad >= 0),
            precio REAL NOT NULL CHECK(precio >= 0),
            categoria TEXT
        )
    ''')
    conexion.commit()
    return conexion

def validar_entero(mensaje, permitir_vacio=False):
    """Valida que el usuario ingrese un número entero válido."""
    while True:
        try:
            valor = input(mensaje)
            if valor == '' and permitir_vacio:
                return None  # Permite vacío si se indica
            valor = int(valor)
            if valor < 0:
                raise ValueError
            return valor
        except ValueError:
            print(Fore.RED + "Entrada inválida. Por favor, ingrese un número entero no negativo.")

def validar_flotante(mensaje):
    """Valida que el usuario ingrese un número flotante válido."""
    while True:
        try:
            valor = float(input(mensaje))
            if valor < 0:
                raise ValueError
            return valor
        except ValueError:
            print(Fore.RED + "Entrada inválida. Por favor, ingrese un número no negativo.")

def quitar_tildes(texto):
    """Elimina las tildes de un texto."""
    return ''.join((c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn'))

def agregar_producto(conexion):
    """Permite agregar un nuevo producto al inventario."""
    nombre = input(Fore.GREEN + "Ingrese el nombre del producto: ").strip()
    while not nombre:
        print(Fore.RED + "El nombre no puede estar vacío.")
        nombre = input(Fore.GREEN + "Ingrese el nombre del producto: ").strip()

    descripcion = input("Ingrese una descripción: ").strip()
    cantidad = validar_entero(Fore.GREEN + "Ingrese la cantidad: ")
    precio = validar_flotante("Ingrese el precio: ")
    
    # Bucle para pedir categoría hasta que sea válida
    categorias_validas = ['almacen', 'carniceria', 'perfumeria', 'verduleria', 'varios']
    while True:
        categoria = input(Fore.GREEN + "Ingrese la categoría: ").strip().lower()
        
    # Verificar si la categoría es válida
        categoria = quitar_tildes(categoria)
        
        if categoria in categorias_validas:
            break  # Salir del bucle si la categoría es válida
        else:
            print(Fore.RED + "Categoría no encontrada. Las categorías válidas son: almacen, carniceria, perfumeria, verduleria, varios.")
    
    cursor = conexion.cursor()
    cursor.execute(''' 
        INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
        VALUES (?, ?, ?, ?, ?)
    ''', (nombre, descripcion, cantidad, precio, categoria))
    conexion.commit()
    print(Fore.YELLOW + "\nProducto agregado exitosamente.")

def mostrar_productos(conexion):
    """Muestra todos los productos registrados en forma de tabla."""
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    if productos:
        headers = ["ID", "Nombre", "Descripción", "Cantidad", "Precio", "Categoría"]
        table = []
        
        # Crear la tabla con los datos de los productos
        for producto in productos:
            table.append([producto[0], producto[1], producto[2], producto[3], f"${producto[4]:.2f}", producto[5]])

        # Mostrar la tabla
        print(Fore.CYAN + "\nLista de productos:")
        print(tabulate(table, headers=headers, tablefmt="fancy_grid", numalign="center"))
    else:
        print(Fore.RED + "\nNo hay productos registrados.")

def actualizar_producto(conexion):
    """Actualiza todos los campos de un producto específico, excepto el ID."""
    
    # Pedir al usuario el ID del producto
    id_producto = validar_entero(Fore.GREEN + "Ingrese el ID del producto a actualizar: ")
    
    # Obtener los datos actuales del producto
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
    producto = cursor.fetchone()

    if producto:
        # Mostrar los detalles actuales del producto
        print(Fore.GREEN + "\nDetalles actuales del producto:")
        print(Fore.WHITE + f"ID: {producto[0]}")
        print(Fore.WHITE + f"Nombre: {producto[1]}")
        print(Fore.WHITE + f"Cantidad: {producto[2]}")
        print(Fore.WHITE + f"Categoría: {producto[3]}")
        print(Fore.WHITE + f"Precio: ${producto[4]}")
        print(Fore.WHITE + f"Descripción: {producto[5]}")
        
        # Solicitar nuevos valores al usuario (dejar vacío para mantener el valor actual)
        nuevo_nombre = input(Fore.YELLOW + "Nuevo nombre (dejar vacío para mantener el actual): ")
        nueva_descripcion = input(Fore.YELLOW + "Nueva descripción (dejar vacío para mantener la actual): ")
        nueva_categoria = input(Fore.YELLOW + "Nueva categoría (dejar vacío para mantener la actual): ")
        nuevo_precio = input(Fore.YELLOW + "Nuevo precio (dejar vacío para mantener el actual): ")
        nueva_cantidad = input(Fore.YELLOW + "Nueva cantidad (dejar vacío para mantener la actual): ")

        # Si el usuario no ingresa un nuevo valor, mantendrá el valor original
        nombre = nuevo_nombre if nuevo_nombre else producto[1]
        descripcion = nueva_descripcion if nueva_descripcion else producto[2]
        cantidad = int(nueva_cantidad) if nueva_cantidad else producto[3]
        precio = float(nuevo_precio) if nuevo_precio else producto[4]
        categoria = nueva_categoria if nueva_categoria else producto[5]

        # Realizar la actualización en la base de datos
        cursor.execute("""
            UPDATE productos
            SET nombre = ?, descripcion = ?, categoria = ?, precio = ?, cantidad = ?
            WHERE id = ?
        """, (nombre, descripcion, categoria, precio, cantidad, id_producto))

        conexion.commit()

        if cursor.rowcount:
            print(Fore.YELLOW + "\nProducto actualizado correctamente.")
        else:
            print(Fore.RED + "\nNo se pudo actualizar el producto.")
    else:
        print(Fore.RED + "\nProducto no encontrado. Verifique el ID ingresado.")
    

def eliminar_producto(conexion):
    """Elimina un producto del inventario."""
    id_producto = validar_entero(Fore.GREEN + "Ingrese el ID del producto a eliminar: ")

    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
    conexion.commit()

    if cursor.rowcount:
        print(Fore.YELLOW + "\nProducto eliminado exitosamente.")
    else:
        print(Fore.RED + "\nProducto no encontrado.")

def buscar_producto(conexion):
    """Busca un producto por ID, nombre o categoría."""
    print("1. Buscar por ID")
    print("2. Buscar por nombre")
    print("3. Buscar por categoría")
    opcion = validar_entero(Fore.GREEN + "Seleccione una opción: ")

    cursor = conexion.cursor()

    if opcion == 1:
        id_producto = validar_entero(Fore.GREEN + "Ingrese el ID del producto: ")
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
    elif opcion == 2:
        nombre = input(Fore.GREEN + "Ingrese el nombre del producto: ").strip()
        while not nombre:
            print(Fore.RED + "El nombre no puede estar vacío.")
            nombre = input("Ingrese el nombre del producto: ").strip()
        cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", (f"%{nombre}%",))
    elif opcion == 3:
        categoria = input(Fore.GREEN + "Ingrese la categoría: ").strip()
        while not categoria:
            print(Fore.RED + "La categoría no puede estar vacía.")
            categoria = input("Ingrese la categoría: ").strip()
        cursor.execute("SELECT * FROM productos WHERE categoria LIKE ?", (f"%{categoria}%",))
    else:
        print(Fore.RED + "\nOpción inválida.")
        return

    productos = cursor.fetchall()
    if productos:
        # Usar tabulate
        headers = ["ID", "Nombre", "Descripción", "Cantidad", "Precio", "Categoría"]
        table = [list(producto) for producto in productos]
        print(tabulate(table, headers, tablefmt="fancy_grid"))
    else:
        print(Fore.RED + "\nNo se encontraron productos.")

def generar_reporte_bajo_stock(conexion):
    """Genera un reporte de productos con bajo stock."""
    limite = validar_entero(Fore.GREEN + "Ingrese el límite de stock: ")

    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (limite,))
    productos = cursor.fetchall()

    if productos:
        # Usar tabulate 
        headers = ["ID", "Nombre", "Descripción", "Cantidad", "Precio", "Categoría"]
        table = [list(producto) for producto in productos]
        print(Fore.CYAN + "\nProductos con bajo stock:")
        print(tabulate(table, headers, tablefmt="fancy_grid"))
    else: 
        print(Fore.RED + "\nNo hay productos con bajo stock.")

def menu_principal():
    """Muestra el menú principal y gestiona la interacción del usuario."""
    conexion = conectar_base_datos()

    while True:
        # Verificar si hay productos en la base de datos
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM productos")
        cantidad_productos = cursor.fetchone()[0]
        
        # Encabezado del menú
        print(Fore.CYAN + Style.BRIGHT + "\n" + "="*35)
        print(Fore.CYAN + Style.BRIGHT + "       MENÚ PRINCIPAL")
        print(Fore.CYAN + Style.BRIGHT + "="*35)
        
        # Opciones del menú
        print(Fore.GREEN + "1. " + Fore.WHITE + "Agregar producto")
        print(Fore.GREEN + "2. " + Fore.WHITE + "Mostrar productos")
        print(Fore.GREEN + "3. " + Fore.WHITE + "Actualizar producto")
        print(Fore.GREEN + "4. " + Fore.WHITE + "Eliminar producto")
        print(Fore.GREEN + "5. " + Fore.WHITE + "Buscar producto")
        print(Fore.GREEN + "6. " + Fore.WHITE + "Reporte bajo stock")
        print(Fore.GREEN + "7. " + Fore.WHITE + "Salir")
        
        print(Fore.CYAN + Style.BRIGHT + "="*35)
        
        # Obtener la opción del usuario
        opcion = validar_entero(Fore.YELLOW + "Seleccione una opción: ")

        # Verificación para las opciones 2-6 si no hay productos
        if opcion in [2, 3, 4, 5, 6] and cantidad_productos == 0:
            print(Fore.RED + "\nDebe agregar productos para la opción seleccionada.")
            continue  # Volver a mostrar el menú

        # Llamado a las funciones
        if opcion == 1:
            agregar_producto(conexion)
        elif opcion == 2:
            mostrar_productos(conexion)
        elif opcion == 3:
            actualizar_producto(conexion)
        elif opcion == 4:
            eliminar_producto(conexion)
        elif opcion == 5:
            buscar_producto(conexion)
        elif opcion == 6:
            generar_reporte_bajo_stock(conexion)
        elif opcion == 7:
            print(Fore.YELLOW + Style.BRIGHT + "\nSaliendo de la aplicación. ¡Hasta luego!")
            break
        else:
            # Mostrar mensaje de advertencia si el usuario intenta seleccionar una opción no válida
            print(Fore.RED + "\nOpción inválida. Intente nuevamente.")

    conexion.close()

if __name__ == "__main__":
    menu_principal()

