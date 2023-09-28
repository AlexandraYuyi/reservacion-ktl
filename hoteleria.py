import random
from datetime import date, datetime
import json
import sys
from sortingmethods import *
from gestionreservaciones import *
from hoteles import *
from log import Accion

# Almacena todas las reservas activas en la aplicación (tempDB)
reservas = []
lista_reservacion = Cola()
global reservasCargadas
reservasCargadas = False

# Almacena todas las habitaciones activas de la aplicación (tempDB)
habitaciones = []
global habitacionesCargadas
habitacionesCargadas = False

# Almacena todas las habitaciones activas de la aplicación (tempDB)
usuarios = []

# Almacena todas las reservas dentre de un periodo (tempDB)
reservasPeriodoDB = []

#Almacena los hoteles
global ruta_hoteles
lista_hoteles = ListaEnlazada()
hoteles = []


class Usuario:
    def __init__(self, nombre: str, idn: int, correo: str, telf: str):
        self.nombre = nombre
        self.idn = idn
        self.correo = correo
        self.telf = telf
        self.totalReservaciones = 0

    def infoLineal(self):
        """
        Devuelve le información del objeto de forma imprimible en una sola linea por consola.
        """ 
        return "Nombres: {}, ID: {}, Correo: {}, Telf: {}, Reservaciones: {}".format(self.nombre, self.idn, self.correo, self.telf, self.totalReservaciones)

    def getNombre(self):
        return self.nombre

    def getIDN(self):
        return self.idn
    
    def getTotalReservaciones(self):
        return self.totalReservaciones

    def setReservacion(self):
        self.totalReservaciones += 1

"""
Clase reserva que encapsula la información y las operaciones de cada reserva.
"""
class  Habitacion:

    def __init__(self, id: str, tipo: str, capacidad: int, precio: int):
        """
        Construye los objetos de la clase Habitacion.
        
        :param id: identificador de la habitacion
        :param tipo: tipo de habitacion
        :param capacidad: capacidad de la habitacion
        :param precio: precio de una noche en la habitacion
        """
        self.id = id
        self.tipo = tipo
        self.capacidad = capacidad
        self.precio = precio

    def info(self):
        """
        Devuelve le información del objeto de forma imprimible por consola.
        """ 
        return "{: <10} {: <16} {: <3} {: >3}$".format(self.id, self.tipo, self.capacidad, self.precio)
    
    """
    Getters de :class:`Habitacion`
    """
    def getId(self):
        return self.id
    
    def getTipo(self):
        return self.tipo
    
    def getCapacidad(self):
        return self.capacidad
    
    def getPrecio(self):
        return self.precio

    """
    Setters de :class: `Habitacion`
    """
    def setHabitacion(self, Id, Tipo, Capacidad, Precio):
        self.id = Id
        self.tipo = Tipo
        self.capacidad = Capacidad
        self.precio= Precio
"""
Clase reserva que encapsula la información y las operaciones de cada reserva.
"""
class Reserva:

    def __init__(self, usuario, habitacion, hotel ,fechaEntrada, fechaSalida):
        """
        Construye los objetos de la clase Reserva.
        
        :param nombre: nombre del responsable de la reserva
        :param idn: numero de identificacion del responsable de la reserva
        :param correo: correo electronico del responsable de la reserva
        :param telf: numero telefonico del responsable de la reserva
        :param habitacion: objeto que contiene la informacion de la habitacion reservada
        :param fechaEntrada: fecha de entrada de la reserva
        :param fechaSalida: fecha de salida de la reserva
        """

        self.id = verificarID()
        self.usuario = usuario
        self.fechaReserva = datetime.now
        self.habitacion = habitacion
        self.fechaEntrada = fechaEntrada
        self.fechaSalida = fechaSalida
        self.duracion = fechaSalida - fechaEntrada
        self.hotel = hotel
        self.costoTotal = self.duracion.days * self.habitacion.getPrecio()

    def info(self):
        """
        Devuelve le información del objeto de forma imprimible por consola.
        """ 
        return "ID: {:0>5}\n Nombres: {}\n Habitacion: {} Hotel: {}\n \n Entrada: {}\n Salida: {}\n Duración: {} días\n\n TOTAL: {}$".format(self.id, self.usuario.getNombre(), self.habitacion.getId(), self.hotel, self.fechaEntrada.strftime("%A %d. %B %Y"), self.fechaSalida.strftime("%A %d. %B %Y"), self.duracion.days, self.costoTotal)

    def infoLineal(self):
        """
        Devuelve le información del objeto de forma imprimible en una sola linea por consola.
        """ 
        return "ID: {:0>5}, Nombres: {}, Habitacion: {}, Hotel: {}, Entrada: {}, Salida: {}, Duración: {} días, TOTAL: {}$".format(self.id, self.usuario.getNombre(), self.habitacion.getId(),self.hotel ,self.fechaEntrada.strftime("%d/%m/%y"), self.fechaSalida.strftime("%d/%m/%y"), self.duracion.days, self.costoTotal)

    """
    Getters de :class:`Reserva`
    """
    def getId(self):
        return self.id

    def getNombre(self):
        return self.nombre

    def getFechaReserva(self):
        return self.fechaReserva

    def getHabitacion(self):
        return self.habitacion

    def getFechaEntrada(self):
        return self.fechaEntrada

    def getFechaSalida(self):
        return self.fechaSalida
    
    def getDuracion(self):
        return self.duracion
    
    def getCostoTotal(self):
        return self.costoTotal

"""
Genera un identificador aleatorio y verifica que no concida
"""
def verificarID():
    # Genera un numero aleatorio entre 0 y 99999
    id = random.randint(0, 99999)

    # Verifica que el el id creado no exista entre las reservas 
    for reserva in reservas:
        if reserva.getId() == id:
            verificarID()
    
    Accion("Operacion", "Se que el id {}, sea unico".format(id)).guardar()

    # Retorna el identificador verificado
    return id

