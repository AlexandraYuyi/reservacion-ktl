import random
from datetime import date, datetime
import json
import sys
from sortingmethods import *
from gestionreservaciones import Cola
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
hoteles = []

class Hotel:
    def __init__(self, nombre, direccion, numero):
        self.nombre = nombre
        self.direccion = direccion
        self.numero = numero
        self.reservaciones = []
        self.habitaciones = []

    # Método para añadir una reservación
    def añadir_reservacion(self, reservacion):
        self.reservaciones.append(reservacion)

    # Método para añadir una habitación
    def añadir_habitacion(self, habitacion):
        self.habitaciones.append(habitacion)

    def mostrar_lista_hoteles(hoteles):
        for hotel in hoteles:
            print(f"Hotel: {hotel.nombre}")
            print(f"Dirección: {hotel.direccion}")
            print(f"Número: {hotel.numero}")
            print(f"Reservas:")
            for reservacion in hotel.reservaciones:
                print(f"- Nombre: {reservacion.nombre}")
                print(f"- Fecha de inicio: {reservacion.fechaEntrada}")
                print(f"- Fecha de fin: {reservacion.fechaSalida}")
            print(f"Habitaciones:")
            for habitacion in hotel.habitaciones:
                print(f"- Número: {habitacion.id}")
                print(f"- Tipo: {habitacion.tipo}")

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
        self.longitud = 0
    def __len__(self):
        return self.longitud
    def __iter__(self):
        actual = self.cabeza
        while actual:
            yield actual.valor
            actual = actual.siguiente
    def agregar(self, valor):
        nuevo_nodo = Nodo(valor)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        self.longitud += 1
    def eliminar(self, valor):
        if self.cabeza is None:
            return False
        if self.cabeza.valor == valor:
            self.cabeza = self.cabeza.siguiente
            self.longitud -= 1
            return True
        actual = self.cabeza
        while actual.siguiente:
            if actual.siguiente.valor == valor:
                actual.siguiente = actual.siguiente.siguiente
                self.longitud -= 1
                return True
            actual = actual.siguiente
        return False
    def insertar(self, indice, valor):
        if indice < 0 or indice > self.longitud:
            raise IndexError("Índice fuera de rango")
        nuevo_nodo = Nodo(valor)
        if indice == 0:
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            for i in range(indice - 1):
                actual = actual.siguiente
            nuevo_nodo.siguiente = actual.siguiente
            actual.siguiente = nuevo_nodo
        self.longitud += 1
    def obtener(self, indice):
        if indice < 0 or indice >= self.longitud:
            raise IndexError("Índice fuera de rango")
        actual = self.cabeza
        for i in range(indice):
            actual = actual.siguiente
        return actual.valor
    def index(self, valor):
        actual = self.cabeza
        indice = 0
        while actual:
            if actual.valor == valor:
                return indice
            actual = actual.siguiente
            indice += 1
        raise ValueError("{} no está en la lista".format(valor))
    def pop(self, indice=None):
        if indice is None:
            indice = self.longitud - 1
        if indice < 0 or indice >= self.longitud:
            raise IndexError("Índice fuera de rango")
        if indice == 0:
            valor = self.cabeza.valor
            self.cabeza = self.cabeza.siguiente
            self.longitud -= 1
            return valor
        actual = self.cabeza
        for i in range(indice - 1):
            actual = actual.siguiente
        valor = actual.siguiente.valor
        actual.siguiente = actual.siguiente.siguiente
        self.longitud -= 1
        return valor
    def listar(self):
        actual = self.cabeza
        if self.cabeza is not None:
            while actual != None:
                print(actual.valor.marca)
                actual = actual.siguiente

# Función para añadir una nueva reservación a un hotel
def añadir_reservacion_a_hotel(hoteles, hotel, reservacion):
    hotel.añadir_reservacion(reservacion)

