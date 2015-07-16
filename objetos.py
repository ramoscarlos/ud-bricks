#/usr/bin/env python
# -*- coding: utf-8 -*-

"Módulo con los objetos necesarios para el juego."

import pygame as p
from comun import WIDTH, HEIGHT, cargar_imagen

class Pelota(p.sprite.Sprite):
    "Sprite de la pelota, encargado de toda sus operaciones."
    def __init__(self):
        "Carga la imagen de la pelota y establece las condiciones iniciales."
        p.sprite.Sprite.__init__(self)
        self.image = cargar_imagen("pelota.png", True)
        self.rect = self.image.get_rect()
        self.speed = [3, 3]
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        
    def actualizar(self):
        "Mueve la pelota dentro de la pantalla."
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed[0] = -self.speed[0]
        if self.rect.top <= 0:
            self.speed[1] = -self.speed[1]
        self.rect.move_ip(self.speed)
        
    def colision(self, objeto):
        "Detecta colisiones con otro objeto."
        if self.rect.colliderect(objeto.rect):
            self.speed[1] = -self.speed[1]
            
    def colisionMultiple(self, muro):
        "Detecta colisión con otros objetos."
        ladrillo = self.rect.collidelist(muro)
        if ladrillo != -1:
            if (self.rect.centerx < muro[ladrillo].left or 
                self.rect.centerx > muro[ladrillo].right):
                self.speed[0] = -self.speed[0]
            else:
                self.speed[1] = -self.speed[1]
            muro.pop(ladrillo)
            return 10
        return 0
            
    def se_salio(self, paleta):
        "Detecta si la pelota salió de la pantalla."
        if self.rect.top >= HEIGHT:
            self.rect.centerx = paleta.centerx
            self.rect.centery = paleta.centery - 24
            return True
        return False


class Jugador(p.sprite.Sprite):
    "Sprite del jugador, encargado de toda sus operaciones."
    def __init__(self):
        "Carga la imagen del jugador y establece las condiciones iniciales."
        p.sprite.Sprite.__init__(self)
        self.image = cargar_imagen("paleta.png", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT - 40
        self.speed = [3, 3]
        
    def mover(self, tecla):
        "Mueve la paleta del jugador en la pantalla."
        if tecla == p.K_LEFT:
            self.speed = [-15, 0]
        elif tecla == p.K_RIGHT:
            self.speed = [15, 0]
        else:
            self.speed = [0, 0]      
        self.rect.move_ip(self.speed)
        self.verificarLimites()

    def moverConAcelerometro(self, valor):
        # Conversión del valor en cadena a un valor flotante.
        try:
            valor = -float(valor)
        except:
            valor = 0
        if abs(valor) < 15:
            valor = 0
        else:
            valor = valor / 2
        self.speed = [valor, 0]
        self.rect.move_ip(self.speed)
        self.verificarLimites()

    def verificarLimites(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH


class Muro(p.sprite.Sprite):
    "Sprite del Muro, encargado generar todos los ladrillos."
    def __init__(self, num_bloques = 80):
        "Carga la imagen del ladrillo y declara variables necesarias."
        p.sprite.Sprite.__init__(self)
        self.image = cargar_imagen("ladrillo.jpg")
        self.rect = self.image.get_rect()
        self.ladrillos = []
        self.construir(num_bloques)
        
    def construir(self, num_bloques):
        "Construye un muro de num_bloques bloques."
        #Posicion inicial (lugar del primer bloque)
        pos_x = 0
        pos_y = 16
        for i in range(num_bloques):
            #Si nos pasamos del largo de la pantalla,
            if pos_x >= WIDTH:
                pos_x = 0               #Regresar a la orilla izquierda,
                pos_y += self.rect.h    #y bajar un "renglon".
            #Agregar un nuevo bloque.
            self.ladrillos.append(self.rect)
            #Y moverlo a su lugar correspondiente.
            self.ladrillos[i] = self.ladrillos[i].move(pos_x, pos_y)
            #Actualizar la posicion para el proximo ladrillo.
            pos_x += self.rect.w
