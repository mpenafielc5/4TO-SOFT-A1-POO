// Función para obtener todas las ventas del almacenamiento local
function obtenerVentas() {
    const ventasJSON = localStorage.getItem("ventas");
    return ventasJSON ? JSON.parse(ventasJSON) : [];
}

// Función para guardar todas las ventas en el almacenamiento local
function guardarVentas(ventas) {
    localStorage.setItem("ventas", JSON.stringify(ventas));
}

// Función para obtener todos los productos del almacenamiento local
function obtenerProductos() {
    const productosJSON = localStorage.getItem("productos");
    return productosJSON ? JSON.parse(productosJSON) : [];
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

// Función para mostrar los productos en el select
function mostrarProductosSelect() {
    const selectProducto = document.getElementById("selectProducto");
    const productos = obtenerProductos();
    productos.forEach(function(producto) {
        const option = document.createElement("option");
        option.value = producto.id;
        option.textContent = `${producto.descripcion} - Precio: ${producto.precio}`;
        selectProducto.appendChild(option);
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

// Función para agregar unidades a un producto en la factura
function agregarUnidades() {
    const selectFactura = document.getElementById("selectFactura");
    const numeroFactura = parseInt(selectFactura.value);

    const selectProducto = document.getElementById("selectProducto");
    const productoId = parseInt(selectProducto.value);
    const cantidadAdicional = parseInt(document.getElementById("cantidad").value);

    const ventas = obtenerVentas();
    const factura = ventas.find(v => v.numeroFactura === numeroFactura);
    const productos = obtenerProductos();
    const producto = productos.find(p => p.id === productoId);

    if (factura && producto) {
        const item = factura.detalleVenta.find(i => i.producto.id === productoId);
        if (item) {
            item.cantidad += cantidadAdicional;
            item.subtotal = item.producto.precio * item.cantidad;
        } else {
            alert("Producto no encontrado en la factura");
            return;
        }

        factura.subtotal = factura.detalleVenta.reduce((acc, item) => acc + item.subtotal, 0);
        factura.descuento = factura.subtotal * factura.cliente.descuento;
        factura.iva = (factura.subtotal - factura.descuento) * 0.12;
        factura.total = factura.subtotal - factura.descuento + factura.iva;

        mostrarInformacionFactura(factura);
        alert("Unidades agregadas correctamente");
    } else {
        alert("Factura o producto no encontrado");
    }
}

// Función para guardar los cambios en una factura
function guardarCambios() {
    const selectFactura = document.getElementById("selectFactura");
    const numeroFactura = parseInt(selectFactura.value);

    const ventas = obtenerVentas();
    const facturaIndex = ventas.findIndex(v => v.numeroFactura === numeroFactura);

    if (facturaIndex !== -1) {
        const factura = ventas[facturaIndex];

        // Actualizar la factura en el array de ventas
        ventas[facturaIndex] = factura;

        // Guardar las ventas actualizadas en el almacenamiento local
        guardarVentas(ventas);

        alert("Cambios guardados correctamente");
    } else {
        alert("Factura no encontrada");
    }
}

// Mostrar números de factura y productos al cargar la página
document.addEventListener("DOMContentLoaded", function() {
    mostrarFacturasSelect();
    mostrarProductosSelect();

    // Eventos para botones
    document.getElementById("btnConsultarFactura").addEventListener("click", consultarFactura);
    document.getElementById("btnAgregar").addEventListener("click", agregarUnidades);
    document.getElementById("btnGuardarCambios").addEventListener("click", guardarCambios);
});
