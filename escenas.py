#/usr/bin/env python
# -*- coding: utf-8 -*-

"Tutorial de Pygame: Creando un clon de Breakout."

import pygame as p
from comun import WIDTH, HEIGHT, PANTALLA, cargar_imagen, Texto
from objetos import Jugador, Muro, Pelota
from g_escenas import Escena
# Agregando interacción con Arduino.
from arduino_uno.arduino_uno import ArduinoUNO


class EscenaJuego(Escena):
    "Clase que define la escena principal del videojuego."
    def __init__(self):
        "Inicialización de las variables del videojuego."
        Escena.__init__(self)
        self.fondo = cargar_imagen("fondo.jpg")
        self.pelota = Pelota()
        self.jugador = Jugador()
        self.muro = Muro()
        self.puntos = 0
        self.puntuacion = Texto("Puntos: ")
        self.vidas = 3
        self.t_vidas = Texto("Vidas: ")
        # Configuracion
        p.key.set_repeat(1, 25)
        # Conexión con Arduino UNO.
        puerto  = "COM3"
        baudios = 9600
        try:
            self.arduino = ArduinoUNO(puerto, baudios)
            self.arduino.leer()
        except:
            self.arduino = None
        
    def leer_eventos(self, eventos):
        "Atando eventos a los objetos."
        for evento in eventos:
            if evento.type == p.KEYDOWN:
                self.jugador.mover(evento.key)
        # Lectura de datos de Arduino.
        if self.arduino:
            self.jugador.moverConAcelerometro(self.arduino.leer())
        
    def actualizar(self):
        "Actualiza los objetos del juego."
        self.pelota.actualizar()
        self.pelota.colision(self.jugador)
        self.puntos += self.pelota.colisionMultiple(self.muro.ladrillos)
        self.vidas  -= self.pelota.se_salio(self.jugador.rect)
        if self.vidas == 0:
            self.cambiar_escena(EscenaJuegoTerminado(self.puntos))

    def dibujar(self, pantalla):
        "Dibujar objetos en pantalla."
        pantalla.blit(self.fondo, (0, 0))
        pantalla.blit(self.puntuacion.mostrar(str(self.puntos)), (0, 0))
        pantalla.blit(self.t_vidas.mostrar(str(self.vidas)), (560, 0))
        pantalla.blit(self.pelota.image, self.pelota.rect)
        pantalla.blit(self.jugador.image, self.jugador.rect)
        for i in range(len(self.muro.ladrillos)):
            pantalla.blit(self.muro.image, self.muro.ladrillos[i])


class EscenaJuegoTerminado(Escena):
    "Escena ejeutada tras perder el juego."
    def __init__(self, puntos):
        "Inicializar Escena de Juego Terminado."
        Escena.__init__(self)
        self.fondo = cargar_imagen("terminado.png")
        self.terminado = Texto("Juego Terminado", tamano = 72)
        self.puntos = Texto("Puntos: " + str(puntos), tamano = 48)
        self.reiniciar = Texto("[F5] Reiniciar", tamano = 36)
        self.salir = Texto("[ESC] Salir", tamano = 36)
        
    def leer_eventos(self, eventos):
        "Redirecciona a la pantalla adecuada."
        for evento in eventos:
            if evento.type == p.KEYDOWN:
                if evento.key == p.K_F5:
                    self.cambiar_escena(EscenaJuego())

    def dibujar(self, pantalla):
        "Mostrar pantalla de juego terminado."
        pantalla.blit(self.fondo, (0, 0))
        pantalla.blit(self.terminado.mostrar(), 
            ((WIDTH-self.terminado.rect.w)/2, (HEIGHT-self.terminado.rect.h)/2)
        )
        pantalla.blit(self.puntos.mostrar(), 
            ((WIDTH-self.puntos.rect.w)/2, HEIGHT/2+self.puntos.rect.h)
        )
        pantalla.blit(self.reiniciar.mostrar(), 
            (10, HEIGHT-self.reiniciar.rect.h-10)
        )
        pantalla.blit(self.salir.mostrar(), 
            (WIDTH-self.salir.rect.w-10, HEIGHT-self.salir.rect.h-10)
        )
        
class EscenaInicio(Escena):
    "Escena ejeutada tras perder el juego."
    def __init__(self):
        "Inicializar Escena de Juego Terminado."
        Escena.__init__(self)
        self.fondo = cargar_imagen("inicial.jpg")
        self.titulo = Texto("UD Bricks", tamano = 72)
        self.iniciar = Texto("[F5] Iniciar Juego", tamano = 36)
        self.salir = Texto("Salir [ESC]", tamano = 36)
        
    def leer_eventos(self, eventos):
        "Redirecciona a la pantalla adecuada."
        for evento in eventos:
            if evento.type == p.KEYDOWN:
                if evento.key == p.K_F5:
                    self.cambiar_escena(EscenaJuego())

    def dibujar(self, pantalla):
        "Mostrar pantalla de juego terminado."
        pantalla.blit(self.fondo, (0, 0))
        pantalla.blit(self.titulo.mostrar(), 
            ((WIDTH-self.titulo.rect.w)/2, (HEIGHT-self.titulo.rect.h)/2)
        )
        pantalla.blit(self.iniciar.mostrar(), 
            (10, HEIGHT-self.iniciar.rect.h-10)
        )
        pantalla.blit(self.salir.mostrar(), 
            (WIDTH-self.salir.rect.w-10, HEIGHT-self.salir.rect.h-10)
        )