# Función para añadir una nueva habitación a un hotel
def añadir_habitacion_a_hotel(hoteles, hotel, habitacion):
    hotel.añadir_habitacion(habitacion)


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
        Construye los objetos de la clase Reserva.
        
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
    Getters de :class:`Reserva`
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
    dia = int(dia)
    mes = int(mes)
    ano = int(ano)

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
    Accion("Sistema", "Archivo de configuracion './config.json' cargado exitosamente").guardar()

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
                      " 1. JML Exclusive Hotel\n" + 
                      " 2. Resort Celeste\n" + "\n" +
                      "Su selección es: ")
        if hotel == "1":
            hotel = "JML Exclusive Hotel"
        else: 
            hotel = "Resort Celeste"
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
        telf = input("Indique su número telefónico: ")
        fechaEntrada = fecha(input("Indique la fecha de entrada (DD/MM/AAAA): "))
        fechaSalida = fecha(input("Indique la fecha de salida (DD/MM/AAAA): "))

        # Se llama a la funcion seleccionarHabitacion para poder escoger dentro de las habitaciones disponibles
        habitacion = seleccionarHabitacion(fechaEntrada, fechaSalida)

        usuarioNuevo = Usuario(nombre, idn, correo, telf)
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
            case 1:
                lista_reservacion.ViewList()
                eliminacion = int(input('Seleccione el Numero de la reservación que desea eliminar: '))
                lista_reservacion.Delete(eliminacion-1)
                lista_reservacion.ViewList()
                print('!!Eliminación de reserva exitosa')
            case 2:
                print('\nLISTA DE RESERVACIONES | JML Exclusive Hotel\n')
                lista_reservacion.Search_Reservacion("JML Exclusive Hotel", 4)

                print('\nLISTA DE RESERVACIONES | Resort Celeste\n')
                lista_reservacion.Search_Reservacion("Resort Celeste", 4)
            case 3:
                bandi=True
                while bandi == True:
                    print('\n___')
                    print('MENÚ DE BUSQUEDA DE RESERVAS EXISTENTE |')
                    print('___')
                    print('0. IDN del cliente')
                    print('1. Rango de costo total de reservaciones')
                    print('2. Rango de fecha de entrada')
                    print('3. Rango de fecha de salida')
                    print('4. Tipo de habitacion')
                    print('99. Salir\n')
                    op= int(input('Seleccione una opcion: '))
                    match op:
                        case 0:
                            IDN = int(input('\nIngrese el IDN del cliente: '))
                            print()
                            lista_reservacion.Search_Reservacion(IDN, 0)
                        case 1: 
                            valor1 = int(input('\nIngrese el minimo de costo total: '))
                            valor2 = int(input('Ingrese el maximo de costo total: '))
                            print()
                            lista_reservacion.Search_Reservacion(None, 1, valor1, valor2)

                        case 2: 
                            fechaEntrada1 = fecha(input("\nIndique el minimo de fecha de entrada (DD/MM/AAAA): "))
                            fechaEntrada2 = fecha(input("Indique el maximo de fecha de entrada (DD/MM/AAAA): "))
                            print()
                            lista_reservacion.Search_Reservacion(None, 2, fechaEntrada1, fechaEntrada2)
                        case 3: 
                            fechaSalida1 = fecha(input("\nIndique el minimo de fecha de salida (DD/MM/AAAA): "))
                            fechaSalida2 = fecha(input("Indique el maximo de fecha de salida (DD/MM/AAAA): "))
                            print()
                            lista_reservacion.Search_Reservacion(None, 3, fechaSalida1, fechaSalida2)
                        case 4:
                            print('\n___')
                            print('TIPO DE HABITACIÓN |')
                            print('___')
                            print('0. Standard')
                            print('1. Standard Doble')
                            print('2. Suite')
                            print('3. Deluxe\n')
                            o = int(input('Seleccione una opcion: '))
                            print()
                            match o:
                                case 0:
                                    print('RESERVACION CON HABITACIONES DE TIPO Standard\n')
                                    lista_reservacion.Search_Reservacion("Standard", 5)
                                case 1:
                                    print('RESERVACION CON HABITACIONES DE TIPO Standard Doble\n')
                                    lista_reservacion.Search_Reservacion("Standard Doble", 5)
                                case 2:
                                    print('RESERVACION CON HABITACIONES DE TIPO Suite\n')
                                    lista_reservacion.Search_Reservacion("Suite", 5)
                                case 3:
                                    print('RESERVACION CON HABITACIONES DE TIPO Standard\n')
                                    lista_reservacion.Search_Reservacion("Deluxe", 5)
                        case 99:
                            bandi = False
            case 99:
                return

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


# def ordenMultiple():
#     print('\n\nMENÚ DE CRITERIOS DE ORDENAMIENTO | ' + hotel)
#     print('___')
#     print('0. Capacidad de la Habitación')
#     print('1. Fecha de entrada')
#     print('2. Número de habitación')
#     print('3. Salir')
    
#     opcion1 = int(input('Seleccione su primer criterio: '))
#     opcion2 = int(input('Seleccione su segundo criterio: '))
    
#     fechaInicial = fecha(input("Indique la fecha inicial (DD/MM/AAAA): "))
#     fechaFinal = fecha(input("Indique la fecha final (DD/MM/AAAA): "))
    
#     orden = input("""Seleccione el tipo de ordenamiento:
# 1. Ascendente
# 2. Descendente
# """)
    
#     if opcion1 == 3 or opcion2 == 3:
#         return
#     else:
#         array = reservasPeriodo(fechaInicial, fechaFinal)

#         if orden == "1" or default == "asc":
#             array = quickSort_Multiple_ASC(array, opcion1, opcion2)
#             verReserervas(array)
#         elif orden == "2" or default == "desc":
#             array = quickSort_Multiple_DESC(array, opcion1, opcion2)
#             verReserervas(array)
#         else:
#             print("Por favor ingrese una opción válida, o configure correctamente el orden por defecto en el archivo de configuración")

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

    # Ciclo para mostrar el menu
    while True:

        # Imprime en la terminal las opciones del menu
        print('\n\nMENU PRINCIPAL | ' + hotel)
        print('___')
        print('0. Cargar Seed')
        print('1. Crear Reserva')
        print('2. Ver reservas por periodo')
        print('3. Ordenar reservas por criterios en un periodo')
        print('4. Reportes')
        # print('4. Ordenar reservas por múltiples criterios')
        print('10. Ver todas las reservas')
        print('11. Ver todas los usuarios')
        print('12. Gestion de reservaciones')
        print('99. Salir')

        try:
            # Solicita al usuario la opcion y la escucha
            opcion = int(input('Seleccione una opción: '))

            # Ejecuta las fuciones segun el caso
            match opcion:
                case 0:
                    Accion("Menu", "Se seleccionó la opcion de 'Cargar Seed'").guardar()
                    cargarReservas()
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
                    gestion_reservaciones()
                case 99:
                    Accion("SALIDA", "Se salió del sistema").guardar()
                    sys.exit()
        except ValueError:
            Accion("Error", "El menu solo admite numeros enteros. Por favor ingrese el numero de la opción").guardar()
            print('\n( X ) Debe ingresar el número de la opción')

main()