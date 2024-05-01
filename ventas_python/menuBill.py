from components import Menu,Valida
from utilities import borrarPantalla,gotoxy
from utilities import reset_color,red_color,green_color,blue_color,purple_color
from clsJson import JsonFile
from company  import Company
from customer import RegularClient
from sales import Sale
from product  import Product
from iCrud import ICrud
import datetime
import time,os
from functools import reduce
import re
from tabulate import tabulate
from colorama import init, Fore, Style

# Definimos la función para borrar la pantalla
def borrarPantalla():
    print("\033c", end="")

# Inicializamos colorama
init()
path, _ = os.path.split(os.path.abspath(__file__))
# Procesos de las Opciones del Menu Facturacion
class CrudClients(ICrud):
    def create(self):
        borrarPantalla()
        validar = Valida()
        ClientDictionary = {
            "dni": "",
            "nombre": "",
            "apellido": "",
            "tipo_cliente": "",  # Agregamos el campo 'tipo_cliente' al diccionario
            "valor": ""
        }
        print(Fore.BLUE + "Ingrese los datos del cliente:" + Fore.RESET)

        while True:
            while True:
                dni = input("Cédula: ")
                try:
                    if validar.cedula_valida(dni):
                        json_file = JsonFile(path+'/archivos/clients.json')
                        clientes = json_file.read()
                        dni_existente = any(cliente["dni"] == dni for cliente in clientes)
                        if dni_existente:
                            print(Fore.RED + "La cédula ingresada ya existe. Inténtelo de nuevo." + Fore.RESET)
                        else:
                            ClientDictionary["dni"] = dni
                            break
                    else:
                        raise ValueError("La cédula ingresada no es válida.")
                except Exception as e:
                    print(Fore.RED + str(e) + Fore.RESET)
                    continuar = input("Si desea intentar de nuevo escriba SI ").lower()
                    if continuar != 'si':
                        return  # Regresar si el usuario no desea intentarlo de nuevo

            while True:
                nombre = input("Nombre: ").upper()
                if nombre.isalpha():
                    ClientDictionary["nombre"] = nombre
                    break
                else:
                    print(Fore.RED + "El nombre debe contener solo letras. Inténtelo de nuevo." + Fore.RESET)

            while True:
                apellido = input("Apellido: ").upper()
                if apellido.isalpha():
                    ClientDictionary["apellido"] = apellido
                    break
                else:
                    print(Fore.RED + "El apellido debe contener solo letras. Inténtelo de nuevo." + Fore.RESET)

            tipo_cliente = input("¿Es el cliente Regular o VIP? ").lower()
            if tipo_cliente == "regular":
                tiene_tarjeta = input("¿Tiene tarjeta? (Si/No): ").lower()
                if tiene_tarjeta == "si":
                    ClientDictionary["tipo_cliente"] = "Regular con tarjeta"  # Asignamos el tipo de cliente
                    ClientDictionary["valor"] = "0"
                    break  # Salir del bucle si el cliente es regular y tiene tarjeta
                else:
                    ClientDictionary["tipo_cliente"] = "Regular"  # Asignamos el tipo de cliente
                    ClientDictionary["valor"] = "0"
                    break
            elif tipo_cliente == "vip":
                ClientDictionary["tipo_cliente"] = "VIP"  # Asignamos el tipo de cliente
                ClientDictionary["valor"] = "10000"
                break  # Salir del bucle si el cliente es VIP
            else:
                print(Fore.RED + "Opción no válida. Por favor, introduzca Regular o VIP." + Fore.RESET)
                return

        clientes.append(ClientDictionary)
        json_file.save(clientes)

    def update(self):
            borrarPantalla()
            dni_a_actualizar = input(Fore.BLUE + "Ingrese la cédula del cliente que desea actualizar: " + Fore.RESET)
            json_file = JsonFile(path+'/archivos/clients.json')
            clientes = json_file.read()
            cliente_encontrado = None
            
            for cliente in clientes:
                if cliente["dni"] == dni_a_actualizar:
                    cliente_encontrado = cliente
                    break
            
            if cliente_encontrado:
                data = [
                    [Fore.MAGENTA + "Cédula:" + Style.RESET_ALL, cliente_encontrado['dni']],
                    [Fore.MAGENTA + "Nombre:" + Style.RESET_ALL, cliente_encontrado['nombre']],
                    [Fore.MAGENTA + "Apellido:" + Style.RESET_ALL, cliente_encontrado['apellido']],
                    [Fore.MAGENTA + "Cupo Disponible:" + Style.RESET_ALL, cliente_encontrado['valor']]
                ]
                
                print(tabulate(data, tablefmt="fancy_grid"))

                tipo_cliente = cliente_encontrado.get('tipo_cliente', '').lower()

                if tipo_cliente == "regular" or tipo_cliente == "regular con tarjeta":
                    print(Fore.MAGENTA + "Tipo de cliente: Regular" + Style.RESET_ALL)
                elif tipo_cliente == "vip":
                    print(Fore.MAGENTA + "Tipo de cliente: VIP" + Style.RESET_ALL)

                confirmacion = input(Fore.YELLOW + f"¿Desea actualizar los datos del cliente {cliente_encontrado['nombre']} {cliente_encontrado['apellido']}? (si/no): " + Fore.RESET)
                if confirmacion.lower() == "si":
                    nuevo_nombre = input(Fore.BLUE + "Ingrese el nuevo nombre: " + Fore.RESET).upper().replace(" ", "")[:15]  # Eliminar espacios y truncar
                    if any(char.isdigit() for char in nuevo_nombre):
                        print(Fore.RED + "Error: El nombre no puede contener números." + Fore.RESET)
                    else:
                        nuevo_apellido = input(Fore.BLUE + "Ingrese el nuevo apellido: " + Fore.RESET).upper().replace(" ", "")[:15]  # Eliminar espacios y truncar
                        if any(char.isdigit() for char in nuevo_apellido):
                            print(Fore.RED + "Error: El apellido no puede contener números." + Fore.RESET)
                        else:
                            cliente_encontrado["nombre"] = nuevo_nombre
                            cliente_encontrado["apellido"] = nuevo_apellido

                            json_file.save(clientes)
                            print(Fore.GREEN + "Nombre y apellido del cliente actualizados exitosamente." + Fore.RESET)
                else:
                    print(Fore.YELLOW + "Operación cancelada. No se actualizaron los datos del cliente." + Fore.RESET)
            else:
                print(Fore.RED + "Cliente no encontrado. No se pueden actualizar los datos." + Fore.RESET)

    def delete(self):
        borrarPantalla()
        dni_a_eliminar = input(Fore.BLUE + "Ingrese la cédula del cliente que desea eliminar: " + Fore.RESET)
        json_file = JsonFile(path+'/archivos/clients.json')
        clientes = json_file.read()
        
        cliente_encontrado = None
        for cliente in clientes:
            if cliente["dni"] == dni_a_eliminar:
                cliente_encontrado = cliente
                break
        
        if cliente_encontrado:
            print(Fore.BLUE + "\nDatos del cliente a eliminar:" + Fore.RESET)
            data = [
                [Fore.MAGENTA + "Cédula:" + Style.RESET_ALL, cliente_encontrado['dni']],
                [Fore.MAGENTA + "Nombre:" + Style.RESET_ALL, cliente_encontrado['nombre']],
                [Fore.MAGENTA + "Apellido:" + Style.RESET_ALL, cliente_encontrado['apellido']],
                [Fore.MAGENTA + "Cupo Disponible:" + Style.RESET_ALL, cliente_encontrado['valor']]
            ]
            print(tabulate(data, tablefmt="fancy_grid"))
            
            tipo_cliente = cliente_encontrado.get('tipo_cliente', '').lower()

            if tipo_cliente == "regular" or tipo_cliente == "regular con tarjeta":
                print(Fore.MAGENTA + "Tipo de cliente: Regular" + Style.RESET_ALL)
            elif tipo_cliente == "vip":
                print(Fore.MAGENTA + "Tipo de cliente: VIP" + Style.RESET_ALL)
            
            confirmacion = input(Fore.YELLOW + "¿Está seguro de que desea eliminar los datos del cliente? Escriba SI para confirmar: " + Fore.RESET)
            if confirmacion.lower() == 'si':
                clientes.remove(cliente_encontrado)
                json_file.save(clientes)
                print(Fore.GREEN + "Cliente eliminado correctamente." + Fore.RESET)
            else:
                print(Fore.YELLOW + "Operación cancelada. Los datos del cliente no han sido eliminados." + Fore.RESET)
        else:
            print(Fore.RED + "Cliente no encontrado. No se puede eliminar." + Fore.RESET)

    def consult(self, clientes=None):
        borrarPantalla()
        consultOptionInput = input("¿Va a hacer una: 1) Consulta general  o  2) Específica?: ")

        # Verificar si la entrada está vacía
        if not consultOptionInput:
            return

        consultOption = int(consultOptionInput)

        if consultOption == 1:
            print(Fore.BLUE + "Realizando consulta general" + Fore.RESET)
            if clientes is None:
                json_file = JsonFile(path+'/archivos/clients.json')
                clientes = json_file.read()

            if clientes:
                borrarPantalla()
                print(Fore.BLUE + "\nDatos de todos los clientes:" + Fore.RESET)
                print(Fore.CYAN + "Cédula        Nombre         Apellido       Cupo Disponible  Tipo" + Fore.RESET)
                print(Fore.CYAN + "────────────────────────────────────────────────────────────────────" + Fore.RESET)

                # Definir función interna para contar clientes recursivamente
                def count_clientes(clientes):
                    if not clientes:
                        return 0
                    return 1 + count_clientes(clientes[1:])

                total_clientes = count_clientes(clientes)

                for cliente in clientes:
                    cedula = cliente['dni'] + ' ' * (12 - len(cliente['dni']))
                    nombre = cliente['nombre'] + ' ' * (14 - len(cliente['nombre']))
                    apellido = cliente['apellido'] + ' ' * (13 - len(cliente['apellido']))
                    cupo_disponible = cliente['valor'] + ' ' * (16 - len(cliente['valor']))
                    tipo_cliente = cliente.get('tipo_cliente', '').lower()
                    if tipo_cliente == "regular" or tipo_cliente == "regular con tarjeta":
                        tipo_cliente_print = "Regular"
                    elif tipo_cliente == "vip":
                        tipo_cliente_print = "VIP"
                    else:
                        tipo_cliente_print = ""
                    tipo_cliente_color = Fore.YELLOW if tipo_cliente_print == 'VIP' else Fore.BLUE
                    print(Fore.MAGENTA + f"{cedula}{nombre}{apellido}{cupo_disponible}" + tipo_cliente_color + f"{tipo_cliente_print}" + Fore.RESET)
                print(Fore.CYAN + "────────────────────────────────────────────────────────────────────" + Fore.RESET)

                # Encontrar el cliente con el mayor cupo disponible
                cliente_mayor_cupo = max(clientes, key=lambda x: float(x['valor']))
                mayor_cupo_disponible = cliente_mayor_cupo['valor']

                # Encontrar el cliente con el menor cupo disponible
                cliente_menor_cupo = min(clientes, key=lambda x: float(x['valor']))
                menor_cupo_disponible = cliente_menor_cupo['valor']

                # Mostrar resultados
                print("Cliente con el mayor cupo disponible:", cliente_mayor_cupo['nombre'], cliente_mayor_cupo['apellido'])
                print("Cupo disponible:", mayor_cupo_disponible)

                print("Cliente con el menor cupo disponible:", cliente_menor_cupo['nombre'], cliente_menor_cupo['apellido'])
                print("Cupo disponible:", menor_cupo_disponible)

                # Mostrar total de clientes
                print("Total de clientes:", total_clientes)

            else:
                borrarPantalla()
                print(Fore.YELLOW + "No hay clientes registrados." + Fore.RESET)
        elif consultOption == 2:
            dni_a_consultar = input("Ingrese la cédula del cliente que desea consultar: ")
            if clientes is None:
                json_file = JsonFile(path+'/archivos/clients.json')
                clientes = json_file.read()

            cliente_encontrado = None
            for cliente in clientes:
                if cliente["dni"] == dni_a_consultar:
                    cliente_encontrado = cliente
                    break

            if cliente_encontrado:
                borrarPantalla()
                print(Fore.BLUE + "\nDatos del cliente:" + Fore.RESET)
                data = [
                    [Fore.MAGENTA + "Cédula:" + Style.RESET_ALL, cliente_encontrado['dni']],
                    [Fore.MAGENTA + "Nombre:" + Style.RESET_ALL, cliente_encontrado['nombre']],
                    [Fore.MAGENTA + "Apellido:" + Style.RESET_ALL, cliente_encontrado['apellido']],
                    [Fore.MAGENTA + "Cupo Disponible:" + Style.RESET_ALL, cliente_encontrado['valor']]
                ]
                print(tabulate(data, tablefmt="fancy_grid"))

                tipo_cliente = cliente_encontrado.get('tipo_cliente', '').lower()

                if tipo_cliente == "regular" or tipo_cliente == "regular con tarjeta":
                    print(Fore.MAGENTA + "Tipo de cliente: Regular" + Style.RESET_ALL)
                elif tipo_cliente == "vip":
                    print(Fore.MAGENTA + "Tipo de cliente: VIP" + Style.RESET_ALL)
            else:
                x = input("Cliente no encontrado. De click para continuar...")
        else:
            print("Opción no válida. Vuelva a intentarlo...")

