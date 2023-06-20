import os
import functools
import json


def cargar_datos_desde_archivo() -> list:
    """
    Carga los datos desde un archivo CSV y devuelve los datos del archivo en formato de lista de diccionarios
    """

    with open(r"D:\Tomas\UTN\1er cuatrimestre\lab I\carpetasEjercicios\Parcial\insumos.csv", "r", encoding="utf-8") as file:
        lista_insumos = []
        for linea in file:
            campos = linea.split(",")
            if len(campos) == 5:
                diccionario = {}
                diccionario["id"] = campos[0]
                diccionario["nombre"] = campos[1]
                diccionario["marca"] = campos[2]
                diccionario["precio"] = campos[3]
                diccionario["caracteristicas"] = campos[4].strip("\n")
                lista_insumos.append(diccionario)
    return lista_insumos


lista_insumos = cargar_datos_desde_archivo()


def listar_cantidad_por_marca(lista: list) -> None:
    """
    Recorre la lista dada como argumento e imprime la cantidad de productos que hay para cada marca

    Args:
        lista (list): Lista de diccionarios que contiene información de los insumos. 
    Returns:
        None
    """
    diccionario_cantidades = {}
    for i in lista:
        if i["marca"] not in diccionario_cantidades.keys():
            diccionario_cantidades[i["marca"]] = 1
        else:
            diccionario_cantidades[i["marca"]] += 1
    print(diccionario_cantidades)


def listar_insumo_por_marca(lista: list) -> None:
    """Recorre una lista de marcas individuales y las filtra de modo que que se imprima, por cada marca, el precio y nombre de sus productos

    Args:
        lista(list):lista de diccionarios con informacion de insumos y sus marcas

    Returns:
        None
    """

    lista_marcas = list(set(map(lambda i: i["marca"], lista)))
    marcas_filtradas = []
    # for i in lista:
    #     if i["marca"] not in marcas_filtradas:
    #         marcas_filtradas.append(i["marca"])
    # marcas_filtradas.extend(filter(lambda j: j["marca"] not in marcas_filtradas, lista))
    for i in lista_marcas:
        print(f'Marca: {i}')
        marca_filtrada = filter(lambda j: j["marca"] == i, lista)
        for j in marca_filtrada:
            print(f' Nombre: {j["nombre"]}, Precio: {j["precio"]}')


def buscar_insumo_por_caracteristica(lista: list) -> None:
    """El usuario ingresa una característica (por ejemplo, "Sin Granos") y se listarán todos los insumos que poseen dicha característica.

    Args:
        lista(list): Lista de diccionarios que contiene información de los insumos. 

    Returns:
        None
    """
    lista_caracteristicas = []
    for i in lista_insumos:
        lista_a_chequear = i["caracteristicas"].lower().split("~")
        for j in lista_a_chequear:
            lista_caracteristicas.append(j)
    caracteristica_a_buscar = input("ingrese valor a chequear: ").lower()
    
    while caracteristica_a_buscar not in lista_caracteristicas:
        caracteristica_a_buscar = input("error.ingrese valor a chequear: ").lower()
    print(caracteristica_a_buscar.capitalize())
    lista_valores_chequeados = list(filter(
        lambda i: caracteristica_a_buscar in i["caracteristicas"].lower().split("~"), lista))
    for i in lista_valores_chequeados:
        print(i)



def listar_insumos_ordenados(lista: list) -> None:
    """Muestra el ID, descripción, precio, marca y la primera característica de todos los productos, ordenados por marca de forma ascendente (A-Z) y, ante marcas iguales, por precio descendente.

    Args:
        lista(list): Lista de diccionarios que contiene información de los insumos. 

    Returns:
        None
    """

    lista_ordenada = []
    for i in range(len(lista) - 1):
        for j in range(i + 1, len(lista)):
            if (lista[i]["marca"] > lista[j]["marca"]):
                aux = lista[i]
                lista[i] = lista[j]
                lista[j] = aux
            elif (lista[i]["marca"] == lista[j]["marca"]):
                if (lista[i]["precio"] < lista[j]["precio"]):
                    aux = lista[i]
                    lista[i] = lista[j]
                    lista[j] = aux
    for i in lista:
        lista_caracteristica = i["caracteristicas"].split("~")
        print(
            f'{i["marca"]} {i["nombre"]} {i["id"]} {i["precio"]} {lista_caracteristica[0]}')