"""
Crea un objeto fecha a partir de una cadena de texto
"""
def fecha(fecha):
    # Separa la cadena de texto separando cada valor en su variable
    dia, mes, ano = fecha.split("/")

    # Se convierte en el texto en numero
    try:
        dia = int(dia)
        mes = int(mes)
        ano = int(ano)
    except ValueError:
        Accion("Error", "La fecha solo admite el formato dd/mm/aaaa").guardar()
        print('\n( X ) La fecha solo admite el formato dd/mm/aaaa')
    # Crea el objeto del tipo Fecha
    fechaObjeto = date(ano, mes, dia)

    Accion("Operacion", "Se creo el objeto de la fecha {}".format(fecha)).guardar()
  
    # Retorna el objeto
    return fechaObjeto

"""
Funcion que carga la configuracion inicial de la aplicacion
"""
def cargarConfig():
    # Abre el archivo de configuracion en modo lectura
    with open('./config.json', 'r') as db:

        # Interpreta el formato JSON
        configJSON = json.load(db)

        # Asigna los valores a variables
        global default 
        default = configJSON[0]["default"]
        
        global ruta_habs
        ruta_habs = configJSON[0]["seed_rooms"]
        
        global ruta_reserv
        ruta_reserv = configJSON[0]["seed_reserv"]
        
        global hotel
        hotel = configJSON[0]["name_hotel"]

        global ruta_hoteles
        ruta_hoteles = configJSON[0]["seed_hoteles"]

    Accion("Sistema", "Archivo de configuracion './config.json' cargado exitosamente").guardar()
"""
Funcion que carga todas las habitaciones disponibles en el hotel
"""
def cargarHoteles():
    with open(ruta_hoteles, 'r') as seed:
            dbJSON = json.load(seed)
            for hotel in dbJSON:
                nom = hotel["nombre"]
                dir = hotel["direccion"]
                tel = hotel["telefono"]
                Hoteles = Hotel(nom, dir, tel)
                hoteles.append(Hoteles)
                lista_hoteles.agregar(Hoteles)
    return
"""
Funcion que carga todas las habitaciones disponibles en el hotel
"""
def cargarHabitaciones():
    global habitacionesCargadas
    if (not habitacionesCargadas):
        # Abre el archivo de habitaciones en modo lectura
        with open(ruta_habs, 'r') as db:

            # Interpreta el formato JSON
            dbJSON = json.load(db)

        # Recorre la lista de obtenida
        for habitacion in dbJSON:

            # Asigna los valores a variables
            id = habitacion["id"]
            tipo = habitacion["tipo"]
            capacidad = habitacion["capacidad"]
            precio = habitacion["precio"]
            
            # Se construye el objeto del tipo Habitacion
            habitacion = Habitacion(id, tipo, capacidad, precio)

            # Se agrega la habitacion a la tempDB
            habitaciones.append(habitacion)
            
        habitacionesCargadas = True
    Accion("Sistema", "Archivo {} cargado exitosamente".format(ruta_habs)).guardar()
    return

"""
Funcion que carga reservas de prueba
"""
def cargarReservas():
    global reservasCargadas
    if (not reservasCargadas):
        # Abre el archivo de reservas en modo lectura
        with open(ruta_reserv, 'r') as db:

            # Interpreta el formato JSON
            dbJSON = json.load(db)

        # Recorre la lista de obtenida
        for reserva in dbJSON:
            bandUsuario = 0
            # Asigna los valores a variables
            cliente = reserva["cliente"]
            nombre = cliente["nombre"]
            correo = cliente["correo"]
            telf = cliente["telf"]
            idn = cliente["idn"]
            habitacion = reserva["habitacion"]
            hotel= habitacion["hotel"]
            habitacionId = habitacion["id"]
            fechaEntrada = fecha(habitacion["fechaEntrada"])
            fechaSalida = fecha(habitacion["fechaSalida"])

            # Recorre la lista de habitaciones
            for habitacionI in habitaciones:
                # Encuentra el objeto de la habitacion y se lo asigna
                if habitacionI.getId() == habitacionId:
                    habitacionId = habitacionI

            for usuario in usuarios:
                if usuario.getIDN() == idn:       
                    bandUsuario = 1
                    # Se construye el objeto del tipo Reserva
                    reserva = Reserva(usuario, habitacionId, hotel ,fechaEntrada, fechaSalida)

                    # Se agrega la reserva a la tempDB0
                    reservas.append(reserva)
                    lista_reservacion.Add(reserva)
                    usuario.setReservacion()

            if bandUsuario == 0:
                usuarioNuevo = Usuario(nombre, idn, correo, telf)
                usuarios.append(usuarioNuevo)

                # Se construye el objeto del tipo Reserva
                reserva = Reserva(usuarioNuevo, habitacionId, hotel ,fechaEntrada, fechaSalida)

                # Se agrega la reserva a la tempDB0
                reservas.append(reserva)
                lista_reservacion.Add(reserva)
                usuarioNuevo.setReservacion()
        for i in range(lista_hoteles.longitud):
            for reserva in reservas:
                if lista_hoteles.obtener(i).nombre == reserva.hotel:
                    lista_hoteles.obtener(i).añadir_reservacion(reserva)
                    lista_hoteles.obtener(i).añadir_habitacion(reserva.habitacion)

        reservasCargadas = True
        Accion("Sistema", "Archivo {} cargado exitosamente".format(ruta_reserv)).guardar()
        print('\n!!! Archivo cargado exitosamente')
    else:
        Accion("Sistema", "Archivo {} ya habia sido cargado previamente".format(ruta_reserv)).guardar()
        print('\n!!! Archivo previamente cargado')
    return

