#/usr/bin/env python
# -*- coding: utf-8 -*-

"Funciones y variables comunes para los videojuegos."

import os
import pygame as p
 
WIDTH    = 640
HEIGHT   = 480
PANTALLA = (WIDTH, HEIGHT)
 
def cargar_imagen(nombre, alpha= False, directorio= "imagenes"):
    "Cargar imágenes del juego."
    ruta = os.path.join(directorio, nombre)
    try:
        imagen = p.image.load(ruta)
    except:
        print("No se puede cargar la imagen: ", ruta)
        raise
        
    if alpha == True:
        imagen = imagen.convert_alpha()
    else:
        imagen = imagen.convert()
    return imagen

class Texto():
    "Crea un texto para mostrar en pantalla."
    def __init__(
        self, predeterminado = "", tamano = 24, fuente = None, color = (0, 0, 0)
    ):
        "Inicializa el texto."
        self.fuente = p.font.Font(fuente, tamano)
        self.default = predeterminado
        self.texto = None
        self.rect = None
        self.color = color
        self.mostrar()
        
    def mostrar(self, cadena = ""):
        "Regresa el texto a mostrar."
        self.texto = self.fuente.render(self.default + cadena, True, self.color)
        self.rect = self.texto.get_rect()
        return self.texto
