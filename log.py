from datetime import date, datetime
import os

class Accion:
    def __init__(self, tipo, mensaje):
        self.date = datetime.now()
        self.tipo = tipo.upper()
        self.mensaje = mensaje

    def info(self):
        """
        Devuelve le información del objeto de forma imprimible por consola.
        """ 
        return "{} | {} - {}\n".format(self.date.strftime("%d/%m/%y %H:%M:%S.%f"), self.tipo, self.mensaje)
    
    def guardar(self):
        # Agregamos la nueva acción a la pila
        if not os.path.exists("log.txt"):
            open("log.txt", "x").close
            with open("log.txt", "r+") as f:
                contenido = f.read()
                f.seek(0, 0)
                f.write("{} | {} - {}\n".format(self.date.strftime("%d/%m/%y %H:%M:%S.%f"), self.tipo, self.mensaje).rstrip('\r\n') + '\n' + contenido)

        else:
            with open("log.txt", "r+") as f:
                contenido = f.read()
                f.seek(0, 0)
                f.write("{} | {} - {}\n".format(self.date.strftime("%d/%m/%y %H:%M:%S.%f"), self.tipo, self.mensaje).rstrip('\r\n') + '\n' + contenido)