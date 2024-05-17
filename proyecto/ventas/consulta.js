// Función para obtener todas las ventas del almacenamiento local
function obtenerVentas() {
    const ventasJSON = localStorage.getItem("ventas");
    return ventasJSON ? JSON.parse(ventasJSON) : [];
}

// Función para mostrar los números de factura en el select
function mostrarFacturasSelect() {
    const selectFactura = document.getElementById("selectFactura");
    const ventas = obtenerVentas();
    ventas.forEach(function(venta) {
        const option = document.createElement("option");
        option.value = venta.numeroFactura;
        option.textContent = `Factura N° ${venta.numeroFactura}`;
        selectFactura.appendChild(option);
    });
}

// Función para mostrar la información de una factura
function mostrarInformacionFactura(factura) {
    const facturaInfo = document.getElementById("facturaInfo");
    document.getElementById("facturaNumero").textContent = factura.numeroFactura;
    document.getElementById("facturaCliente").textContent = `${factura.cliente.nombre} ${factura.cliente.apellido}`;
    document.getElementById("facturaFecha").textContent = factura.fecha;

    const facturaDetalleElement = document.getElementById("facturaDetalle");
    facturaDetalleElement.innerHTML = "";
    factura.detalleVenta.forEach(function(item) {
        const li = document.createElement("li");
        li.textContent = `${item.producto.descripcion} - Cantidad: ${item.cantidad} - Subtotal: ${item.subtotal.toFixed(2)}`;
        facturaDetalleElement.appendChild(li);
    });

    document.getElementById("facturaSubtotal").textContent = factura.subtotal.toFixed(2);
    document.getElementById("facturaDescuento").textContent = factura.descuento.toFixed(2);
    document.getElementById("facturaIVA").textContent = factura.iva.toFixed(2);
    document.getElementById("facturaTotal").textContent = factura.total.toFixed(2);

    facturaInfo.style.display = "block";
}

// Función para consultar una factura
function consultarFactura() {
    const selectFactura = document.getElementById("selectFactura");
    const numeroFactura = parseInt(selectFactura.value);

    const ventas = obtenerVentas();
    const factura = ventas.find(v => v.numeroFactura === numeroFactura);

    if (factura) {
        mostrarInformacionFactura(factura);
    } else {
        alert("Factura no encontrada");
    }
}

// Mostrar números de factura al cargar la página
document.addEventListener("DOMContentLoaded", function() {
    mostrarFacturasSelect();

    // Evento para botón consultar factura
    document.getElementById("btnConsultarFactura").addEventListener("click", consultarFactura);
});
