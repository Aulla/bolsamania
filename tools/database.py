#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2016 José A. Fernández
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import sqlite3

class database(object):
    
    fileName = None
    conn = None
    close = True
    _cursor = None
    
    def createSchema(self):
        schema_filename = "./data/bolsamania_schema.sql"
        with open(schema_filename, 'rt') as f:
            schema = f.read()
        if self.close:
            self.conecta()
        print("Creando schema ...")
        self.sqlQuery(schema)
        #self.desconecta()
    
    def setFilename(self, fichero):
        self.fileName = fichero
            
    def conecta(self):
        if not self.close:
            return
        print("Conectando a %s" % self.fileName)
        self.conn = sqlite3.connect(self.fileName)
        self._cursor = self.conn.cursor()
        self.close = False
    
    def filename(self):
        return self.fileName
    
    def desconecta(self):
        print("Desconectando de %s" % self.fileName)
        self.conn.close()
        self.close = True
    
    def sqlSelect(self,tablename,campo,where = None):
        if where is None:
            where = '1=1'
        _query = "select %s FROM %s WHERE %s" % (campo,tablename,where)
        self._cursor.execute(_query)
        return self._cursor.fetchall()
    
    def sqlQuery(self, _sqlQuery):
        #print("Ejecutando query :\n%s" % _sqlQuery)
        if not self._cursor.executescript(_sqlQuery):
            print("SQL Error : %s" % _sqlQuery)
    
        