"""
Funcion para la seleccion y verificacion de habitaciones disponibles
"""
def seleccionarHabitacion(fechaEntrada, fechaSalida):

    # Imprime en la terminal los titulos
    print('\n_________')
    print('HABITACIONES DISPONIBLES')
    print('{: <6}  {: <10} {: <16} {: <3} {: <3}'.format('Opción', 'Habitación', 'Tipo', 'Per.', 'Precio')) 

    # Variable auxiliar para el conteo
    i = 0
    
    # Base de datos temporal para almacenar las habitaciones no disponibles
    habitacionesNoDisponibles = []

    # Recorre la lista de reservas
    for reserva in reservas:
        # Agreaga a la lista temporal las habitaciones que concidan en las fechas
        if ((reserva.getFechaEntrada() < fechaEntrada and reserva.getFechaSalida() > fechaSalida) or (reserva.getFechaEntrada() < fechaEntrada and ( fechaSalida > reserva.getFechaSalida() > fechaSalida)) or (reserva.getFechaSalida() > fechaSalida and ( fechaEntrada < reserva.getFechaEntrada() < fechaSalida))):
            habitacionesNoDisponibles.append(reserva.getHabitacion())
    
    # Crea una lista con las habitaciones disponibles
    habitacionesDiponibles = [x for x in habitaciones if x not in habitacionesNoDisponibles]

    # Recorre la lista de habitaciones disponibles
    for hab  in habitacionesDiponibles:
        # Imprime en la terminal las habitaciones disponlibles formateadas
        print("{: >2}.    ".format(i),hab.info())
        i += 1
    print('‾‾‾‾‾‾‾‾‾')
    
    Accion("Habitacion", "Se mostraron todas las habitaciones").guardar()

    # Solicita la seleccion de habitacion
    index = int(input('Seleccione una habitacion: '))

    # Asigna la habitacion seleccionada a una variable
    habitacionSeleccionada = habitacionesDiponibles[index]
    
    # Retorna el objeto de la habitacion seleccionada
    Accion("Habitacion", "Se selecciono la habitacion {}".format(habitacionSeleccionada.info())).guardar()
    return habitacionSeleccionada

"""
Funcion que crea las reservas
"""
def crearReserva():
    
    # Solicita al usuario los datos necesarios y los almacena en sus respectivas variables
    print('')
    try:
        hotel= input("Seleccione el Hotel donde hara la reservación:\n" + 
                      " 1. Hotel Gran Meliá Caracas\n" + 
                      " 2. Hotel JW Marriott Caracas\n" + 
                      " 3. Hotel Hilton Caracas\n" +
                      "Su selección es: ")
        if hotel == "1":
            hotel = "Hotel Gran Meliá Caracas"
        elif hotel == "2":
            hotel = "Hotel JW Marriott Caracas"
        else: 
            hotel = "Hotel Hilton Caracas"
        print()

        idn = int(input("Indique su número de cédula: "))

        for usuario in usuarios:
            if usuario.getIDN() == idn:
                fechaEntrada = fecha(input("Indique la fecha de entrada (DD/MM/AAAA): "))
                fechaSalida = fecha(input("Indique la fecha de salida (DD/MM/AAAA): "))

                # Se llama a la funcion seleccionarHabitacion para poder escoger dentro de las habitaciones disponibles
                habitacion = seleccionarHabitacion(fechaEntrada, fechaSalida)

                # Crea un nuevo objeto de la clase reserva
                reserva = Reserva(usuario, habitacion, hotel, fechaEntrada, fechaSalida)

                # Se agrega la reserva a la tempDB
                reservas.append(reserva)
                lista_reservacion.Add(reserva)
                usuario.setReservacion()

                print('\n_________')
                # Imprime en la terminal los detalles de la reserva realizada.
                print("RESERVA:\n",reserva.info())
                print('‾‾‾‾‾‾‾‾‾')

                Accion("Reserva", "Reserva de usurios recurrente realizada exitosamente / {}".format(reserva.info())).guardar()
                print('\n!!! Reserva realizada exitosamente')
                return

        nombre = input("Indique su nombre: ")
        correo = input("Indique su correo electrónico: ")
        try:
            telf = int(input("Indique su número telefónico: "))
        except ValueError:
            Accion("Error", "El numero telefonico solo admite numeros").guardar()
            print('\n( X ) El numero telefonico solo admite numeros\n')
            return
            
        fechaEntrada = fecha(input("Indique la fecha de entrada (DD/MM/AAAA): "))
        fechaSalida = fecha(input("Indique la fecha de salida (DD/MM/AAAA): "))

        # Se llama a la funcion seleccionarHabitacion para poder escoger dentro de las habitaciones disponibles
        habitacion = seleccionarHabitacion(fechaEntrada, fechaSalida)

        usuarioNuevo = Usuario(nombre, idn, correo, str(telf))
        usuarios.append(usuarioNuevo)

        # Crea un nuevo objeto de la clase reserva
        reserva = Reserva(usuarioNuevo, habitacion, hotel, fechaEntrada, fechaSalida)

        # Se agrega la reserva a la tempDB
        reservas.append(reserva)
        lista_reservacion.Add(reserva)
        usuario.setReservacion()

        print('\n_________')
        # Imprime en la terminal los detalles de la reserva realizada.
        print("RESERVA:\n",reserva.info())
        print('‾‾‾‾‾‾‾‾‾')

        Accion("Reserva", "Reserva de usurios nuevo realizada exitosamente / {}".format(reserva.info())).guardar()
        print('\n!!! Reserva realizada exitosamente')
        return
    except ValueError:
        Accion("Error", "La cedula solo debe contener numeros").guardar()
        print('\n( X ) Su cedula solo debe contener numeros')

"""
Funcion que permite listar todas las reservas
"""
def verReserervas(arr):
    print('\n_________')

    # Variable auxiliar de conteo
    i = 1

    # Recorre todas las reservas
    for reserva in arr:

        # Imprime en la terminal todas las reservas formateadas
        print("RESERVA", i , ': ', reserva.infoLineal())
        i += 1
    print('\nTOTAL: ', len(arr), 'reservas')
    print('‾‾‾‾‾‾‾‾‾')

    Accion("REPORTE", "Se visualizaron todas las reservas almacenadas").guardar()
    return

