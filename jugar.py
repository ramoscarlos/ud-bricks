#/usr/bin/env python
# -*- coding: utf-8 -*-

"Script para ejecutar el juego."

from g_escenas import Director
from escenas import EscenaInicio

def main():
    "Ejecutar el juego."
    director = Director("UD Bricks v0.2")
    director.ejecutar(EscenaInicio(), 60)

if __name__ == "__main__":
    main()
