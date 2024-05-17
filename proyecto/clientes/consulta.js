// Función para obtener todos los clientes del almacenamiento local
function obtenerClientes() {
    const clientesJSON = localStorage.getItem("clientes");
    return clientesJSON ? JSON.parse(clientesJSON) : [];
}

// Función para buscar un cliente por cédula
function buscarClientePorCedula(cedula) {
    const clientes = obtenerClientes();
    return clientes.find(cliente => cliente.cedula === cedula);
}

// Manejo del formulario de consulta de clientes
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("consultaForm").addEventListener("submit", function(event) {
        event.preventDefault(); // Evita que se envíe el formulario
        
        const cedulaConsulta = document.getElementById("consultaCedula").value;

        const clienteEncontrado = buscarClientePorCedula(cedulaConsulta);

        const resultadoConsulta = document.getElementById("resultadoConsulta");

        if (clienteEncontrado) {
            resultadoConsulta.innerHTML = `
                <p>ID: ${clienteEncontrado.id}</p>
                <p>Cédula: ${clienteEncontrado.cedula}</p>
                <p>Nombre: ${clienteEncontrado.nombre}</p>
                <p>Apellido: ${clienteEncontrado.apellido}</p>
                <p>Tipo de Cliente: ${clienteEncontrado.tipoCliente}</p>
                <p>Tiene Tarjeta: ${clienteEncontrado.tieneTarjeta ? "Sí" : "No"}</p>
                <p>Credito disponible: ${clienteEncontrado.credito}</p>
                <p>Descuento: ${clienteEncontrado.descuento}</p>
            `;
        } else {
            resultadoConsulta.innerHTML = "<p>No se encontró un cliente con esa cédula.</p>";
        }
    });
});