class CrudProducts(ICrud):
    def create(self):
        borrarPantalla()
        # Leer el json de los productos
        json_file = JsonFile(path+'/archivos/products.json')
        products = json_file.read()

        # Obtener el último id
        lastId = 0
        for product in products:
            if int(product["id"]) > lastId:
                lastId = int(product["id"])
            
        # Incrementar el último ID en uno para obtener el siguiente ID
        nextId = lastId + 1

        # Solicitar al usuario que ingrese los datos del nuevo producto
        while True:
            descripcion = input("Descripción del producto: ").upper()  # Convertir la descripción a mayúsculas automáticamente
            if descripcion.strip() == "":
                borrarPantalla()
                print(Fore.RED + "La descripción no puede estar en blanco. Por favor, ingrese una descripción válida." + Fore.RESET)
                continue
            elif any(char.isdigit() for char in descripcion):
                confirmacion = input("La descripción no puede contener números. ¿Desea intentarlo de nuevo? (SI/NO): ").lower()
                if confirmacion == 'no':
                    return
                else:
                    continue
            else:
                break

        # Validar y solicitar el precio del producto
        while True:
            precio = input("Precio del producto: ")
            if re.match(r'^\d+(\.\d+)?$', precio):
                precio = float(precio)
                break
            else:
                print(Fore.RED + "El precio debe ser un número entero o decimal." + Fore.RESET)

        # Validar y solicitar el stock del producto
        while True:
            stock = input("Stock del producto: ")
            if stock.isdigit():
                stock = int(stock)
                break
            else:
                print(Fore.RED + "El stock debe ser un número entero." + Fore.RESET)

        ProductDictionary = {
            "id": nextId,
            "descripcion": descripcion,
            "precio": precio,
            "stock": stock
        }
        products.append(ProductDictionary)
        json_file.save(products)
        print(Fore.GREEN + "¡Producto agregado exitosamente!" + Fore.RESET)


    def update(self):
        borrarPantalla()
        # Leer el JSON de los productos
        json_file = JsonFile(path+'/archivos/products.json')
        products = json_file.read()

        # Solicitar al usuario que ingrese el ID del producto a actualizar
        while True:
            product_id = input(Fore.BLUE + "Ingrese el ID del producto que desea actualizar: " + Fore.RESET)
            if product_id.isdigit():
                product_id = int(product_id)
                break
            else:
                print(Fore.RED + "El ID debe ser un número entero." + Fore.RESET)

        # Buscar el producto por su ID
        product_to_update = None
        for product in products:
            if int(product["id"]) == product_id:
                product_to_update = product
                break

        if product_to_update is not None:
            # Presentar los datos actuales del producto
            current_data = [
                [Fore.MAGENTA + "ID:" + Style.RESET_ALL, product_to_update["id"]],
                [Fore.MAGENTA + "Descripción:" + Style.RESET_ALL, product_to_update["descripcion"]],
                [Fore.MAGENTA + "Precio:" + Style.RESET_ALL, product_to_update["precio"]],
                [Fore.MAGENTA + "Stock:" + Style.RESET_ALL, product_to_update["stock"]]
            ]
            print(Fore.CYAN + "Datos actuales del producto:" + Fore.RESET)
            print(tabulate(current_data, tablefmt="fancy_grid"))

            # Confirmar si el usuario desea actualizar el producto
            confirmacion = input(Fore.YELLOW + "¿Desea actualizar este producto? (SI/NO): " + Fore.RESET).lower()
            if confirmacion == 'si':
                # Solicitar la nueva descripción del producto
                while True:
                    new_description = input("Ingrese la nueva descripción del producto: ").strip().upper()  # Convertir la descripción a mayúsculas automáticamente
                    # Verificar si la descripción está en blanco o contiene números
                    if not new_description:
                        print(Fore.RED + "La descripción no puede estar en blanco. Por favor, ingrese una descripción válida." + Fore.RESET)
                    elif any(char.isdigit() for char in new_description):
                        print(Fore.RED + "La descripción no puede contener números. Por favor, ingrese una descripción válida." + Fore.RESET)
                    else:
                        # Verificar si la nueva descripción ya está siendo utilizada
                        if any(product["descripcion"] == new_description for product in products if product["id"] != product_id):
                            print(Fore.RED + "La descripción ingresada ya está en uso por otro producto. Por favor, ingrese una descripción diferente." + Fore.RESET)
                        else:
                            break

                # Solicitar el nuevo precio del producto
                while True:
                    new_price = input("Ingrese el nuevo precio del producto: ")
                    if re.match(r'^\d+(\.\d+)?$', new_price):
                        new_price = float(new_price)
                        break
                    else:
                        print(Fore.RED + "El precio debe ser un número entero o decimal." + Fore.RESET)

                # Solicitar el nuevo stock del producto
                while True:
                    new_stock = input("Ingrese el nuevo stock del producto: ")
                    if new_stock.isdigit():
                        new_stock = int(new_stock)
                        break
                    else:
                        print(Fore.RED + "El stock debe ser un número entero." + Fore.RESET)

                # Actualizar la descripción, precio y stock del producto
                product_to_update["descripcion"] = new_description
                product_to_update["precio"] = new_price
                product_to_update["stock"] = new_stock
                json_file.save(products)
                print(Fore.GREEN + "¡Producto actualizado exitosamente!" + Fore.RESET)
            elif confirmacion == 'no':
                print("Operación cancelada. No se han realizado cambios en el producto.")
            else:
                print(Fore.RED + "Respuesta no válida. Por favor, ingrese 'SI' o 'NO'." + Fore.RESET)
        else:
            print(Fore.RED + "No se encontró ningún producto con el ID especificado." + Fore.RESET)


    def delete(self):
        borrarPantalla()
        # Leer el JSON de los productos
        json_file = JsonFile(path+'/archivos/products.json')
        products = json_file.read()

        # Solicitar al usuario que ingrese el ID del producto a eliminar
        while True:
            product_id = input("Ingrese el ID del producto que desea eliminar: ")
            if product_id.isdigit():
                product_id = int(product_id)
                break
            else:
                print("El ID debe ser un número entero.")

        # Buscar el producto por su ID y mostrar su descripción
        product_to_delete = None
        for product in products:
            if int(product["id"]) == product_id:
                product_to_delete = product
                # Mostrar los datos del producto a eliminar
                current_data = [
                    [Fore.MAGENTA + "ID:" + Style.RESET_ALL, product_to_delete["id"]],
                    [Fore.MAGENTA + "Descripción:" + Style.RESET_ALL, product_to_delete["descripcion"]],
                    [Fore.MAGENTA + "Precio:" + Style.RESET_ALL, product_to_delete["precio"]],
                    [Fore.MAGENTA + "Stock:" + Style.RESET_ALL, product_to_delete["stock"]]
                ]
                print(Fore.CYAN + "Datos del producto a eliminar:" + Fore.RESET)
                print(tabulate(current_data, tablefmt="fancy_grid"))
                break

        if product_to_delete is not None:
            # Confirmar la eliminación con el usuario
            confirmacion = input("¿Estás seguro de que quieres eliminar este producto? (SI/NO): ").lower()
            if confirmacion == 'si':
                products.remove(product_to_delete)
                json_file.save(products)
                print("¡Producto eliminado exitosamente!")
                input("Presione una tecla para salir...")
            else:
                print("Eliminación cancelada.")
                input("Presione una tecla para salir...")
        else:
            print("No se encontró ningún producto con el ID especificado.")
            input("Presione una tecla para salir...")

    
    def consult(self):
        while True:
            borrarPantalla()
            # Leer el JSON de los productos
            json_file = JsonFile(path+'/archivos/products.json')
            products = json_file.read()

            consult_option = None

            while consult_option not in ['1', '2']:
                consult_option = input("¿Va a hacer una: 1) Consulta general  o  2) Específica?: ")

                if consult_option == '1':
                    if not products:
                        print("No hay productos disponibles.")
                        retry = input("¿Desea intentar de nuevo? (si/no): ").lower()
                        if retry == "si":
                            break
                        elif retry == "no":
                            return
                        else:
                            print("Respuesta no válida. Por favor, ingrese 'si' o 'no'.")
                        continue
                    else:
                        print(Fore.BLUE + "\nDatos de todos los productos:" + Fore.RESET)
                        print(Fore.CYAN + "ID        Descripción               Precio    Stock" + Fore.RESET)
                        print(Fore.CYAN + "─────────────────────────────────────────────────────" + Fore.RESET)
                        for product in products:
                            print(Fore.MAGENTA + f"{product['id']:8} {product['descripcion'][:22]:<25} {product['precio']:8} {product['stock']:6}" + Fore.RESET)
                                            # Encontrar el producto más caro y el más barato
                        max_price_product = max(products, key=lambda x: x["precio"])
                        min_price_product = min(products, key=lambda x: x["precio"])

                        # Encontrar el producto con mayor y menor stock
                        max_stock_product = max(products, key=lambda x: x["stock"])
                        min_stock_product = min(products, key=lambda x: x["stock"])

                        print("\nProducto más caro:", max_price_product["descripcion"])
                        print("Producto más barato:", min_price_product["descripcion"])
                        print("Producto con mayor stock:", max_stock_product["descripcion"])
                        print("Producto con menor stock:", min_stock_product["descripcion"])
                        return
                elif consult_option == '2':
                    product_id_to_consult = input("Ingrese el ID del producto que desea consultar: ")

                    if not product_id_to_consult.isdigit():
                        print("El ID debe ser un número entero.")
                        retry = input("¿Desea intentar de nuevo? (si/no): ").lower()
                        if retry == "si":
                            break
                        elif retry == "no":
                            x=input("Presione cualquier tecla...")
                            return
                        else:
                            print("Respuesta no válida. Por favor, ingrese 'si' o 'no'.")
                        continue

                    product_id_to_consult = int(product_id_to_consult)

                    product_found = None
                    for product in products:
                        if product["id"] == product_id_to_consult:
                            product_found = product
                            break

                    if product_found:
                        borrarPantalla()
                        print("Datos del producto:")
                        data = [
                            [Fore.MAGENTA + "ID:" + Style.RESET_ALL, product_found['id']],
                            [Fore.MAGENTA + "Descripción:" + Style.RESET_ALL, product_found['descripcion']],
                            [Fore.MAGENTA + "Precio:" + Style.RESET_ALL, product_found['precio']],
                            [Fore.MAGENTA + "Stock:" + Style.RESET_ALL, product_found['stock']]
                        ]
                        print(tabulate(data, tablefmt="fancy_grid"))
                        return
                    else:
                        print("Producto no encontrado. Intente nuevamente...")
                        x=input("Presione cualquier tecla...")
                else:
                    print("Opción no válida. Por favor, ingrese '1' o '2'.")


        
