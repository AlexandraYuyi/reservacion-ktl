
# El archivo `gestionreservaciones` es para la clase de la lista entrelazada tipo Cola
# sobre la reservaciones de cada hotel

class Nodo: 
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None

class Cola: 
    __Longitud = 0

    def __init__(self):
        self.frente = None
        self.fin = None 

    def __Empty__(self): 
        return self.frente is None
    
    def Add(self, valor): 
        nodo_nuevo = Nodo(valor)
        if self.__Empty__():
            self.frente = nodo_nuevo
        else: 
            self.fin.siguiente= nodo_nuevo
        self.fin = nodo_nuevo
        self.__Longitud += 1

    def Delete(self, posicion=0, i=0): 
        if self.__Empty__():
            return None
        else:
            if posicion > self.__Longitud-1:
                print("Error")
                pass

            elif posicion != 0:
                nodo_temp = nodo_inicio = self.frente
                while i < posicion: 
                    self.frente = nodo_temp
                    nodo_temp = nodo_temp.siguiente
                    i+= 1
                self.frente.siguiente = nodo_temp.siguiente
                self.frente = nodo_inicio
            else: 
                self.frente = self.frente.siguiente
                
            if self.frente == None: 
                self.fin = None
            else:
                nodo_temp = self.frente
                while nodo_temp.siguiente != None: 
                    nodo_temp= nodo_temp.siguiente
                self.fin = nodo_temp

    __criterios = ["idn", "costoTotal", "fechaEntrada", "fechaSalida", "hotel", "tipo"]

    def Search_Reservacion(self, valor, i=0, valor1=0, valor2=0): 
        if self.__Empty__(): 
            return None
        else: 
            nodo_temp = self.frente
            while nodo_temp != None: 
                if i < 1: 
                    if getattr(nodo_temp.valor.usuario, self.__criterios[i])== valor:
                        print(nodo_temp.valor.infoLineal())
                elif i >= 1 and i <= 4:
                    if i >= 1 and i <= 3 : 
                        if getattr(nodo_temp.valor, self.__criterios[i])>= valor1 and getattr(nodo_temp.valor, self.__criterios[i]) <= valor2:
                            print(nodo_temp.valor.infoLineal())
                    else:
                        if getattr(nodo_temp.valor, self.__criterios[i])== valor:
                            print(nodo_temp.valor.infoLineal())
                else: 
                    if getattr(nodo_temp.valor.habitacion, self.__criterios[i])== valor:
                        print(nodo_temp.valor.infoLineal())
                        
                nodo_temp = nodo_temp.siguiente

    def ViewList(self):
        if self.__Empty__() is False:
            nodo_temp = self.frente
            print('\n_________')
            i = 1
            while nodo_temp != None:
                print("RESERVA", i , ': ' + nodo_temp.valor.infoLineal())
                i += 1
                nodo_temp = nodo_temp.siguiente
            print('‾‾‾‾‾‾‾‾‾')
