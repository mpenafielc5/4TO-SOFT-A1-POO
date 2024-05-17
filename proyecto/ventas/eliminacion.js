// Función para obtener todos los productos del almacenamiento local
function obtenerProductos() {
    const productosJSON = localStorage.getItem("productos");
    return productosJSON ? JSON.parse(productosJSON) : [];
}

// Función para obtener todas las ventas del almacenamiento local
function obtenerVentas() {
    const ventasJSON = localStorage.getItem("ventas");
    return ventasJSON ? JSON.parse(ventasJSON) : [];
}

// Función para eliminar una venta del almacenamiento local
function eliminarVenta(numeroFactura) {
    let ventas = obtenerVentas();
    const ventaIndex = ventas.findIndex(venta => venta.numeroFactura === numeroFactura);

    if (ventaIndex !== -1) {
        // Restaurar el stock de los productos
        const productos = obtenerProductos();
        ventas[ventaIndex].detalleVenta.forEach(function(item) {
            const producto = productos.find(p => p.id === item.producto.id);
            if (producto) {
                producto.stock += item.cantidad;
            }
        });

        // Guardar los productos actualizados
        localStorage.setItem("productos", JSON.stringify(productos));

        // Eliminar la venta
        ventas.splice(ventaIndex, 1);
        localStorage.setItem("ventas", JSON.stringify(ventas));

        alert(`Venta con número de factura ${numeroFactura} eliminada exitosamente.`);
    } else {
        alert(`Venta con número de factura ${numeroFactura} no encontrada.`);
    }
}

// Evento para eliminar venta por número de factura
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("btnEliminarVenta").addEventListener("click", function() {
        const numeroFactura = parseInt(document.getElementById("numeroFacturaEliminar").value);
        if (!isNaN(numeroFactura)) {
            eliminarVenta(numeroFactura);
        } else {
            alert("Por favor, ingrese un número de factura válido.");
        }
    });
});
