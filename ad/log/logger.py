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
import logging.config

logging.config.fileConfig('./cfg/ConfigLog.ini')
modulo = "ApiAD"
log = logging.getLogger(modulo)
logapi = logging.getLogger()