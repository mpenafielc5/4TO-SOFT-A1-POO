// Función para eliminar un cliente por su número de cédula
function eliminarClientePorCedula(cedula) {
    console.log("Cédula recibida para eliminar:", cedula); // Mostrar la cédula recibida en la consola
    let clientes = obtenerClientes();
    const clienteIndex = clientes.findIndex(cliente => cliente.cedula === cedula);
    console.log("Índice del cliente a eliminar:", clienteIndex); // Mostrar el índice del cliente a eliminar en la consola
    if (clienteIndex !== -1) {
        clientes.splice(clienteIndex, 1); // Eliminar el cliente del arreglo
        localStorage.setItem("clientes", JSON.stringify(clientes)); // Actualizar el almacenamiento local
        return true; // Cliente eliminado con éxito
    }
    return false; // Cliente no encontrado o no eliminado
}