def realizar_compras(lista: list) -> None:
    """Permite realizar compras de productos. El usuario
ingresa una marca y se muestran todos los productos disponibles de
esa marca. Luego, el usuario elige un producto y la cantidad deseada.
Esta acción se repite hasta que el usuario decida finalizar la compra.
Al finalizar, se muestra el total de la compra y se genera un archivo
TXT con la factura de la compra, incluyendo cantidad, producto,
subtotal y el total de la compra.

Args:
    lista(list): Lista de diccionarios que contiene información de los insumos.

Returns:
    None

    """
    lista_marcas = list(set(map(lambda i: i["marca"].lower(), lista)))
    lista_compras = []
    salir = False
    while (salir == False):

        lista_marca_inspeccionada = []
        marca_a_inspeccionar = input("ingrese marca: ").lower()

        while marca_a_inspeccionar not in lista_marcas:
            marca_a_inspeccionar = input(
                "Marca no encontrada, ingrese marca").lower()
        opcion = 0
        precio = 0

        for i in lista:
            if i["marca"].lower() == marca_a_inspeccionar:
                opcion += 1
                lista_marca_inspeccionada.append(i)
                print(f'opcion {opcion}(comprar): {i}')
        print(f'opcion {opcion + 1}: {"Salir"}')
        print(f'opcion {opcion + 2}: {"Comprar otro producto"}')
        eleccion = input("Que desea hacer? ")
        while eleccion.isalpha():
            eleccion = input("Que desea hacer? ")
        if eleccion.isdigit():
            eleccion = int(eleccion)
        if int(eleccion) < 0:
            eleccion = int(eleccion)
        while (eleccion != "s") and (eleccion != opcion+1) and not (0 < eleccion <= opcion + 2):
            eleccion = input("error.que desea hacer?")
            if eleccion.isdigit():
                eleccion = int(eleccion)

        if eleccion == opcion + 1:
            salir = True
            break
        elif eleccion == opcion + 2:
            continue
        cantidad_elegida = input(f"cuanto desea comprar? ")

        while not cantidad_elegida.isdigit() or int(cantidad_elegida) < 0:
            cantidad_elegida = input(f"cuanto desea comprar?")

        if cantidad_elegida.isdigit():
            cantidad_elegida = int(cantidad_elegida)
        if (eleccion > 0 and eleccion < opcion + 1) and (cantidad_elegida < 1000):
            diccionario = {}
            precio += cantidad_elegida * \
                (float(
                    lista_marca_inspeccionada[eleccion - 1]["precio"].replace("$", "")))
            diccionario["nombre"] = lista_marca_inspeccionada[eleccion - 1]["nombre"]
            diccionario["marca"] = lista_marca_inspeccionada[eleccion - 1]["marca"]
            diccionario["precio"] = lista_marca_inspeccionada[eleccion - 1]["precio"]
            diccionario["caracteristicas"] = lista_marca_inspeccionada[eleccion -
                                                                       1]["caracteristicas"]
            diccionario["cantidad"] = cantidad_elegida
            lista_compras.append(diccionario)

        eleccion2 = input("Desea comprar otro producto(1) o desea salir(2)")
        if ((eleccion2.isdigit()) and (0 < int(eleccion2) < 3)):
            if int(eleccion2) == 1:
                continue
            elif int(eleccion2) == 2:
                salir = True
                break
            else:
                print(
                    "valor invalido, se lo devolvera al principio para que elija otro producto")

    with open("factura.txt", "w") as file:
        for i in lista_compras:
            file.write(
                f'x{i["cantidad"]} producto: {i["nombre"]}({i["marca"]}), precio: {i["precio"]}\n')
        file.write(f"Total: {precio}")


