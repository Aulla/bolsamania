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
from PyQt5 import QtGui, Qt, QtWidgets
from PyQt5.uic.uiparser import _layout_position

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


  
class formRecord(Qt.QDialog):
    
    _layout = None
    
    def __init__(self, titulo = None):
        super(formRecord, self).__init__()
        self.setWindowTitle(titulo)
        self.setModal(True)
        self._layout = Qt.QVBoxLayout()
        self._layout.addStretch(1)
        self.setLayout(self._layout)
        
        
    
    def addFieldData(self, fieldName):
        self._layout.addWidget(fieldName)
    
    



class fieldData(QtWidgets.QWidget):
    
    _label = None
    _value = None
    _showAlias = True
    _frame = None
    _HBoxLayout = None
    _type = None
    _editable = None
    
    def __init__(self, alias = None, value = None):
        super(fieldData, self).__init__()
        self._editable = True
        self.setType(value)
        self.setAlias(alias)
        self.setValue(value)
        self.mountLayout()
          
    
    def setAlias(self, value):
        self._label.setText(value)
        self.paintLayout()
    
    def alias(self):
        return self._label
    
    def value(self):
        _retorno = None
        if isinstance(self._value , bool):
            _retorno = self._value.checkState()
        else:
            _retorno = self._value.text()
        return _retorno
    
    
    def setValue(self, value):
        if isinstance(value , bool):
            self._value.setCheckState(bool(value))
        else:
            self._value.setText(value)
        
        self.paintLayout()
    
    def showAlias(self, value):
        self._showAlias = value
        if self._showAlias:
            self._label.show()
        else:
            self._label.hide()
    
    def setType(self, value):
        #Siempre hay label
        #print("%s es %s" % (value,type(value)))
        self._label = Qt.QLabel()
        
        if isinstance(value , str):#Texto
            #print("Es str")
            self._value = Qt.QLineEdit()
        elif (isinstance(value , int) and not isinstance(value , bool)) or isinstance(value , float): #Numerico
            #print("Es numérico")
            self._value = Qt.QLineEdit()
        elif isinstance(value , bool): #Boleano
            #print("Es booleano")
            self._value = Qt.QCheckBox()
        else:
            print("FieldData.DrawType(%s) desconocido. Se usa String" % type(value))
    
    def mountLayout(self):
        self._HBoxLayout = Qt.QHBoxLayout()
        self._HBoxLayout.addStretch(1)
        self._HBoxLayout.addWidget(self._label)
        self._HBoxLayout.addWidget(self._value)
        self.setLayout(self._HBoxLayout)
    
    def paintLayout(self):
        #Redimensiona el control apra que aparezcan bien todos los campos
        _leng = 220
        self.setFixedSize(_leng,40)
    
    def editable(self):
        return self._editable
    
    def setEditable(self, editable):
        if self._editable is not editable:
            self._editable = editable
            self._value.setEnabled(self._editable)

        
        
    
      
        
    
    
        
        