"""
Funcion que permite listar todas las reservas
"""
def verUsuarios():
    print('\n_________')

    # Variable auxiliar de conteo
    i = 1

    # Recorre todas las reservas
    for usuario in usuarios:

        # Imprime en la terminal todas las reservas formateadas
        print("USUARIO", i , ': ', usuario.infoLineal())
        i += 1
    print('\nTOTAL: ', len(usuarios), 'usuarios')
    print('‾‾‾‾‾‾‾‾‾')
    Accion("REPORTE", "Se visualizaron todos los usuarios almacenadas").guardar()
    return


"""
Funcion para obtener la lista de reservas en una fecha
"""
def reservasPeriodo(fechaInicio = fecha("01/01/2023"), fechaFinal = fecha("31/12/2023")):
    # Se vacia la base de datos temporal
    reservasPeriodoDB = []

    # Se recorre la lista de reserva
    for reserva in reservas:
        # Se comprueba que se encuentre dentro del periodo seleccionado
        if reserva.getFechaEntrada() > fechaInicio and reserva.getFechaSalida() < fechaFinal:
            # Se agrega a la base de datos temporal
            reservasPeriodoDB.append(reserva)


    print('\n_________')

    # Variable auxiliar de conteo
    i = 1

    # Recorre todas las reservas
    for reserva in reservasPeriodoDB:

        # Imprime en la terminal todas las reservas formateadas
        print("RESERVA", i , ': ', reserva.infoLineal())
        i += 1
    print('‾‾‾‾‾‾‾‾‾')
    return reservasPeriodoDB


def ordenar():
    print('\n\nMENÚ DE CRITERIOS DE ORDENAMIENTO | ' + hotel)
    print('___')
    print('0. Capacidad de la Habitación')
    print('1. Fecha de entrada')
    print('2. Número de habitación')
    print('3. Precio Total')
    print('4. Fecha de salida')
    print('5. Duración de la estadía')
    print('99. Salir')
    
    opcion = int(input('Seleccione una opción: '))
    
    fechaInicial = fecha(input("Indique la fecha inicial (DD/MM/AAAA): "))
    fechaFinal = fecha(input("Indique la fecha final (DD/MM/AAAA): "))
    
    print('1. Ascendente')
    print('2. Descendente')
    orden = input("Seleccione el tipo de ordenamiento: ")
    
    if opcion == 99:
        Accion("Menu", "Se salio del menu 'Ordenar'").guardar()
        return
    else:
        array = reservasPeriodo(fechaInicial, fechaFinal)

        if orden == "1":
            array = quickSort_NoMultiple_ASC(array, 0, len(array)-1, opcion)
            verReserervas(array)
            Accion("Menu", "Se ordeno de forma 'Ascendente'").guardar()
        elif orden == "2":
            array = quickSort_NoMultiple_DESC(array, 0, len(array)-1, opcion)
            verReserervas(array)
            Accion("Menu", "Se ordeno de forma 'Descendente'").guardar()
        elif default == "asc":
            array = quickSort_NoMultiple_ASC(array, 0, len(array)-1, opcion)
            verReserervas(array)
            Accion("Menu", "Se ordeno por defecto 'Ascendente'").guardar()
        elif default == "desc":
            array = quickSort_NoMultiple_DESC(array, 0, len(array)-1, opcion)
            verReserervas(array)
            Accion("Menu", "Se ordeno por defecto 'Descendente'").guardar()
        else:
            Accion("Error", "Por favor ingrese una opción válida, o configure correctamente el orden por defecto en el archivo de configuración").guardar()
            print("Por favor ingrese una opción válida, o configure correctamente el orden por defecto en el archivo de configuración")
    
        opcion = input("Desea volver a ordenar las reservas? (Si = 1 / No = 0): ")

        while opcion !=0:
            Accion("Menu", "Se selecciono la opcion de volver a ordenar las reservas").guardar()
            if opcion == "1":
                print('\n\nMENÚ DE CRITERIOS DE ORDENAMIENTO | ' + hotel)
                print('___')
                print('0. Capacidad de la Habitación')
                print('1. Fecha de entrada')
                print('2. Número de habitación')
                print('3. Precio Total')
                print('4. Fecha de salida')
                print('5. Duración de la estadía')
                print('99. Atras')

                opcion = int(input('Seleccione una opción: '))
        
                if opcion == 99:
                    Accion("Menu", "Se salio del menu 'Ordenar'").guardar()
                    opcion == 0
                    return
                else:
                    if orden == "1":
                        array = quickSort_NoMultiple_ASC(array, 0, len(array)-1, opcion)
                        verReserervas(array)
                        Accion("Menu", "Se ordeno de forma 'Ascendente'").guardar()
                    elif orden == "2":
                        array = quickSort_NoMultiple_DESC(array, 0, len(array)-1, opcion)
                        verReserervas(array)
                        Accion("Menu", "Se ordeno de forma 'Descendente'").guardar()
                    elif default == "asc":
                        array = quickSort_NoMultiple_ASC(array, 0, len(array)-1, opcion)
                        verReserervas(array)
                        Accion("Menu", "Se ordeno por defecto 'Ascendente'").guardar()
                    elif default == "desc":
                        array = quickSort_NoMultiple_DESC(array, 0, len(array)-1, opcion)
                        verReserervas(array)
                        Accion("Menu", "Se ordeno por defecto 'Descendente'").guardar()
                    else:
                        Accion("Error", "Por favor ingrese una opción válida, o configure correctamente el orden por defecto en el archivo de configuración").guardar()
                        print("Por favor ingrese una opción válida, o configure correctamente el orden por defecto en el archivo de configuración")
                    
                    opcion = input("Desea volver a ordenar las reservas? (S=1/N=0): ")
            else:
                return