class CrudSales(ICrud):
    def create(self):
            validar = Valida()
            borrarPantalla()
            print('\033c', end='')
            gotoxy(2,1);print(green_color+"*"*90+reset_color)
            gotoxy(30,2);print(blue_color+"Registro de Venta")
            gotoxy(17,3);print(blue_color+Company.get_business_name())
            gotoxy(5,4);print(f"Factura#:F0999999 {' '*3} Fecha:{datetime.datetime.now()}")
            gotoxy(66,4);print("Subtotal:")
            gotoxy(66,5);print("Decuento:")
            gotoxy(66,6);print("Iva     :")
            gotoxy(66,7);print("Total   :")
            gotoxy(15,6);print("Cedula:")
            dni=validar.solo_numeros("Error: Solo numeros",23,6)
            json_clientes = JsonFile(path+'/archivos/clients.json')
            client = json_clientes.find("dni",dni)
            if not client:
                gotoxy(35,6);print("Cliente no existe")
                return
            client = client[0]
            cli = RegularClient(client["nombre"],client["apellido"], client["dni"], card=True) 
            sale = Sale(cli)
            gotoxy(35,6);print(cli.fullName())
            gotoxy(2,8);print(green_color+"*"*90+reset_color) 
            gotoxy(5,9);print(purple_color+"Linea") 
            gotoxy(12,9);print("Id_Articulo") 
            gotoxy(24,9);print("Descripcion") 
            gotoxy(38,9);print("Precio") 
            gotoxy(48,9);print("Cantidad") 
            gotoxy(58,9);print("Subtotal") 
            gotoxy(70,9);print("n->Terminar Venta)"+reset_color)
            json_productos = JsonFile(path+'/archivos/products.json')
            products = json_productos.read()
            follow ="s"
            line=1
            while follow.lower()=="s":
                gotoxy(7,9+line);print(line)
                gotoxy(15,9+line);
                id=int(validar.solo_numeros("Error: Solo numeros",15,9+line))
                product = next((prod for prod in products if prod["id"] == id), None)
                if not product:
                    gotoxy(24,9+line);print("Producto no existe")
                    time.sleep(1)
                    gotoxy(24,9+line);print(" "*20)
                else:
                    product_stock = product["stock"]
                    if product_stock < 1:
                        gotoxy(24,9+line);print("Producto sin stock disponible")
                        time.sleep(1)
                        gotoxy(24,9+line);print(" "*30)
                    else:
                        gotoxy(24,9+line);print(product["descripcion"])
                        gotoxy(38,9+line);print(product["precio"])
                        gotoxy(49,9+line);qyt=int(validar.solo_numeros("Error:Solo numeros",49,9+line))
                        if qyt > product_stock:
                            gotoxy(49,9+line);print("Cantidad insuficiente, stock disponible:", product_stock)
                            time.sleep(1)
                            gotoxy(49,9+line);print(" "*40)
                        else:
                            gotoxy(59,9+line);print(product["precio"] * qyt)
                            sale.add_detail(Product(product["id"], product["descripcion"], product["precio"], product_stock), qyt)
                            product["stock"] -= qyt  # Actualizar el stock del producto
                            json_productos.save(products)  # Guardar los cambios en el archivo JSON
                            gotoxy(76,4);print(round(sale.subtotal,2))
                            gotoxy(76,5);print(round(sale.discount,2))
                            gotoxy(76,6);print(round(sale.iva,2))
                            gotoxy(76,7);print(round(sale.total,2))
                            gotoxy(74,9+line);follow=input() or "s"  
                            gotoxy(76,9+line);print(green_color+"✔"+reset_color)  
                            line += 1
            gotoxy(15,9+line);print(red_color+"Esta seguro de grabar la venta(s/n):")
            gotoxy(54,9+line);procesar = input().lower()
            if procesar == "s":
                gotoxy(15,10+line);print("😊 Venta Grabada satisfactoriamente 😊"+reset_color)
                json_invoices = JsonFile(path+'/archivos/invoices.json')
                invoices = json_invoices.read()
                ult_invoices = invoices[-1]["factura"]+1
                data = sale.getJson()
                data["factura"]=ult_invoices
                invoices.append(data)
                json_invoices.save(invoices)
            else:
                gotoxy(20,10+line);print("🤣 Venta Cancelada 🤣"+reset_color)    
            time.sleep(2)



    
    def update(self):
            while True:
                borrarPantalla()
                # Solicitar el número de factura como un número entero
                numero_factura_input = input("Ingrese el número de factura que desea modificar (deje en blanco para volver atrás): ")
                
                if not numero_factura_input:
                    respuesta = input("No ha ingresado ningún número de factura. ¿Desea volver a intentarlo? (s/n): ")
                    if respuesta.lower() != 's':
                        return

                try:
                    numero_factura = int(numero_factura_input)
                except ValueError:
                    print("Por favor, ingrese un número válido.")
                    continue

                json_file = JsonFile(path+'/archivos/invoices.json')
                invoices = json_file.read()
                
                # Buscar la factura con el número proporcionado
                factura_encontrada = None
                for factura in invoices:
                    if factura["factura"] == numero_factura:
                        factura_encontrada = factura
                        break
                
                if factura_encontrada is None:
                    print(Fore.RED + "La factura no fue encontrada.")
                    continue
                
                # Obtener la información del cliente y detalles de la factura encontrada
                cliente = factura_encontrada["cliente"]
                subtotal = factura_encontrada["subtotal"]
                descuento = factura_encontrada["descuento"]
                iva = factura_encontrada["iva"]
                total = factura_encontrada["total"]
                detalle_venta = factura_encontrada["detalle"]
                
                # Mostrar los detalles de la factura
                print(Fore.BLUE + "Detalles de la factura:")
                print("Factura#:", factura_encontrada["factura"])
                print("Fecha:", factura_encontrada["Fecha"])
                print("Cliente:", cliente)
                print("Subtotal:", subtotal)
                print("Descuento:", descuento)
                print("IVA:", iva)
                print("Total:", total)

                # Mostrar los detalles de la venta
                print("\nDetalles de la venta:")
                for detalle in detalle_venta:
                    print("\nDetalle actual:")
                    print("Producto:", detalle["poducto"])
                    print("Precio:", detalle["precio"])
                    print("Cantidad:", detalle["cantidad"])

                # Confirmar si se desea modificar esta factura
                confirmacion = input("\n¿Desea modificar esta factura? (s/n): ")
                if confirmacion.lower() != 's':
                    continue
                
                # Modificar detalles de la venta y actualizar stock
                for detalle in detalle_venta:
                    print("\nDetalle actual:")
                    print("Producto:", detalle["poducto"])
                    print("Precio:", detalle["precio"])
                    print("Cantidad:", detalle["cantidad"])
                    
                    # Solicitar nueva cantidad
                    nueva_cantidad = int(input("Ingrese la nueva cantidad para este producto: "))
                    cantidad_original = detalle["cantidad"]
                    detalle["cantidad"] = nueva_cantidad
                    
                    # Buscar el producto en la lista de productos
                    producto_descripcion = detalle["poducto"]
                    json_productos = JsonFile(path+'/archivos/products.json')
                    products = json_productos.read()
                    product = next((prod for prod in products if prod["descripcion"] == producto_descripcion), None)
                    if product:
                        cantidad_disponible = product["stock"]
                        diferencia_cantidad = nueva_cantidad - cantidad_original
                        if diferencia_cantidad > 0:  # Si se están agregando más productos
                            if diferencia_cantidad > cantidad_disponible:
                                print(Fore.RED + f"No hay suficiente stock para añadir {diferencia_cantidad} unidades del producto {producto_descripcion}. Stock disponible: {cantidad_disponible}")
                                detalle["cantidad"] = cantidad_original + (cantidad_disponible)  # Restaurar la cantidad original
                            else:
                                product["stock"] -= diferencia_cantidad  # Actualizar el stock
                        elif diferencia_cantidad < 0:  # Si se están devolviendo productos
                            product["stock"] -= diferencia_cantidad  # Actualizar el stock
                        json_productos.save(products)  # Guardar los cambios en el archivo JSON
                    else:
                        print(Fore.RED + "El producto no fue encontrado.")
                
                # Actualizar los totales de la venta
                subtotal_actualizado = sum(detalle["precio"] * detalle["cantidad"] for detalle in detalle_venta)
                factura_encontrada["subtotal"] = subtotal_actualizado
                total_actualizado = subtotal_actualizado - descuento + iva
                factura_encontrada["total"] = total_actualizado
                
                # Guardar los cambios en el archivo JSON
                json_file.save(invoices)
                print(Fore.GREEN + "Venta modificada exitosamente.")
                break



    def delete(self):
        borrarPantalla()
        # Leer el archivo JSON de facturas
        json_file = JsonFile(path+'/archivos/invoices.json')
        invoices = json_file.read()
        
        # Verificar si hay al menos dos facturas en el archivo
        if len(invoices) < 2:
            print(Fore.RED + "No hay suficientes facturas para eliminar.")
            return
        
        # Solicitar el número de factura que se desea eliminar
        numero_factura = int(input("Ingrese el número de factura que desea eliminar (excepto la primera): "))
        
        # Verificar si la factura a eliminar es la primera
        if numero_factura == 1:
            print(Fore.RED + "No se puede eliminar la primera factura.")
            return
        
        # Buscar la factura con el número proporcionado
        factura_encontrada = None
        for factura in invoices:
            if factura["factura"] == numero_factura:
                factura_encontrada = factura
                break
        
        if factura_encontrada is None:
            print(Fore.RED + "La factura no fue encontrada.")
            return
        
        # Mostrar la factura por pantalla
        print(Fore.CYAN + "\nDetalles de la factura a eliminar:" + Fore.RESET)
        print("Factura#:", factura_encontrada["factura"])
        print("Fecha:", factura_encontrada["Fecha"])
        print("Cliente:", factura_encontrada["cliente"])
        print("Subtotal:", factura_encontrada["subtotal"])
        print("Descuento:", factura_encontrada["descuento"])
        print("IVA:", factura_encontrada["iva"])
        print("Total:", factura_encontrada["total"])
        print(Fore.CYAN + "\nDetalles de productos comprados:" + Fore.RESET)
        
        # Mostrar los detalles de la venta en formato tabular
        detalle_data = []
        for detalle in factura_encontrada["detalle"]:
            detalle_data.append([
                Fore.MAGENTA + "Producto:" + Style.RESET_ALL,
                detalle['poducto'],
                Fore.MAGENTA + "Precio:" + Style.RESET_ALL,
                str(detalle['precio']),
                Fore.MAGENTA + "Cantidad:" + Style.RESET_ALL,
                str(detalle['cantidad'])
            ])

        print(tabulate(detalle_data, headers=["", "", "", "", "", ""], tablefmt="grid"))

        # Confirmar con el usuario antes de eliminar la factura
        confirmacion = input(f"\n¿Está seguro de que desea eliminar la factura {numero_factura}? (s/n): ").lower()
        if confirmacion != "s":
            print(Fore.YELLOW + "Operación cancelada.")
            return

        # Devolver el stock de los productos comprados en la factura
        for detalle in factura_encontrada["detalle"]:
            producto_descripcion = detalle["poducto"]
            cantidad_devuelta = detalle["cantidad"]
            json_productos = JsonFile(path+'/archivos/products.json')
            products = json_productos.read()
            product = next((prod for prod in products if prod["descripcion"] == producto_descripcion), None)
            if product:
                product["stock"] += cantidad_devuelta  # Devolver el stock
                json_productos.save(products)  # Guardar los cambios en el archivo JSON
            else:
                print(Fore.RED + "El producto no fue encontrado.")

        # Eliminar la factura del archivo JSON
        invoices.remove(factura_encontrada)
        
        # Guardar los cambios en el archivo JSON
        json_file.save(invoices)
        print(Fore.GREEN + f"La factura {numero_factura} ha sido eliminada satisfactoriamente." + Fore.RESET)








    
    def consult(self):
            print('\033c', end='')
            gotoxy(2,1);print(green_color+"█"*90)
            gotoxy(2,2);print("██"+" "*34+"Consulta de Venta"+" "*35+"██")
            gotoxy(2,4);invoice= input("Ingrese Factura: ")
            if invoice.isdigit():
                invoice = int(invoice)
                json_file = JsonFile(path+'/archivos/invoices.json')
                invoices = json_file.find("factura", invoice)
                
                if invoices:
                    factura = invoices[0]
                    detalles_factura = {k: v for k, v in factura.items() if k != 'detalle'}
                    detalle_venta = factura["detalle"]
                    
                    # Mostrar los detalles principales de la factura
                    print(f"Impresion de la Factura#{invoice}")
                    print(tabulate([detalles_factura], headers="keys", tablefmt="fancy_grid"))
                    
                    # Mostrar el detalle de la venta
                    print("\nDetalle de la Venta:")
                    headers = detalle_venta[0].keys() if detalle_venta else []
                    data = [[detalle[key] for key in headers] for detalle in detalle_venta]
                    if data:
                        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))
                    else:
                        print("No hay detalles de venta para esta factura.")
                else:
                    print("No se encontraron detalles para esta factura.")
            else:    
                json_file = JsonFile(path+'/archivos/invoices.json')
                invoices = json_file.read()
                print("Consulta de Facturas")
                for fac in invoices:
                    print(f"{fac['factura']}   {fac['Fecha']}   {fac['cliente']}   {fac['total']}")
                
                suma = reduce(lambda total, invoice: round(total+ invoice["total"],2), 
                invoices,0)
                totales_map = list(map(lambda invoice: invoice["total"], invoices))
                total_client = list(filter(lambda invoice: invoice["cliente"] == "Dayanna Vera", invoices))

                max_invoice = max(totales_map)
                min_invoice = min(totales_map)
                tot_invoices = sum(totales_map)
                print("filter cliente: ",total_client)
                print(f"map Facturas:{totales_map}")
                print(f"              max Factura:{max_invoice}")
                print(f"              min Factura:{min_invoice}")
                print(f"              sum Factura:{tot_invoices}")
                print(f"              reduce Facturas:{suma}")
            x=input("presione una tecla para continuar...")      