def guardar_json(lista) -> None:
    """Genera un archivo JSON con todos los
productos cuyo nombre contiene la palabra "Alimento".

Args:
    lista(list): Lista de diccionarios que contiene información de los insumos.

Returns:
    None

    """

    lista_alimento = []
    for i in lista:
        if "Alimento" in i["nombre"]:
            lista_alimento.append(i)
    with open("alimento.json", "w", encoding="utf-8") as file:
        json.dump(lista_alimento, file)
    # return lista_alimento


def leer_desde_formato_json() -> None:
    """Permite mostrar un listado de los insumos
guardados en el archivo JSON generado en la opción anterior.

Returns:
    None
    """

    with open("alimento.json", "r", encoding="utf-8") as file:
        lista_alimentos = json.load(file)
        print(lista_alimentos)


def actualizar_precios(lista: list) -> None:
    """Aplica un aumento del 8.4% a todos los
productos, utilizando la función map. Los productos actualizados se
guardan en el archivo "Insumos.csv".

Args:
    lista(list): Lista de diccionarios que contiene información de los insumos.

Returns: None

    """

    lista_actualizada_precios = list(map(lambda value:
                                         {"id": value["id"],
                                          "nombre": value["nombre"],
                                             "marca": value["marca"],
                                             "precio": float(value["precio"].replace("$", "")) * 1.084,
                                             "caracteristicas": value["caracteristicas"]}, lista))
    with open("insumos.csv", "w", encoding="utf-8") as file:
        for producto in lista_actualizada_precios:
            file.write(
                f"{producto['id']},{producto['nombre']},{producto['marca']},{producto['precio']},{producto['caracteristicas']}\n")


def cargar_marcas():
    lista_marcas = []
    with open(r"D:\Tomas\UTN\1er cuatrimestre\lab I\carpetasEjercicios\Parcial\marcas.txt", "r", encoding="utf-8") as file:
        for linea in file:
            lista_marcas.append(linea.lower().strip("\n"))
    return lista_marcas


lista_marcas_nuevas = cargar_marcas()

def imprimir_marcas_nuevas(lista:list):
        print(lista)

def agregar_nuevo_producto(lista: list):
    lista_nombres = []
    lista_ids = []
    lista_caracteristicas = []
    lista_precios = []
    for i in lista_insumos:
        lista_a_chequear = i["caracteristicas"].lower().split("~")
        lista_ids.append(i["id"])
        lista_nombres.append(i["nombre"])
        lista_precios.append(i["precio"])
        for j in lista_a_chequear:
            lista_caracteristicas.append(j)
    lista_caracteristicas = list(set(lista_caracteristicas))
    lista_productos_nuevos = []
    seguir_agregando = True
    while seguir_agregando:
        caracteristicas_nuevo_producto = []
        marca_a_agregar = input("que marca desea elegir? ").lower()
        while marca_a_agregar not in lista:
            marca_a_agregar = input("error.que marca desea elegir? ").lower()
        id = input("ingrese id")
        while id in lista_ids or not id.isdigit():
            id = input("error.ingrese id valido: ")
        nombre = input("ingrese nombre: ")
        while nombre in lista_nombres:
            nombre = input("error.ingrese nombre valido: ")
        precio = input("ingrese precio")
        caracteristica = input("ingrese caracteristica: ")
        
        while not caracteristica.isalpha():
            caracteristica = input("error.ingrese caracteristica valida: ")
        caracteristicas_nuevo_producto.append(caracteristica)
        caracteristica2 = input(
            "desea agregar otra caracteristica(si) o no(no)? ")
        if caracteristica2 == "si":
            caracteristica2_real = input("ingrese caracteristica")
            while not caracteristica2_real.isalpha():
                caracteristica2_real = input("error.ingrese caracteristica valida: ")
            caracteristicas_nuevo_producto.append(caracteristica2_real)

            caracteristica3 = input(
                "desea agregar otra caracteristica(si) o no(no)?")
            if caracteristica3 == "si":
                caracteristica3_real = input("ingrese caracteristica")
                while not caracteristica3_real.isalpha():
                    caracteristica3_real = input("error.ingrese caracteristica valida: ")
                caracteristicas_nuevo_producto.append(caracteristica3_real)

        caracteristicas_a_agregar = "~".join(caracteristicas_nuevo_producto)
        producto_nuevo = {
            "id":  id,
            "nombre": nombre,
            "marca": marca_a_agregar,
            "precio": precio,
            "caracteristicas": caracteristicas_a_agregar
        }
        lista_productos_nuevos.append(producto_nuevo)
        seguir_agregando_usuario = input("Desea agregar otro producto?(si/no) ")
        while seguir_agregando_usuario != "si" and seguir_agregando_usuario != "no":
            seguir_agregando_usuario = input("Desea agregar otr producto?(si/no) ")
        if seguir_agregando_usuario == "no":
            seguir_agregando = False
    return lista_productos_nuevos


