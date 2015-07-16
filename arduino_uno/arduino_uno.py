#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo que contiene una clase para la conexión con una tarjeta Arduino UNO por
medio del puerto serial.
"""

from serial import Serial

class ArduinoUNO(Serial):
    """
    Clase para la conexión con la tarjeta Arduino UNO, derivada de la clase
    Serial para entrablar comunicación.
    """
    def __init__(self, puerto, baudios, **args):
        "Inicia la conexión con el puerto serial."
        try:
            super(ArduinoUNO, self).__init__(
                port = puerto, baudrate = baudios, **args)
        except:
            print("No se pudo establecer conexión en el puerto especificado.")
        
    def escribir(self, datos=None):
        "Envía información a la tarjeta."
        self.write(datos)
        
    def leer(self):
        "Recibe los datos enviados por la tarjeta Arduino."
        resultado = self.readline().strip()
        return resultado
        
    def desconectar(self):
        "Termina la conexión con el puerto serial."
        self.close()