def gestion_hoteles():
    while True:
        print('___')
        print('\nMENÚ DE GESTIÓN DE HOTELES |')
        print('___')
        print('0. Crear hotel')
        print('1. Eliminar hotel')
        print('2. Ver lista de hoteles')
        print('3. Habitaciones')
        print('4. Ver reservaciones')
        print('99. Salir')
        opcion = int(input('Seleccione una opcion: '))

        match opcion: 
            case 0:
                Accion("Menu", "Se seleccionó la opcion de 'Crear hotel'").guardar()
                print('___')
                print('\nCREACIÓN DE HOTEL |')
                print('___\n')
                Nombre = input('Ingrese el nombre del Hotel: ')
                Direccion = input('Ingrese la dirección del Hotel: ')
                try:
                    Numero = int(input('Ingrese el número de teléfono del Hotel: '))
                except ValueError:
                    Accion("Error", "El numero del hotel no admite Letras. Por favor ingrese nuevamente").guardar()
                    print('\n( X ) Debe de ingresar solo numeros')
                    break
                
                hotel = Hotel(Nombre, Direccion, str(Numero))
                lista_hoteles.agregar(hotel)
                Accion("operacion", "Creación del Hotel '{}'".format(Nombre)).guardar()
                print('\n!!Creación de Hotel exitosa')
            case 1: 
                Accion("Menu", "Se seleccionó la opcion de 'Eliminar hotel'").guardar()
                print('\n___')
                print('\nELIMINACIÓN DE HOTEL')
                print('___\n')
                print('Lista de Hoteles')
                i = 1
                for hotel in lista_hoteles: 
                    print("HOTEL {}: {}".format(i, hotel.Hotel_infoLineal()))
                    i += 1
                op = int(input('\nSeleccione el Hotel que desea eliminar: '))
                op = op - 1
                try:
                    lista_hoteles.pop(op)
                except IndexError: 
                    Accion("Error", "El hotel que selecciona no existe en la lista. Por favor ingrese nuevamente").guardar()
                    print('\n( X ) Debe de ingresar un hotel valido')
                    break
                Accion("operacion", "Eliminación de Hotel exitosa").guardar()
                print('\n!!Eliminación de Hotel exitosa\n')
            case 2: 
                Accion("Menu", "Se seleccionó la opcion de 'Ver lista de hoteles'").guardar()
                print('\n___')
                print('\nLISTA DE HOTEL')
                print('___\n')
                i = 1
                for hotel in lista_hoteles: 
                    print("HOTEL {}: {}".format(i, hotel.Hotel_infoLineal()))
                    i += 1
                Accion("operacion", "Se listaron los hoteles disponibles").guardar()
            case 3: 
                Accion("Menu", "Se seleccionó la opcion de 'Habitaciones'").guardar()
                while True: 
                    bandi = True
                    print('\n___')
                    print('\nSELECCION DE HOTEL |')
                    print('___\n')
                    j= 1
                    for lista in lista_hoteles:
                        print("{}. {}".format(j, lista.nombre))
                        j +=1
                    print('99. Salir')
                    opcion = int(input('Seleccione una opcion: '))
                    if opcion == 99: 
                        break
                    po = opcion - 1
                    try:
                        hotel = lista_hoteles.obtener(po).nombre
                    except IndexError: 
                        Accion("Error", "El hotel que selecciona no existe en la lista. Por favor ingrese nuevamente").guardar()
                        print('\n( X ) Debe de ingresar un hotel valido\n')
                        break 

                    while bandi == True: 
                        print('\n___')
                        print('\nMENÚ DE HABITACIONES DE HOTELES | ' + hotel)
                        print('___')
                        print('0. Crear Habitacion')
                        print('1. Ver Habitaciones')
                        print('2. Modificar Habitacion')
                        print('99. Salir')

                        try:
                            op = int(input('Seleccione una opcion: '))
                        except ValueError: 
                            Accion("Error", "El menu de habitaciones solo admite numeros enteros. Por favor ingrese el numero de la opcion").guardar()
                            print('\n( X ) Debe ingresar el número de la opción')
                            break

                        match op:
                            case 0: 
                                print('\n___')
                                print('\nCREACIÓN DE HABITACION DE HOTEL | '+ hotel)
                                print('___\n')
                                id = input('Ingrese el ID de la Habitacion: ')
                                tip = input('Ingrese el Tipo de la Habitacion: ')
                                try:
                                    Capacidad = int(input('Ingrese la Capacidad de la Habitacion: '))
                                    Precio = int(input('Ingrese el Precio de la Habitacion: '))
                                except ValueError: 
                                    Accion("Error", "El la capacidad o el precio solo admite numeros enteros. Por favor ingrese un valor correcto").guardar()
                                    print('\n( X ) Debe ingresar un valor correcto')
                                    break

                                habitacion = Habitacion(id, tip, Capacidad, Precio)
                                habitaciones.append(habitacion)
                                lista_hoteles.obtener(po).habitaciones.append(habitacion)
                                print('\n!!Creacion de habitacion exitosa')
                            case 1: 
                                print('\n___')
                                print('\nLISTA DE HABITACIONES DEL HOTEL | '+ hotel)
                                print('___\n')
                                print('{: <10} {: <15} {: <3} {: <3}'.format('Habitación', 'Tipo', 'Per.', 'Precio'))
                                for i in range(len(lista_hoteles.obtener(po).habitaciones)): 
                                    print(lista_hoteles.obtener(po).Hotel_infoHabitacion(i))
                            case 2: 
                                print('\n___')
                                print('\nMODIFICACION DE HABITACION DE HOTEL |'+ hotel)
                                print('___\n')
                                k = 1
                                for i in range(len(lista_hoteles.obtener(po).habitaciones)): 
                                    print("HABITACION {} : {}". format(k, lista_hoteles.obtener(po).Hotel_infoHabitacionLineal(i)))
                                    k += 1
        
                                try:
                                    o = int(input("Seleccione la habitacion que desea modificar: "))
                                    if o < 1: 
                                        raise IndexError
                                except:
                                    Accion("Error", "El numero de habitacion que selecciono no existe en el hotel o El ingreso solo admite numeros enteros. Por favor ingrese un numero correcto").guardar()
                                    print('\n( X ) Debe ingresar el numero de habitacion existente o un numero entero')
                                    break
                                id = input('\nIngrese el ID de la Habitacion: ')
                                tip = input('Ingrese el Tipo de la Habitacion: ')
                                try:
                                    Capacidad = int(input('Ingrese la Capacidad de la Habitacion: '))
                                    Precio = int(input('Ingrese el Precio de la Habitacion: '))
                                except ValueError: 
                                    Accion("Error", "El la capacidad o el precio solo admite numeros enteros. Por favor ingrese un valor correcto").guardar()
                                    print('\n( X ) Debe ingresar un valor correcto')
                                    break
                                ID = lista_hoteles.obtener(po).habitaciones[o-1].getId()
                                lista_hoteles.obtener(po).habitaciones[o-1].setHabitacion(id, tip, Capacidad, Precio)
                                for habitacion in habitaciones:
                                    if habitacion.getId () == ID:
                                        habitacion.setHabitacion(id, tip, Capacidad, Precio)                                        
                                print('\n!!Modificacion de habitacion exitosa')    
                            case 99:
                                bandi = False
            case 4: 
                Accion("Menu", "Se seleccionó la opcion de 'Ver reservaciones'").guardar()
                print('\n___')
                print('\nLISTADO DE RESERVACIONES DE HOTELES |')
                print('___\n')
                for hotel in lista_hoteles:
                    hotel.mostrar_lista_hoteles()
                Accion("operacion", "Se listaron las reservaciones").guardar()
            case 99: 
                Accion("Menu", "Se salio del menu 'Gestion de hoteles'").guardar()
                return 
                

