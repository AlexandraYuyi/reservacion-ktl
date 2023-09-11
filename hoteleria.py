import random
from datetime import date, datetime
import json
import sys

# Almacena todas las reservas activas en la aplicación (tempDB)
reservas = []

# Almacena todas las habitaciones activas de la aplicación (tempDB)
habitaciones = []

# Almacena todas las habitaciones activas de la aplicación (tempDB)
usuarios = []

# Almacena todas las reservas dentre de un periodo (tempDB)
reservasPeriodoDB = []

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

    def __init__(self, usuario, habitacion, fechaEntrada, fechaSalida):
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
        self.costoTotal = self.duracion.days * self.habitacion.getPrecio()

    def info(self):
        """
        Devuelve le información del objeto de forma imprimible por consola.
        """ 
        return "ID: {:0>5}\n Nombres: {}\n Habitacion: {}\n Entrada: {}\n Salida: {}\n Duración: {} días\n\n TOTAL: {}$".format(self.id, self.usuario.getNombre(), self.habitacion.getId(), self.fechaEntrada.strftime("%A %d. %B %Y"), self.fechaSalida.strftime("%A %d. %B %Y"), self.duracion.days, self.costoTotal)

    def infoLineal(self):
        """
        Devuelve le información del objeto de forma imprimible en una sola linea por consola.
        """ 
        return "ID: {:0>5}, Nombres: {}, Habitacion: {}, Entrada: {}, Salida: {}, Duración: {} días, TOTAL: {}$".format(self.id, self.usuario.getNombre(), self.habitacion.getId(), self.fechaEntrada.strftime("%d/%m/%y"), self.fechaSalida.strftime("%d/%m/%y"), self.duracion.days, self.costoTotal)

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

"""
Funcion que carga todas las habitaciones disponibles en el hotel
"""
def cargarHabitaciones():
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
    return

"""
Funcion que carga reservas de prueba
"""
def cargarReservas():
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
                reserva = Reserva(usuario, habitacionId, fechaEntrada, fechaSalida)

                # Se agrega la reserva a la tempDB0
                reservas.append(reserva)
                usuario.setReservacion()

        if bandUsuario == 0:
            usuarioNuevo = Usuario(nombre, idn, correo, telf)
            usuarios.append(usuarioNuevo)

            # Se construye el objeto del tipo Reserva
            reserva = Reserva(usuarioNuevo, habitacionId, fechaEntrada, fechaSalida)

            # Se agrega la reserva a la tempDB0
            reservas.append(reserva)
            usuarioNuevo.setReservacion()

    print('\n!!! Archivo cargado exitosamente')
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

    # Solicita la seleccion de habitacion
    index = int(input('Seleccione una habitacion: '))

    # Asigna la habitacion seleccionada a una variable
    habitacionSeleccionada = habitacionesDiponibles[index]
    
    # Retorna el objeto de la habitacion seleccionada
    return habitacionSeleccionada

"""
Funcion que crea las reservas
"""
def crearReserva():
    
    # Solicita al usuario los datos necesarios y los almacena en sus respectivas variables
    print('')
    idn = int(input("Indique su número de cédula: "))

    for usuario in usuarios:
        if usuario.getIDN() == idn:
            fechaEntrada = fecha(input("Indique la fecha de entrada (DD/MM/AAAA): "))
            fechaSalida = fecha(input("Indique la fecha de salida (DD/MM/AAAA): "))

            # Se llama a la funcion seleccionarHabitacion para poder escoger dentro de las habitaciones disponibles
            habitacion = seleccionarHabitacion(fechaEntrada, fechaSalida)

            # Crea un nuevo objeto de la clase reserva
            reserva = Reserva(usuario, habitacion, fechaEntrada, fechaSalida)

            # Se agrega la reserva a la tempDB
            reservas.append(reserva)
            usuario.setReservacion()

            print('\n_________')
            # Imprime en la terminal los detalles de la reserva realizada.
            print("RESERVA:\n",reserva.info())
            print('‾‾‾‾‾‾‾‾‾')

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
    reserva = Reserva(usuarioNuevo, habitacion, fechaEntrada, fechaSalida)

    # Se agrega la reserva a la tempDB
    reservas.append(reserva)
    usuario.setReservacion()

    print('\n_________')
    # Imprime en la terminal los detalles de la reserva realizada.
    print("RESERVA:\n",reserva.info())
    print('‾‾‾‾‾‾‾‾‾')

    print('\n!!! Reserva realizada exitosamente')
    return

"""
Funcion que permite listar todas las reservas
"""
def verReserervas():
    print('\n_________')

    # Variable auxiliar de conteo
    i = 1

    # Recorre todas las reservas
    for reserva in reservas:

        # Imprime en la terminal todas las reservas formateadas
        print("RESERVA", i , ': ', reserva.infoLineal())
        i += 1
    print('\nTOTAL: ', len(reservas), 'reservas')
    print('‾‾‾‾‾‾‾‾‾')
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

"""
Funcion principal
"""
def main():
    # Carga el archivo de configuracion
    cargarConfig()

    # Carga las habitaciones
    cargarHabitaciones()

    # Ciclo para mostrar el menu
    while True:

        # Imprime en la terminal las opciones del menu
        print('\n\nMENU PRINCIPAL | ' + hotel)
        print('___')
        print('0. Cargar Seed')
        print('1. Crear Reserva')
        print('2. Reserva Periodo')
        print('10. Ver todas las reservas')
        print('11. Ver todas los usuarios')
        print('99. Salir')

        # Solicita al usuario la opcion y la escucha
        opcion = int(input('Seleccione una opción: '))

        # Ejecuta las fuciones segun el caso
        match opcion:
            case 0:
                cargarReservas()
            case 1:
                crearReserva()
            case 2:
                reservasPeriodo()
            case 10:
                verReserervas()
            case 11:
                verUsuarios()
            case 99:
                sys.exit()
main()