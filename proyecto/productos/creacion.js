// Definición de la clase Producto
class Producto {
    constructor(id, descripcion, precio, stock) {
        this.id = id;
        this.descripcion = descripcion;
        this.precio = precio;
        this.stock = stock;
    }
}

// Función para guardar un producto en el almacenamiento local
function guardarProducto(producto) {
    const productos = obtenerProductos();
    productos.push(producto);
    localStorage.setItem("productos", JSON.stringify(productos));
}

// Función para obtener todos los productos del almacenamiento local
function obtenerProductos() {
    const productosJSON = localStorage.getItem("productos");
    return productosJSON ? JSON.parse(productosJSON) : [];
}

let contadorProductos = localStorage.getItem('contadorProductos') ? parseInt(localStorage.getItem('contadorProductos')) : 1;

// Manejo del formulario de creación de productos
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("creacionProductosForm").addEventListener("submit", function(event) {
        event.preventDefault(); // Evita que se envíe el formulario

        // Obtener los valores ingresados por el usuario
        const descripcion = document.getElementById("descripcion").value;
        const precio = document.getElementById("precio").value;
        const stock = document.getElementById("stock").value;

        // Crear un nuevo producto con ID automático
        const nuevoProducto = new Producto(
            contadorProductos++,
            descripcion,
            parseFloat(precio),
            parseInt(stock)
        );

        // Guardar el producto
        guardarProducto(nuevoProducto);

        // Mostrar mensaje de éxito
        alert("Producto creado exitosamente");

        // Limpiar los campos del formulario
        document.getElementById("descripcion").value = "";
        document.getElementById("precio").value = "";
        document.getElementById("stock").value = "";

        // Actualizar el contador de productos en el almacenamiento local
        localStorage.setItem('contadorProductos', contadorProductos);
    });
});
