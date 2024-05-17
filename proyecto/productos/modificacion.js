// Función para obtener todos los productos del almacenamiento local
function obtenerProductos() {
    const productosJSON = localStorage.getItem("productos");
    return productosJSON ? JSON.parse(productosJSON) : [];
}

// Función para mostrar los productos en el select
function mostrarProductosSelect() {
    const selectProducto = document.getElementById("selectProducto");
    selectProducto.innerHTML = ""; // Limpiar el select antes de agregar productos

    const productos = obtenerProductos();
    productos.forEach(function(producto) {
        const option = document.createElement("option");
        option.value = producto.id;
        option.textContent = `${producto.descripcion}`;
        selectProducto.appendChild(option);
    });
}

// Función para cargar los datos del producto seleccionado
function cargarDatosProducto() {
    const selectProducto = document.getElementById("selectProducto");
    const productoId = parseInt(selectProducto.value);

    const productos = obtenerProductos();
    const producto = productos.find(p => p.id === productoId);

    if (producto) {
        document.getElementById("descripcion").value = producto.descripcion;
        document.getElementById("precio").value = producto.precio;
        document.getElementById("stock").value = producto.stock;
    }
}

// Función para modificar el producto seleccionado
function modificarProducto() {
    const selectProducto = document.getElementById("selectProducto");
    const productoId = parseInt(selectProducto.value);
    const descripcion = document.getElementById("descripcion").value;
    const precio = parseFloat(document.getElementById("precio").value);
    const stock = parseInt(document.getElementById("stock").value);

    const productos = obtenerProductos();
    const indice = productos.findIndex(p => p.id === productoId);

    if (indice !== -1) {
        productos[indice].descripcion = descripcion;
        productos[indice].precio = precio;
        productos[indice].stock = stock;

        localStorage.setItem("productos", JSON.stringify(productos));
        alert("Producto modificado exitosamente");

        // Actualizar la lista de productos en el select
        mostrarProductosSelect();
        // Limpiar los campos del formulario
        document.getElementById("descripcion").value = "";
        document.getElementById("precio").value = "";
        document.getElementById("stock").value = "";
        document.getElementById("selectProducto").value = "";
    } else {
        alert("Producto no encontrado");
    }
}

// Mostrar los productos en el select al cargar la página
document.addEventListener("DOMContentLoaded", function() {
    mostrarProductosSelect();
    document.getElementById("selectProducto").addEventListener("change", cargarDatosProducto);
    document.getElementById("btnModificar").addEventListener("click", modificarProducto);
});
