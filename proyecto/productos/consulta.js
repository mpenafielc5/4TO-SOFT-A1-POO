// Función para obtener todos los productos del almacenamiento local
function obtenerProductos() {
    const productosJSON = localStorage.getItem("productos");
    return productosJSON ? JSON.parse(productosJSON) : [];
}

// Función para mostrar los productos en la página
function mostrarProductos() {
    const listaProductos = document.getElementById("listaProductos");
    listaProductos.innerHTML = ""; // Limpiar la lista antes de mostrar los productos

    const productos = obtenerProductos();
    productos.forEach(function(producto) {
        const li = document.createElement("li");
        li.textContent = `ID: ${producto.id} - Descripción: ${producto.descripcion} - Precio: ${producto.precio} - Stock: ${producto.stock}`;
        listaProductos.appendChild(li);
    });
}

// Mostrar los productos al cargar la página
document.addEventListener("DOMContentLoaded", function() {
    mostrarProductos();
});
