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
from flask import jsonify, abort
from flask import request, Response, make_response
import ad.utils.contants as co
import ad.utils.latlog as ll
import re


@co.app.route('/pingserver', methods=['GET'])
def my_route():
    index = request.args.get('index', default=1, type=int)
    size = request.args.get('size', default=5, type=int)
    return jsonify({'index': index, "size": size})


# Servicio para Consultar la información de un punto dado su ID
@co.app.route('/ad/getApid', methods=['POST'])
def get_ap():
    global condb
    dUser = {}
    try:
        if request.json.get('id') is not None:
            apid = request.json.get('id')
            lstDat = co.condb.select(co.dQuery.get('/ad/getAp.id').format(apid))
            if lstDat[0]:
                if len(lstDat[1]) > 0:
                    for regAp in lstDat[1]:
                        dUser['id'] = regAp[0]
                        dUser['programa'] = regAp[1]
                        dUser['fecha_instalacion'] = regAp[2]
                        dUser['latitud'] = regAp[3]
                        dUser['longitud'] = regAp[4]
                        dUser['colonia'] = regAp[5]
                        dUser['alcaldia'] = regAp[5]
                    response = jsonify({'ap': dUser, "errorMessage": ""})
                    co.log.info(response)
                    return response
                else:
                    codError, codHTTP = 2, 422
                    msgError = "No existe el access point [{}] registrado en Base de Datos".format(apid)
            else:
                codError, codHTTP = 2, 422
                msgError = lstDat[1].__str__()
        else:
            codError, codHTTP = 2, 400
            msgError = "Campo [id] requerido en la solicitud"
    except Exception as error:
        codError, codHTTP = 2, error.code
        msgError = error.description

    if re.search("connection|conexión", msgError) is not None:
        codHTTP = 500
    print("Ocurrio un problema en el Servicio de Consulta de access point  >>> {} [Cod HTTP {}]".format(msgError, codHTTP))
    co.log.error("Ocurrio un problema en el Servicio de Consulta de access point  >>> {} [Cod HTTP {}]".format(msgError, codHTTP))
    response = make_response(jsonify(errorCode=codError, errorMessage=msgError), codHTTP)
    abort(response)


# Servicio para Obtener una lista paginada de puntos de acceso WiFi
#               Obtener una lista paginada de puntos de acceso dada una colonia.
@co.app.route('/ad/getAppag', methods=['POST'])
def get_appag():
    global condb
    dAp = {}
    lstAps = []
    try:
        index = request.json.get('index')
        size = request.json.get('size')
        colonia = request.json.get('colonia')
        if (index is not None) and (size is not None):
            if (0 < int(index) <= 1000) and (0 < int(size) <= 100):  # Validacion de parametros
                if colonia is None:
                    lstDat = co.condb.select(co.dQuery.get('/ad/getAp.pag').format(int(size), int(index)))
                else:
                    lstDat = co.condb.select(co.dQuery.get('/ad/getAp.pag.col').format(colonia, int(size), int(index)))
                if lstDat[0]:
                    if len(lstDat[1]) > 0:
                        for regAp in lstDat[1]:
                            dAp['id'] = regAp[0]
                            dAp['programa'] = regAp[1]
                            dAp['fecha_instalacion'] = regAp[2]
                            dAp['latitud'] = regAp[3]
                            dAp['longitud'] = regAp[4]
                            dAp['colonia'] = regAp[5]
                            dAp['alcaldia'] = regAp[5]
                            lstAps.append(dAp)
                            dAp = {}
                    response = jsonify({'aps': lstAps, "errorMessage": ""})
                    co.log.info(response)
                    return response
                else:
                    codError, codHTTP = 2, 422
                    msgError = lstDat[1].__str__()
            else:
                codError, codHTTP = 2, 400
                msgError = "Parametros incorrectos de paginado >> index:{} size:{}".format(index, size)
        else:
            codError, codHTTP = 2, 400
            msgError = "Parametros incorrectos de paginado >> index:{} size:{}".format(index, size)
    except Exception as error:
        msgError = error.description
        codError, codHTTP = 2, error.code

    if re.search("connection|conexión", msgError) is not None:
        codHTTP = 500
    print("Ocurrio un problema en el Servicio de Consulta de access point  >>> {} [Cod HTTP {}]".format(msgError, codHTTP))
    co.log.error("Ocurrio un problema en el Servicio de Consulta de access point  >>> {} [Cod HTTP {}]".format(msgError, codHTTP))
    response = make_response(jsonify(errorCode=codError, errorMessage=msgError), codHTTP)
    abort(response)


# Servicio para Obtener una lista paginada de puntos de acceso WiFi
@co.app.route('/ad/getAppagll', methods=['POST'])
def get_appaglatlong():
    global condb
    codError, codHTTP, msgError = 9, 500, ''
    try:
        index = request.json.get('index')
        size = request.json.get('size')
        latitud = request.json.get('latitud')
        longitud = request.json.get('longitud')
        if (index is not None) and (size is not None):
            if (0 < int(index) <= 1000) and (0 < int(size) <= 100):  # Validacion de parametros
                if latitud is not None and longitud is not None:
                    lstDat = ll.calculadist(latitud, longitud, index, size)
                    if lstDat[0]:
                        response = jsonify({'aps': lstDat[1], "errorMessage": ""})
                        co.log.info(response)
                        return response
                    else:
                        codError, codHTTP = 2, 422
                        msgError = lstDat[1].__str__()
            else:
                codError, codHTTP = 2, 400
                msgError = "Parametros incorrectos de paginado >> index:{} size:{}".format(index, size)
        else:
            codError, codHTTP = 2, 400
            msgError = "Parametros incorrectos de paginado >> index:{} size:{}".format(index, size)
    except Exception as error:
        msgError = error.description
        codError, codHTTP = 2, error.code

    if re.search("connection|conexión", msgError) is not None:
        codHTTP = 500
    print("Ocurrio un problema en el Servicio de Consulta de access point  >>> {} [Cod HTTP {}]".format(msgError, codHTTP))
    co.log.error("Ocurrio un problema en el Servicio de Consulta de access point  >>> {} [Cod HTTP {}]".format(msgError, codHTTP))
    response = make_response(jsonify(errorCode=codError, errorMessage=msgError), codHTTP)
    abort(response)