def gestion_reservaciones():
    while True:

            print('___')
            print('\nMENÚ DE GESTIÓN DE RESERVACIONES |')
            print('___')
            print('0. Crear reservación')
            print('1. Eliminar reservación')
            print('2. Listar reservaciones por Hotel')
            print('3. Buscar reservación exitente')
            print('99. Salir')
        
            opcion = int(input('Seleccione una opción: '))
        

            match opcion:
                case 0: 
                    crearReserva()
                    Accion("Menu", "Se seleccionó la opcion de 'Eliminar reservación'").guardar()
                case 1:
                    Accion("Menu", "Se seleccionó la opcion de 'Crear reservación'").guardar()
                    lista_reservacion.ViewList()
                    try:
                        eliminacion = int(input('Seleccione el Numero de la reservación que desea eliminar: '))
                        if eliminacion-1 < 0: 
                            raise IndexError
                    except: 
                        Accion("Error", "El la reservacion que eligio no existe o ingreso algo que sea un numero. Por favor ingrese el numero de la opcion").guardar()
                        print('\n( X ) Debe ingresar un número de la opción o un numero entero')
                        break
                    lista_reservacion.Delete(eliminacion-1)
                    lista_reservacion.ViewList()
                    Accion("Sistema", "Eliminación de reserva exitosa").guardar()
                    print('!! Eliminación de reserva exitosa')
                case 2:
                    Accion("Menu", "Se seleccionó la opcion de 'Listar reservaciones por Hotel'").guardar()

                    print('\nLISTA DE RESERVACIONES | Hotel Gran Meliá Caracas\n')
                    lista_reservacion.Search_Reservacion("Hotel Gran MeliÃ¡ Caracas", 4)
                    Accion("operacion", "Se listaron las reservaciones del 'Hotel Gran Meliá Caracas'").guardar()


                    print('\nLISTA DE RESERVACIONES | Hotel JW Marriott Caracas\n')
                    lista_reservacion.Search_Reservacion("Hotel JW Marriott Caracas", 4)
                    Accion("operacion", "Se listaron las reservaciones del 'Hotel JW Marriott Caracas'").guardar()


                    print('\nLISTA DE RESERVACIONES | Hotel Hilton Caracas\n')
                    lista_reservacion.Search_Reservacion("Hotel Hilton Caracas", 4)
                    Accion("operacion", "Se listaron las reservaciones del 'Hotel Hilton Caracas'").guardar()
                
                case 3:
                    Accion("Menu", "Se seleccionó la opcion de 'Buscar reservación exitente'").guardar()

                    bandi=True
                    while bandi == True:
                        print('\n___')
                        print('\nMENÚ DE BUSQUEDA DE RESERVAS EXISTENTE |')
                        print('___')
                        print('0. IDN del cliente')
                        print('1. Rango de costo total de reservaciones')
                        print('2. Rango de fecha de entrada')
                        print('3. Rango de fecha de salida')
                        print('4. Tipo de habitacion')
                        print('99. Salir\n')
                        try:
                            op= int(input('Seleccione una opcion: '))
                        except ValueError: 
                            Accion("Error", "El menu de busqueda de reservaciones solo admite numeros enteros. Por favor ingrese el numero de la opcion").guardar()
                            print('\n( X ) Debe ingresar el número de la opción')
                            op = -1
                        match op:
                            case 0:
                                Accion("Menu", "Se seleccionó la opcion de 'IDN del cliente'").guardar()
                                IDN = int(input('\nIngrese el IDN del cliente: '))
                                print()
                                lista_reservacion.Search_Reservacion(IDN, 0)
                                Accion("Operacion", "Se listaron las reservaciones del cliente'{}'".format(IDN)).guardar()
                            case 1: 
                                Accion("Menu", "Se seleccionó la opcion de 'Rango de costo total de reservaciones'").guardar()
                                valor1 = int(input('\nIngrese el minimo de costo total: '))
                                valor2 = int(input('Ingrese el maximo de costo total: '))
                                print()
                                lista_reservacion.Search_Reservacion(None, 1, valor1, valor2)
                                Accion("Operacion", "Se listaron las reservaciones del rango {} al {}".format(valor1, valor2)).guardar()

                            case 2: 
                                Accion("Menu", "Se seleccionó la opcion de 'Rango de fecha de entrada'").guardar()
                                fechaEntrada1 = fecha(input("\nIndique el minimo de fecha de entrada (DD/MM/AAAA): "))
                                fechaEntrada2 = fecha(input("Indique el maximo de fecha de entrada (DD/MM/AAAA): "))
                                print()
                                lista_reservacion.Search_Reservacion(None, 2, fechaEntrada1, fechaEntrada2)
                                Accion("Operacion", "Se listaron las reservaciones del rango {} al {}".format(fechaEntrada1, fechaEntrada2)).guardar()
                            case 3:
                                Accion("Menu", "Se seleccionó la opcion de 'Rango de fecha de salida'").guardar()
                                fechaSalida1 = fecha(input("\nIndique el minimo de fecha de salida (DD/MM/AAAA): "))
                                fechaSalida2 = fecha(input("Indique el maximo de fecha de salida (DD/MM/AAAA): "))
                                print()
                                lista_reservacion.Search_Reservacion(None, 3, fechaSalida1, fechaSalida2)
                                Accion("Operacion", "Se listaron las reservaciones del rango {} al {}".format(fechaSalida1, fechaSalida2)).guardar()
                            case 4:
                                Accion("Menu", "Se seleccionó la opcion de 'Tipo de habitacion'").guardar()
                                print('\n___')
                                print('\nTIPO DE HABITACIÓN |')
                                print('___')
                                print('0. Standard')
                                print('1. Standard Doble')
                                print('2. Suite')
                                print('3. Deluxe\n')
                                try:
                                    o= int(input('Seleccione una opcion: '))
                                except ValueError: 
                                    Accion("Error", "El menu de busqueda de reservaciones solo admite numeros enteros. Por favor ingrese el numero de la opcion").guardar()
                                    print('\n( X ) Debe ingresar el número de la opción')
                                    o = -1
                                print()
                                match o:
                                    case 0:
                                        Accion("Menu", "Se seleccionó el tipo de habitacion 'Standard'").guardar()
                                        print('RESERVACION CON HABITACIONES DE TIPO Standard\n')
                                        lista_reservacion.Search_Reservacion("Standard", 5)
                                        Accion("operacion", "Se listaron las reservaciones de las habitaciones 'Standard'").guardar()
                                    case 1:
                                        Accion("Menu", "Se seleccionó el tipo de habitacion 'Standard Doble'").guardar()
                                        print('RESERVACION CON HABITACIONES DE TIPO Standard Doble\n')
                                        lista_reservacion.Search_Reservacion("Standard Doble", 5)
                                        Accion("operacion", "Se listaron las reservaciones de las habitaciones 'Standard Doble'").guardar()
                                    case 2:
                                        Accion("Menu", "Se seleccionó el tipo de habitacion 'Suite'").guardar()
                                        print('RESERVACION CON HABITACIONES DE TIPO Suite\n')
                                        lista_reservacion.Search_Reservacion("Suite", 5)
                                        Accion("operacion", "Se listaron las reservaciones de las habitaciones 'Suite'").guardar()
                                    case 3:
                                        Accion("Menu", "Se seleccionó el tipo de habitacion 'Deluxe'").guardar()
                                        print('RESERVACION CON HABITACIONES DE TIPO Deluxe\n')
                                        lista_reservacion.Search_Reservacion("Deluxe", 5)
                                        Accion("operacion", "Se listaron las reservaciones de las habitaciones 'Deluxe'").guardar()
                            case 99:
                                Accion("Menu", "Se salio del menu 'Busqueda de reservas existentes'").guardar()
                                bandi = False
                case 99:
                    Accion("Menu", "Se salio del menu 'Gestion de reservaciones'").guardar()
                    return
        


