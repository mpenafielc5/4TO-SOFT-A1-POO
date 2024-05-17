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
        this.calcularDescuentoYCredito();
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


// Función para guardar un cliente en el almacenamiento local
function guardarCliente(cliente) {
    const clientes = obtenerClientes();
    clientes.push(cliente);
    localStorage.setItem("clientes", JSON.stringify(clientes));
}

// Función para obtener todos los clientes del almacenamiento local
function obtenerClientes() {
    const clientesJSON = localStorage.getItem("clientes");
    return clientesJSON ? JSON.parse(clientesJSON) : [];
}

// Función para validar la cédula
function cedulaValida(cedula) {
    if (cedula.length !== 10) {
        return false;
    }
    
    const provincia = parseInt(cedula.substring(0, 2));
    if (provincia < 1 || provincia > 24) {
        return false;
    }

    const coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2];
    const digitos = cedula.split('').map(Number);
    const digitoVerificador = digitos.pop();

    let suma = 0;
    for (let i = 0; i < digitos.length; i++) {
        let valor = digitos[i] * coeficientes[i];
        if (valor >= 10) {
            valor -= 9;
        }
        suma += valor;
    }

    const calculado = (10 - (suma % 10)) % 10;
    return calculado === digitoVerificador;
}

let contadorClientes = localStorage.getItem('contadorClientes') ? parseInt(localStorage.getItem('contadorClientes')) : 1;

// Manejo del formulario de creación de clientes
document.addEventListener("DOMContentLoaded", function() {
    // Cargar clientes almacenados al cargar la página
    cargarClientes();

    document.getElementById("clienteForm").addEventListener("submit", function(event) {
        event.preventDefault(); // Evita que se envíe el formulario
        
        const cedula = document.getElementById("cedula").value;
        const nombre = document.getElementById("nombre").value;
        const apellido = document.getElementById("apellido").value;
        const tipoCliente = document.querySelector('input[name="tipoCliente"]:checked').value;
        const tarjeta = document.querySelector('input[name="tarjeta"]:checked').value;

        if (!cedulaValida(cedula)) {
            alert("Error: La cédula ingresada no es válida");
            return;
        }

        const nuevoCliente = new Cliente(
            contadorClientes++,
            cedula,
            nombre,
            apellido,
            tipoCliente,
            tarjeta === "si"
        );

        console.log("Nuevo Cliente:");
        console.log(nuevoCliente);

        guardarCliente(nuevoCliente);

        alert("Datos Guardados");

        document.getElementById("clienteForm").reset();
    });
});

// Función para cargar clientes almacenados del localStorage
function cargarClientes() {
    const clientes = obtenerClientes();
    clientes.forEach(function(cliente) {
        // Aquí puedes hacer lo que quieras con los datos del cliente, como agregarlos a una lista o una tabla en tu página
        console.log(cliente);
    });
}
