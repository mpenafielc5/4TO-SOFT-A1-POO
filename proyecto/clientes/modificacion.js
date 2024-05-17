// Definición de la clase Cliente
class Cliente {
    constructor(id, cedula, nombre, apellido, tipoCliente, tieneTarjeta) {
        this.id = id;
        this.cedula = cedula;
        this.nombre = nombre;
        this.apellido = apellido;
        this.tipoCliente = tipoCliente;
        this.tieneTarjeta = tieneTarjeta;
        this.descuento = 0;
        this.credito = 0;
        this.calcularDescuentoYCredito(); // Llamada al método para calcular descuento y crédito al crear una instancia de Cliente
    }

    calcularDescuentoYCredito() {
        if (this.tipoCliente === "regular") {
            if (this.tieneTarjeta) {
                this.descuento = 0.1;
                this.credito = 0;
            } else {
                this.descuento = 0;
                this.credito = 0;
            }
        } else if (this.tipoCliente === "vip") {
            if (this.tieneTarjeta) {
                this.descuento = 0.1;
                this.credito = 10000;
            } else {
                this.descuento = 0;
                this.credito = 10000;
            }
        }
    }
}

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

// Manejo del formulario de modificación de clientes
document.addEventListener("DOMContentLoaded", function() {
    const modificacionForm = document.getElementById("modificacionForm");
    const formularioModificacion = document.getElementById("formularioModificacion");
    const resultadoModificacion = document.getElementById("resultadoModificacion");

    modificacionForm.addEventListener("submit", function(event) {
        event.preventDefault(); // Evita que se envíe el formulario
        
        const cedulaConsulta = document.getElementById("modificacionCedula").value;

        const clienteEncontrado = buscarClientePorCedula(cedulaConsulta);

        if (clienteEncontrado) {
            formularioModificacion.style.display = "block"; // Mostrar el formulario de modificación
            resultadoModificacion.innerHTML = ""; // Limpiar el área de resultados
            // Llenar el formulario de modificación con los datos del cliente encontrado
            document.getElementById("modificacionNombre").value = clienteEncontrado.nombre;
            document.getElementById("modificacionApellido").value = clienteEncontrado.apellido;
            document.querySelector('input[name="modificacionTipoCliente"][value="' + clienteEncontrado.tipoCliente + '"]').checked = true;
            document.querySelector('input[name="modificacionTarjeta"][value="' + (clienteEncontrado.tieneTarjeta ? "si" : "no") + '"]').checked = true;
        } else {
            resultadoModificacion.innerHTML = "<p>No se encontró un cliente con esa cédula.</p>";
            formularioModificacion.style.display = "none"; // Ocultar el formulario de modificación
        }
    });

    const formularioModificar = document.getElementById("formularioModificar");

    formularioModificar.addEventListener("submit", function(event) {
        event.preventDefault(); // Evita que se envíe el formulario
    
        const cedulaConsulta = document.getElementById("modificacionCedula").value;
    
        const clientes = obtenerClientes();
        const clienteIndex = clientes.findIndex(cliente => cliente.cedula === cedulaConsulta);
    
        if (clienteIndex !== -1) {
            // Actualizar los datos del cliente
            clientes[clienteIndex].nombre = document.getElementById("modificacionNombre").value;
            clientes[clienteIndex].apellido = document.getElementById("modificacionApellido").value;
            clientes[clienteIndex].tipoCliente = document.querySelector('input[name="modificacionTipoCliente"]:checked').value;
            clientes[clienteIndex].tieneTarjeta = document.querySelector('input[name="modificacionTarjeta"]:checked').value === "si";
    
            // Crear una instancia del cliente actualizado
            const clienteActualizado = new Cliente(
                clientes[clienteIndex].id,
                clientes[clienteIndex].cedula,
                clientes[clienteIndex].nombre,
                clientes[clienteIndex].apellido,
                clientes[clienteIndex].tipoCliente,
                clientes[clienteIndex].tieneTarjeta
            );
    
            // Calcular descuento y crédito para el cliente actualizado
            clienteActualizado.calcularDescuentoYCredito();
    
            // Actualizar el cliente en el arreglo
            clientes[clienteIndex] = clienteActualizado;
    
            // Guardar los cambios en el almacenamiento local
            localStorage.setItem("clientes", JSON.stringify(clientes));
    
            resultadoModificacion.innerHTML = "<p>Los cambios se han guardado correctamente.</p>";
        } else {
            resultadoModificacion.innerHTML = "<p>No se pudo encontrar al cliente para realizar la modificación.</p>";
        }
    });
});
