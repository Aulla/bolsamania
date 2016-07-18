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
##############################################################################
from PyQt5 import QtGui, Qt

class tableviewQt5(object):
    
    _tableView = None
    _model = None
    
    def __init__(self, objeto):
        self._tableView = objeto
        self._tableView.setAlternatingRowColors(True)
        self._model = QtGui.QStandardItemModel(self._tableView)
        self._tableView.setModel(self._model)
    
    def cargaCabecera(self,position, value, align = None):
        if align is not None:
            print("FIXME: tableviewQt5.cargaCabecera.align %s" % align)
        self._model.setHorizontalHeaderItem(position, Qt.QStandardItem(str(value)))
    
    #Carga un valor especifico en una casilla especifica
    def cargaGrid(self, fila, columna, value , tipo = None):
        _value = None
        if tipo is 0 or tipo is None:
            _value = Qt.QStandardItem(str(value))
        elif tipo is 1:
            _value = Qt.QStandardItem(int(value))
        elif tipo is 2:
            _value = Qt.QStandardItem(float(value))
        else:
            print("FIXME: tableviewQt5.cargaGrid.tipo %s desconocido" % tipo)
            _value = Qt.QStandardItem(str(value))
                
        self._model.setItem(fila, columna, _value)
    
    #Retorna el valor del campo especificado en la linea seleccionada
    def valorGridSeleccionado(self, campo):
        curentIndex = self._tableView.currentIndex()
        #print("Current index row es %s" % curentIndex.row())
        if curentIndex.row() >= 0:
            return self._model.item(curentIndex.row(), campo).text()
        else:
            return -1
        

        
        
    
    
    def mostrar(self):
        self._tableView.show()
    
    def __del__(self):
        self.tableView = None
    
    
                
    
    

