// Función para obtener todos los clientes del almacenamiento local
function obtenerClientes() {
    const clientesJSON = localStorage.getItem("clientes");
    return clientesJSON ? JSON.parse(clientesJSON) : [];
}

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

// Función para guardar una venta en el almacenamiento local
function guardarVenta(venta) {
    const ventas = obtenerVentas();
    ventas.push(venta);
    localStorage.setItem("ventas", JSON.stringify(ventas));
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

// Función para buscar un cliente por cédula
function buscarClientePorCedula(cedula) {
    const clientes = obtenerClientes();
    return clientes.find(cliente => cliente.cedula === cedula);
}

// Función para mostrar la información del cliente
function mostrarInformacionCliente(cliente) {
    const clienteInfo = document.getElementById("clienteInfo");
    const clienteNombre = document.getElementById("clienteNombre");
    clienteNombre.textContent = `${cliente.nombre} ${cliente.apellido}`;
    clienteInfo.style.display = "block";
}

// Función para agregar un producto al detalle de venta
function agregarProducto() {
    const selectProducto = document.getElementById("selectProducto");
    const productoId = parseInt(selectProducto.value);
    const cantidad = parseInt(document.getElementById("cantidad").value);

    const productos = obtenerProductos();
    const producto = productos.find(p => p.id === productoId);

    if (producto) {
        if (producto.stock >= cantidad) {
            const subtotal = producto.precio * cantidad;
            const detalle = { producto, cantidad, subtotal };
            ventaActual.detalleVenta.push(detalle);
            actualizarDetalleVenta();
        } else {
            alert("No hay suficiente stock de este producto");
        }
    } else {
        alert("Producto no encontrado");
    }
}

// Función para actualizar el detalle de venta en la página
function actualizarDetalleVenta() {
    const detalleVentaElement = document.getElementById("detalleVenta");
    detalleVentaElement.innerHTML = "";

    ventaActual.subtotal = 0;

    ventaActual.detalleVenta.forEach(function(item) {
        const li = document.createElement("li");
        li.textContent = `${item.producto.descripcion} - Cantidad: ${item.cantidad} - Subtotal: ${item.subtotal.toFixed(2)}`;
        detalleVentaElement.appendChild(li);
        ventaActual.subtotal += item.subtotal;
    });

    const iva = ventaActual.subtotal * 0.12;
    const total = ventaActual.subtotal + iva;

    const subtotalElement = document.createElement("li");
    subtotalElement.textContent = `Subtotal: ${ventaActual.subtotal.toFixed(2)}`;
    detalleVentaElement.appendChild(subtotalElement);

    const ivaElement = document.createElement("li");
    ivaElement.textContent = `IVA (12%): ${iva.toFixed(2)}`;
    detalleVentaElement.appendChild(ivaElement);

    const totalElement = document.createElement("li");
    totalElement.textContent = `Total: ${total.toFixed(2)}`;
    detalleVentaElement.appendChild(totalElement);
}

// Función para registrar la venta
function registrarVenta() {
    if (ventaActual.detalleVenta.length === 0) {
        alert("No hay productos en la venta");
        return;
    }

    const clienteId = ventaActual.cliente.id;
    const clientes = obtenerClientes();
    const cliente = clientes.find(c => c.id === clienteId);

    if (!cliente) {
        alert("Cliente no encontrado");
        return;
    }

    // Calcular el descuento
    const descuento = ventaActual.subtotal * cliente.descuento;
    const subtotalConDescuento = ventaActual.subtotal - descuento;
    const iva = subtotalConDescuento * 0.12;
    const total = subtotalConDescuento + iva;
    

    // Asignar número de factura
    const ventas = obtenerVentas();
    const numeroFactura = ventas.length + 1;

    // Crear la venta
    const venta = {
        numeroFactura,
        cliente,
        detalleVenta: ventaActual.detalleVenta, 
        subtotal: ventaActual.subtotal,
        descuento,
        iva,
        total,
        fecha: new Date().toLocaleString()
    };

    // Guardar la venta
    guardarVenta(venta);

    // Obtener los productos
    const productos = obtenerProductos();

    // Actualizar el stock de los productos
    ventaActual.detalleVenta.forEach(function(item) {
        const producto = productos.find(p => p.id === item.producto.id);
        if (producto) {
            producto.stock -= item.cantidad;
        }
    });

    // Guardar los productos actualizados
    localStorage.setItem("productos", JSON.stringify(productos));

    alert(`Venta registrada exitosamente. Número de factura: ${numeroFactura}`);

    // Reiniciar venta actual
    ventaActual = { cliente: null, detalleVenta: [], subtotal: 0 };
    document.getElementById("clienteInfo").style.display = "none";
    actualizarDetalleVenta();

    // Resetear el formulario
    document.getElementById("formVenta").reset();
}

// Variable para almacenar la venta actual en proceso
let ventaActual = {
    cliente: null,
    detalleVenta: [],
    subtotal: 0
};

// Mostrar productos al cargar la página
document.addEventListener("DOMContentLoaded", function() {
    mostrarProductosSelect();

    // Evento para buscar cliente por cédula
    document.getElementById("btnBuscarCliente").addEventListener("click", function() {
        const cedulaCliente = document.getElementById("cedulaCliente").value;
        const cliente = buscarClientePorCedula(cedulaCliente);
        if (cliente) {
            ventaActual.cliente = cliente;
            mostrarInformacionCliente(cliente);
        } else {
            alert("Cliente no encontrado");
        }
    });

    // Eventos para botones
    document.getElementById("btnAgregar").addEventListener("click", agregarProducto);
    document.getElementById("btnRegistrarVenta").addEventListener("click", registrarVenta);
});
