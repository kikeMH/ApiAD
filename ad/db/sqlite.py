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
import time
import pandas as pd
import sqlite3
import os
import ad.utils.contants as co

class ConexionDB:
    '''
    Clase de Base de Datos, almacena metodos de conexion y consulta
    '''
    def __init__(self, dsn):
        self.dsn = dsn
        self.connection = None
        self.cursor = None

    def creaconexion(self):
        """Funcion de conexion a Base de Datos inicial, se ejecuta al invocarse desde la instancia
           inlcuye reintentos de conexion
        """
        self.connection = None
        if os.path.isfile(self.dsn):
            os.remove(self.dsn)
            co.log.warning("Archivo obsoleto de BD removido")
        try:
            reintento = 1
            while reintento <= 3:
                try:
                    self.connection = sqlite3.connect(self.dsn, check_same_thread=False)
                    self.cursor = self.connection.cursor()
                    self.cursor.execute('''CREATE TABLE "AD_APWIFI_CDMX" (
                                        "id"	TEXT NOT NULL,
                                        "programa"	TEXT NOT NULL,
                                        "fecha_instalacion"	NUMERIC,
                                        "latitud"	INTEGER NOT NULL,
                                        "longitud"	INTEGER NOT NULL,
                                        "colonia"	TEXT NOT NULL,
                                        "alcaldia"	TEXT NOT NULL,
                                        PRIMARY KEY("id"))''')
                    co.log.info(" -Coneccion a BD-SQLite establecida correctamente")
                except Exception as errordb:
                    co.log.error("Error de conexion %s", errordb)
                    co.log.error(errordb, exc_info=True)
                if self.connection is None:
                    print("Reintento de conexion a Base de Datos... {}".format(reintento))
                    co.log.info("Reintento de conexion a Base de Datos... {}".format(reintento))
                    time.sleep(5)
                else:
                    break
                reintento += 1
        except Exception as error:
            print(error)
            co.log.error(error, exc_info=True)

    def select(self, stmt):
        '''
        Funcion para consulta de datos
        :param stmt:
        :return: [flag, datos]
        '''
        datos, flag = [], False
        try:
            self.cursor.execute(stmt)
            datos = self.cursor.fetchall()
            flag = True
        except Exception as error:
            co.log.error(error, exc_info=True)
        return [flag, datos]

    def etlccv(self):
        # Carga de datos desde fuente origen
        df = pd.read_csv('./in/2024-01-18-puntos_de_acceso_wifi.csv', skiprows=1, header=None)
        co.log.info("Datos leidos correctamente")

        # Persistencia de datos a BD
        sql = "insert into AD_APWIFI_CDMX(id, programa, fecha_instalacion, latitud, longitud, colonia, alcaldia) " \
              "values('{}', '{}', {}, {}, {}, '{}', '{}')"
        rows = []
        fo = open("./log/stmterr.sql", 'w')
        for index, row in df.iterrows():
            stmt = sql.format(row[0], row[1], 'null', row[3], row[4], row[5], row[6])
            try:
                self.cursor.execute(stmt)
                co.c_rx += 1
                co.hascoor[row[0]] = {'id': row[0], 'programa': row[1], 'fecha_instalacion': None, 'latitud': row[3], 'longitud': float(row[4]), 'colonia': row[5], 'alcaldia': row[6]}
            except Exception as error:
                co.c_err += 1
                co.log.error(error, exc_info=True)
                fo.write("{}\n".format(stmt))
            rows.append(stmt)
            print(time.strftime("%H:%M:%S"), "RX={:0>8} TX={:0>8} ERR={:0>8}\t\t\r".format(co.c_rx, co.c_tx, co.c_err), end="", flush=True)
        self.connection.commit()
        # condb.connection.close()
        print("\n** REGISTROS RECIBIDOS ==> [{}]".format(len(rows)))
        print("** REGISTROS PERSISTIDOS A BD ==> [{}]".format(co.c_rx))
        print("** REGISTROS CONERROR ==> [{}]".format(co.c_err))
        fo.close()