def guardar_datos_actualizados(lista_productos_nuevos):

    lista_a_guardar = lista_insumos + lista_productos_nuevos
    tipo_archivo_a_guardar = input(
        "elija tipo de archivo a gurdar(json o csv)").lower()
    while tipo_archivo_a_guardar != "json" and tipo_archivo_a_guardar != "csv":
        tipo_archivo_a_guardar = input(
            "elija tipo de archivo a gurdar(json o csv)").lower()
    nombre_archivo = input(
        "ingrese nombre de archivo nuevo que desea guardar(sin la extension)")
    nuevo_nombre_archivo = f'{nombre_archivo}.{tipo_archivo_a_guardar}'
    if tipo_archivo_a_guardar == "json":
        try:
            with open(nuevo_nombre_archivo, "w") as file:
                json.dump(lista_a_guardar, file)
        except Exception:
            print("No se pudo guardar el archivo")
    elif tipo_archivo_a_guardar == "csv":
        try:
            with open(nuevo_nombre_archivo, "w") as file:
                for producto in lista_a_guardar:
                    file.write(
                        f"{producto['id']},{producto['nombre']},{producto['marca']},{producto['precio']},{producto['caracteristicas']}\n")
        except Exception:
            print("No se pudo guardar el archivo")


def menu_opciones() -> None:
    """Se ofrece un menu de opciones para realizar diferentes tareas sobre una lista de insumos.El usuario seleeciona lo que quiere hacer, y se ejecuta la funcion pedida

    Returns:
        None

    """
    while True:
        os.system("cls")
        print("""
        ----------Menú de opciones-----------
        | 1_Cargar datos desde archivo      |
        | 2-Listar cantidad por marca       |
        | 3-Listar insumos por marca        | 
        | 4-Buscar insumo por caracteristica|
        | 5-Listar insumos ordenados        |
        | 6-Realizar compras                |
        | 7-Guardar en formato json         |
        | 8-Leer desde formato json         |
        | 9-Actualizar precios              |
        | 10-Agregar producto               |    
        | 11- Guardar datos actualizados    |
        |  12- Salir                        |
        -------------------------------------    
            """
              )

        opcion = input("Elija opcion(1-12): ")
        os.system("cls")
        if opcion == "1":
            cargar_datos_desde_archivo()
        elif opcion == "2":
            listar_cantidad_por_marca(lista_insumos)
        elif opcion == "3":
            listar_insumo_por_marca(lista_insumos)
        elif opcion == "4":
            buscar_insumo_por_caracteristica(lista_insumos)
        elif opcion == "5":
            listar_insumos_ordenados(lista_insumos)
        elif opcion == "6":
            realizar_compras(lista_insumos)
        elif opcion == "7":
            guardar_json(lista_insumos)
        elif opcion == "8":
            leer_desde_formato_json()
        elif opcion == "9":
            actualizar_precios(lista_insumos)
        elif opcion == "10":
            imprimir_marcas_nuevas(lista_marcas_nuevas)
            lista_productos_nuevos = agregar_nuevo_producto(lista_marcas_nuevas)
        elif opcion == "11":
            guardar_datos_actualizados(lista_productos_nuevos)
        elif opcion == "12":
            break
        else:
            print("opcion invalida")
        input("presione cualquier tecla para continuar...")
        os.system("cls")


menu_opciones()
