# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Title: Data pipeline
# Author:  Enrique Miranda
# Status: Desarrollo
# Type: Consola
# Created: 25-Febrero-2020
# Python-Version:3.8.0
# Post-History:

#  Desarrollo para: Arkon Data

# Paqueteria de aplicacion
from ad.db.sqlite import ConexionDB
import ad.log.logger as log
import ad.utils.contants as co
import sys
from flask import Flask

co.app = Flask(__name__) # Aplicacion que correra en el Servidor

import ad.services.LoadServices  # Se cargan los servicios que estaran disponibles en el Servidor
co.log = log.logapi

# Conexion a Base de Datos SQLite
co.condb = ConexionDB("./database/datapipeline.db")
co.condb.creaconexion()
co.condb.etlccv()


if __name__ == '__main__':
    from waitress import serve

    print("*------------------D A T A  -  P I P E L I N E -----------------------------*")
    print("*             _              _        _      ____                           *")
    print("*            / \     _ __   (_)      / \    |  _ \                          *")
    print("*           / _ \   | '_ \  | |     / _ \   | | | |                         *")
    print("*          / ___ \  | |_) | | |    / ___ \  | |_| |                         *")
    print("*         /_/   \_\ | .__/  |_|   /_/   \_\ |____/                          *")
    print("*                   |_|                                                     *")
    print("*---------------------------------------------------------------------------*")
    print("| - Modulo: " + co.MODULO + "                                                           |")
    print("| - Revision:" + co.REVISION + "                  Version: " + co.VERSION + "             |")
    print("*---------------------------------------------------------------------------*")
    print(sys.version)

    print("\n** SERVIDOR INCIALIZADO ***".format(co.c_err))
    #Se lanza el Servidor
    serve(co.app, host="0.0.0.0", port=8000)