def reportes():
    print('\n\nMENU DE REPORTES | ' + hotel)
    print('___')
    print('0. Reservaciones por período según el precio total')
    print('1. Usuarios según el número de reservaciones que tengan realizadas')
    print('2. Reservaciones según la duración de estadía')
    print('3. Salir')
    
    opcion = int(input('Seleccione una opción: '))
    
    print('1. Ascendente')
    print('2. Descendente')
    orden = input("Seleccione el tipo de ordenamiento: ")
    
    match opcion:
        case 0:
            fechaInicial = fecha(input("Indique la fecha inicial (DD/MM/AAAA): "))
            fechaFinal = fecha(input("Indique la fecha final (DD/MM/AAAA): "))
            array = reservasPeriodo(fechaInicial, fechaFinal)
            
            if orden == "1":
                array = mergesort_RangoFechas_ASC(array)
                verReserervas(array)
                Accion("Menu", "Se seleccionó la opcion de 'Reservaciones por período según el precio total' de forma 'Ascendente' en el periodo de {} a {}".format(fechaInicial.strftime("%d/%m/%y"),fechaFinal.strftime("%d/%m/%y"))).guardar()
            elif orden == "2":
                array = mergesort_RangoFechas_DESC(array)
                verReserervas(array)
                Accion("Menu", "Se seleccionó la opcion de 'Reservaciones por período según el precio total' de forma 'Descendente' en el periodo de {} a {}".format(fechaInicial.strftime("%d/%m/%y"),fechaFinal.strftime("%d/%m/%y"))).guardar()
            elif default == "asc":
                array = mergesort_RangoFechas_ASC(array)
                verReserervas(array)
                Accion("Menu", "Se seleccionó la opcion de 'Reservaciones por período según el precio total' por defecto 'Ascendente' en el periodo de {} a {}".format(fechaInicial.strftime("%d/%m/%y"),fechaFinal.strftime("%d/%m/%y"))).guardar()
            elif default == "desc":
                array = mergesort_RangoFechas_DESC(array)
                verReserervas(array)
                Accion("Menu", "Se seleccionó la opcion de 'Reservaciones por período según el precio total' por defecto 'Descendente' en el periodo de {} a {}".format(fechaInicial.strftime("%d/%m/%y"),fechaFinal.strftime("%d/%m/%y"))).guardar()
            else:
                Accion("Error", "Por favor ingrese una opción válida, o configure correctamente el orden por defecto en el archivo de configuración").guardar()
                print("Por favor ingrese una opción válida, o configure correctamente el orden por defecto en el archivo de configuración")
                
        case 1:
            if orden == "1":
                array = shellsort_NoReservaciones_ASC(usuarios)
                verReserervas(array)
                Accion("Menu", "Se seleccionó la opcion de 'Usuarios según el número de reservaciones que tengan realizadas' de forma 'Ascendente'").guardar()
            elif orden == "2":
                array = shellsort_NoReservaciones_DESC(usuarios)
                verReserervas(array)
                Accion("Menu", "Se seleccionó la opcion de 'Usuarios según el número de reservaciones que tengan realizadas' de forma 'Descendente'").guardar()
            elif default == "asc":
                array = shellsort_NoReservaciones_ASC(usuarios)
                verReserervas(array)
                Accion("Menu", "Se seleccionó la opcion de 'Usuarios según el número de reservaciones que tengan realizadas' por defecto 'Ascendente'").guardar()
            elif default == "desc":
                array = shellsort_NoReservaciones_DESC(usuarios)
                verReserervas(array)
                Accion("Menu", "Se seleccionó la opcion de 'Usuarios según el número de reservaciones que tengan realizadas' por defecto 'Descendente'").guardar()
            else:
                Accion("Error", "Por favor ingrese una opción válida, o configure correctamente el orden por defecto en el archivo de configuración").guardar()
                print("Por favor ingrese una opción válida, o configure correctamente el orden por defecto en el archivo de configuración")
                
        case 2:

            if orden == "1":
                array = heapSort_Duracion_ASC(reservas)
                verReserervas(array)
                Accion("Menu", "Se seleccionó la opcion de 'Reservaciones según la duración de estadía' de forma 'Ascendente'").guardar()
            elif orden == "2":
                array = heapSort_Duracion_DESC(reservas)
                verReserervas(array)
                Accion("Menu", "Se seleccionó la opcion de 'Reservaciones según la duración de estadía' de forma 'Descendente'").guardar()
            elif default == "asc":
                array = heapSort_Duracion_ASC(reservas)
                verReserervas(array)
                Accion("Menu", "Se seleccionó la opcion de 'Reservaciones según la duración de estadía' por defecto 'Ascendente'").guardar()
            elif default == "desc":
                array = heapSort_Duracion_DESC(reservas)
                verReserervas(array)
                Accion("Menu", "Se seleccionó la opcion de 'Reservaciones según la duración de estadía' por defecto 'Descendente'").guardar()
            else:
                Accion("Error", "Por favor ingrese una opción válida, o configure correctamente el orden por defecto en el archivo de configuración").guardar()
                print("Por favor ingrese una opción válida, o configure correctamente el orden por defecto en el archivo de configuración")
        case 3:
            Accion("Menu", "Se salio del menu 'Reportes'").guardar()
            return

