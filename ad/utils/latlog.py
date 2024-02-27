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
from numpy import sin, cos, arccos, pi, round
import ad.utils.contants as co
import operator


def rad2deg(radians):
    '''
    Funcion para convertir radianes a grados
    :param radians:
    :return: degrees
    '''
    degrees = radians * 180 / pi
    return degrees


def deg2rad(degrees):
    '''
    Funcion para convertir grados a radianes
    :param degrees:
    :return: degrees
    '''
    radians = degrees * pi / 180
    return radians


def getDistanceBetweenPoints(latitude1, longitude1, latitude2, longitude2):
    '''
    Funcion que obtiene el calculo de la distancia de una coordenada respecto a otra dadas la latitud y longitud
    :param latitude1:
    :param longitude1:
    :param latitude2:
    :param longitude2:
    :return:
    '''
    theta = longitude1 - longitude2
    distance = 60 * 1.1515 * rad2deg(
        arccos((sin(deg2rad(latitude1)) * sin(deg2rad(latitude2))) + (cos(deg2rad(latitude1)) * cos(deg2rad(latitude2)) * cos(deg2rad(theta))))
    )
    return round(distance * 1.609344, 2)


def calculadist(lat1, long1, index, size):
    '''
    Funcion para obtener una lista de AP mas proximas a una coordenada dada
    :param lat1:
    :param long1:
    :param index:
    :param size:
    :return:
    '''
    lstret, dicdist = [], {}
    flag = False
    co.log.debug("Coordenada dada[lat>> {}  lon>> {}]".format(lat1, long1))
    try:
        for ap in co.hascoor:
            dicdist[ap] = getDistanceBetweenPoints(lat1, long1, co.hascoor[ap].get('latitud'), co.hascoor[ap].get('longitud'))
        lstsort = sorted(dicdist.items(), key=operator.itemgetter(1), reverse=False)
        lsttmp = lstsort[index:index+size]
        co.log.debug("Lista de Distancias\n {}".format(lsttmp))
        for element in lsttmp:
            lstret.append(co.hascoor[element[0]])
        flag = True
    except Exception as error:
        co.log.error(error, exc_info=True)
    return [flag, lstret]
