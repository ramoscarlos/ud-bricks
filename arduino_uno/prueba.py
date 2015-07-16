#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo de prueba de transmisión y recepción de datos con el Arduino UNO.
"""

import time
from arduino_uno import ArduinoUNO

def prueba():
    "Prueba de lectura del puerto serial."
    puerto  = "/dev/ttyACM0"
    baudios = 9600
    arduino = ArduinoUNO(puerto, baudios)
    # Inicio del ciclo de lectura.
    print("Iniciando lectura de datos desde Arduino.")
    while True:
        print(arduino.leer())

if __name__ == "__main__":
    prueba()