// Función para obtener todos los productos del almacenamiento local
function obtenerProductos() {
    const productosJSON = localStorage.getItem("productos");
    return productosJSON ? JSON.parse(productosJSON) : [];
}

// Función para eliminar un producto
function eliminarProducto(id) {
    let productos = obtenerProductos();
    productos = productos.filter(producto => producto.id !== id);
    localStorage.setItem("productos", JSON.stringify(productos));
    alert("Producto eliminado exitosamente");
    mostrarProductos();
}

// Función para mostrar los productos en la página
function mostrarProductos() {
    const listaProductos = document.getElementById("listaProductos");
    listaProductos.innerHTML = ""; // Limpiar la lista antes de mostrar los productos

    const productos = obtenerProductos();
    productos.forEach(function(producto) {
        const li = document.createElement("li");
        li.textContent = `ID: ${producto.id} - Descripción: ${producto.descripcion} - Precio: ${producto.precio} - Stock: ${producto.stock}`;
        
        const btnEliminar = document.createElement("button");
        btnEliminar.textContent = "Eliminar";
        btnEliminar.addEventListener("click", function() {
            if (confirm("¿Estás seguro de que deseas eliminar este producto?")) {
                eliminarProducto(producto.id);
            }
        });

        li.appendChild(btnEliminar);
        listaProductos.appendChild(li);
    });
}

// Mostrar los productos al cargar la página
document.addEventListener("DOMContentLoaded", function() {
    mostrarProductos();
});