# Clase para el menú
class Menu:
    def __init__(self, titulo, opciones, x, y):
        self.titulo = titulo
        self.opciones = opciones
        self.x = x
        self.y = y

    def mostrar(self):
        print(Fore.BLUE + self.titulo.center(50))
        print(Fore.RESET)
        for idx, opcion in enumerate(self.opciones, start=1):
            print(Fore.GREEN + f"{idx}) {opcion}" + Fore.RESET)

    def menu(self):
        self.mostrar()
        return input("Seleccione una opción: ")

# Menu principal
opc = ''
while opc != '4':
    borrarPantalla()
    menu_main = Menu("Menu Facturacion", ["Clientes", "Productos", "Ventas", "Salir"], 20, 10)
    opc = menu_main.menu()
    if opc == "1":
        opc1 = ''
        while opc1 != '5':
            borrarPantalla()
            clients = CrudClients()
            menu_clients = Menu("Menu Clientes", ["Ingresar", "Actualizar", "Eliminar", "Consultar", "Salir"], 20, 10)
            opc1 = menu_clients.menu()
            if opc1 == "1":
                clients.create()
            elif opc1 == "2":
                clients.update()
            elif opc1 == "3":
                clients.delete()
            elif opc1 == "4":
                clients.consult()
            input("Regresando...")
    elif opc == "2":
        opc2 = ''
        while opc2 != '5':
            borrarPantalla()
            productos = CrudProducts()
            menu_products = Menu("Menu Productos", ["Ingresar", "Actualizar", "Eliminar", "Consultar", "Salir"], 20, 10)
            opc2 = menu_products.menu()
            if opc2 == "1":
                productos.create()
            elif opc2 == "2":
                productos.update()
            elif opc2 == "3":
                productos.delete()
            elif opc2 == "4":
                productos.consult()
            input("Presione una tecla para continuar...")
    elif opc == "3":
        opc3 = ''
        while opc3 != '5':
            borrarPantalla()
            sales = CrudSales()
            menu_sales = Menu("Menu Ventas", ["Registro Venta", "Consultar", "Modificar", "Eliminar", "Salir"], 20, 10)
            opc3 = menu_sales.menu()
            if opc3 == "1":
                sales.create()
            elif opc3 == "2":
                sales.consult()
            elif opc3 == "3":
                sales.update()
            elif opc3 == "4":
                sales.delete()
            input("Presione una tecla para continuar...")

borrarPantalla()
input("Presione una tecla para salir...")
borrarPantalla()
