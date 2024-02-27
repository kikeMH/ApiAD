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

global CO_USER, CO_PASS
global cfg, log, app, condb

VERSION = '1.0.0.0'
REVISION = '25/02/2024 10:22'
MODULO = "ApiAD"
c_rx = 0
c_tx = 0
c_err = 0
hascoor = {}
dQuery = {
        '/ad/getAp.id': "select id, programa, fecha_instalacion, latitud, longitud, colonia, alcaldia from AD_APWIFI_CDMX where id='{}'",
        '/ad/getAp.pag': "select id, programa, fecha_instalacion, latitud, longitud, colonia, alcaldia from AD_APWIFI_CDMX LIMIT {} OFFSET {}",
        '/ad/getAp.pag.col': "select id, programa, fecha_instalacion, latitud, longitud, colonia, alcaldia from AD_APWIFI_CDMX where colonia='{}' LIMIT {} OFFSET {}"
        }

