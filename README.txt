README.txt
Descripción
Este programa es un sistema de gestión de inventarios de productos. Permite realizar operaciones básicas como agregar, mostrar, actualizar, eliminar y buscar productos en una base de datos SQLite. Además, incluye una funcionalidad para generar un reporte de productos con bajo stock. El programa utiliza la biblioteca colorama para mejorar la experiencia del usuario con colores en la interfaz de texto y tabulate para mostrar los productos en formato tabular.

Funcionalidades
1. Agregar producto
Permite agregar un nuevo producto al inventario.
Se solicita información como el nombre, descripción, cantidad, precio y categoría del producto.
Las categorías válidas son: almacen, carnicería, perfumería, verdulería, y varios.

2. Mostrar productos
Muestra todos los productos registrados en la base de datos en formato tabular, con columnas como ID, nombre, descripción, cantidad, precio y categoría.
Si no hay productos registrados, muestre un mensaje de advertencia.

3. Actualizar producto
Permite actualizar los detalles de un producto específico, utilizando su ID.
Se pueden actualizar campos como el nombre, descripción, cantidad, precio y categoría del producto.
Si no se ingresa un valor nuevo para algún campo, se mantiene el valor original.

4. Eliminar producto
Elimine un producto del inventario usando su identificación.
Si el producto no existe, muestra un mensaje de error.

5. Buscar producto
Permite buscar productos por ID, nombre o categoría.
Muestra los productos encontrados en formato tabular.

6. Generar informe de bajo stock
Muestra los productos cuyo stock es menor o igual al límite especificado por el usuario.
Los productos se presentan en formato tabular.

7. Salir
Permite salir del sistema.

Bibliotecas utilizadas:
sqlite3: incluido en la instalación estándar de Python.
colorama: para la gestión de colores en la consola.
tabulate: para mostrar tablas en la consola.

Notas
El programa crea una base de datos llamada inventario.db.
Las operaciones de actualización y eliminación se realizan mediante el ID del producto, el cual se asigna automáticamente al agregar un nuevo producto.
