class Nodo: 
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None
        
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

    def Hotel_infoLineal(self): 
        return "Nombre del Hotel: {}, Dirrecion: {}, Numero de Telefono {}, Numero de Reservaciones {}".format(self.nombre, self.direccion, self.numero, len(self.reservaciones))
    
    def Hotel_infoHabitacion(self, i):
        return "{: <10} {: <16} {: <3} {: >3}$".format(self.habitaciones[i].id, self.habitaciones[i].tipo, self.habitaciones[i].capacidad, self.habitaciones[i].precio)
    
    def Hotel_infoHabitacionLineal(self, i):
        return "ID:{}, Tipo: {}, Capacidad: {}, Precio: {}$".format(self.habitaciones[i].id, self.habitaciones[i].tipo, self.habitaciones[i].capacidad, self.habitaciones[i].precio)
    
    def mostrar_lista_hoteles(self):
            print(f"Hotel: {self.nombre}")
            print(f"Dirección: {self.direccion}")
            print(f"Número: {self.numero}")
            print(f"Reservas:\n")
            for reserva in self.reservaciones:
                print(f"- Nombre: {reserva.usuario.nombre}")
                print(f"- Fecha de inicio: {reserva.fechaEntrada}")
                print(f"- Fecha de fin: {reserva.fechaSalida}\n")
            print(f"\nHabitaciones:\n")
            for habitacion in self.habitaciones:
                print(f"- Número: {habitacion.id}")
                print(f"- Tipo: {habitacion.tipo}\n")

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
    def obtener(self, indice, i=0):
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
                print(actual.valor.nombre)
                actual = actual.siguiente
    