"""
Funcion principal
"""
def main():
    # Carga el archivo de configuracion
    cargarConfig()
    Accion("Sistema", "Se cargó la configuracion inicial").guardar()
    
    # Carga las habitaciones
    cargarHabitaciones()
    Accion("Sistema", "Se cargó la bases de datos de las habitaciones").guardar()
    Accion("Menu", "Se seleccionó la opcion de 'Cargar Seed'").guardar()
    cargarHoteles()
    cargarReservas()

    # Ciclo para mostrar el menu
    while True:

        # Imprime en la terminal las opciones del menu
        print('\n\nMENU PRINCIPAL | ' + hotel)
        print('___')
        # print('0. Cargar Seed')
        print('1. Crear Reserva')
        print('2. Ver reservas por periodo')
        print('3. Ordenar reservas por criterios en un periodo')
        print('4. Reportes')
        print('10. Ver todas las reservas')
        print('11. Ver todas los usuarios')
        print('12. Gestión de reservaciones')
        print('13. Gestión de hoteles')
        print('99. Salir')

        try:
            # Solicita al usuario la opcion y la escucha
            opcion = int(input('Seleccione una opción: '))

            # Ejecuta las fuciones segun el caso
            match opcion:
                # case 0:
                #     Accion("Menu", "Se seleccionó la opcion de 'Cargar Seed'").guardar()
                #     cargarHoteles()
                #     cargarReservas()
                case 1:
                    Accion("Menu", "Se seleccionó la opcion de 'Crear Reserva'").guardar()
                    crearReserva()
                case 2:
                    Accion("Menu", "Se seleccionó la opcion de 'Ver reservas por periodo'").guardar()
                    reservasPeriodo()
                case 3:
                    Accion("Menu", "Se seleccionó la opcion de 'Ordenar reservas por criterios en un periodo'").guardar()
                    ordenar()
                # case 4:
                #     ordenMultiple()
                case 4:
                    Accion("Menu", "Se seleccionó la opcion de 'Reportes'").guardar()
                    reportes()
                case 10:
                    Accion("Menu", "Se seleccionó la opcion de 'Ver todas las reservas'").guardar()
                    verReserervas(reservas)
                case 11:
                    Accion("Menu", "Se seleccionó la opcion de 'Ver todas los usuarios'").guardar()
                    verUsuarios()
                case 12:
                    try:
                        gestion_reservaciones()
                    except ValueError: 
                        Accion("Error", "El menu de gestion de reservaciones solo admite numeros enteros. Por favor ingrese el numero de la opcion").guardar()
                        print('\n( X ) Debe ingresar el número de la opción')
                        gestion_reservaciones()
                case 13:  
                    try:
                        gestion_hoteles()
                    except ValueError: 
                        Accion("Error", "El menu de gestion de hotelessolo admite numeros enteros. Por favor ingrese el numero de la opcion").guardar()
                        print('\n( X ) Debe ingresar el número de la opción')
                        gestion_hoteles()
                case 99:
                    Accion("SALIDA", "Se salió del sistema").guardar()
                    sys.exit()
        except ValueError:
            Accion("Error", "El menu solo admite numeros enteros. Por favor ingrese el numero de la opción").guardar()
            print('\n( X ) Debe ingresar el número de la opción')
        except IndexError:
            Accion("Error", "Indice fuera de rango").guardar()
            print('\n( X ) Indice fuera de rango')
main()