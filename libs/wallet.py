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

from tools.controlesqt5 import tableviewQt5, fieldData, formRecord
from tools.recolector import recolector
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox
from datetime import datetime, timedelta
import csv
    
class wallet(object):
    uiMasterWallet = None
    uiWallet = None
    db = None
    _oldDescription = None
    _recolector = None
    _valueActual = None
    _valueMin = None
    _valueMax = None
    _valueDate = None
    _valueOpen = None
    _valueClose = None
    _valueAdjust = None
    _valueVolume = None
    
    
    def __init__(self,masterW, db):
        self.db = db
        self.uiMasterWallet = uic.loadUi(masterW)
        self.uiMasterWallet.setModal(True)
        self.cargaCartera()
        self.uiMasterWallet.show()
        self._tableViewWallet._tableView.clicked.connect(self.tableView_Clicked)
        self.tableView_Clicked()
    
    def tableView_Clicked(self):
        print("TableView clicked !!")
        #Hay que recoger cuanto es el intervalo y luego lanzar un proceso cada tiempo ...
        resultIdCartera = self.db.sqlSelect("cartera","precioc, acciones, idvalor", "id = %s" % self._tableViewWallet.valorGridSeleccionado(0))
        #print("result ... %s" % resultIdCartera)
        idValor = None
        for result in resultIdCartera:
            self._precioc, self._acciones, idValor = result
        
        if idValor is None:
            return
        #print("idValor es %s" % idValor)
        
        resultValorName = self.db.sqlSelect("valores","name", "id = %s" % idValor)
        valorName = None
        for result2 in resultValorName:
            valorName = result2[0]
        
        #print("El valor a buscar es ... %s" % valorName) 
        
        _recolector = recolector(valorName)
        _desde = datetime.now()
        cerrado = False
        if _desde.strftime("%w") is '0':
            _desde = _desde + timedelta(days=-2)
            cerrado = True
        
        if _desde.strftime("%w") is '6':
            _desde = _desde + timedelta(days=-1)
            cerrado = True
        _hasta = _desde
        
        _periodo = "d"
        ficheroTemp = _recolector.ask(_desde, _hasta, _periodo)
        cabecera = False
        #print("Leyendo fichero %s" % ficheroTemp)
        with open(ficheroTemp, 'r') as csvfile:
            spamreader = csv.reader(csvfile,quotechar='|')
            for row in spamreader:
                if cabecera is False:
                    cabecera = True
                    #print("Cabecera %s" % row)
                else:
                    #print("Linea %s" % row)
                    self._valueDate, self._valueOpen, self._valueMax, self._valueMin, self._valueClose, self._valueVolume, self._valueAdjust = row
                    self.updateLabels()
    
    def updateLabels(self):
        
        _coste = self._acciones * float(self._precioc)
        _valorActual = self._acciones * float(self._valueClose)
        _variacionN = self._acciones * (float(self._valueOpen) - float(self._valueClose))
        _variacionP = (_variacionN * 100) / _valorActual
        _rentabilidadN = _valorActual - _coste
        _rentabilidadP = (_rentabilidadN * 100 / _valorActual) 
        
        self.uiMasterWallet.lblCosteValue.setText(str(_coste))
        self.uiMasterWallet.lblValorValue.setText(str(_valorActual))
        self.uiMasterWallet.lblVariacionHoyValue.setText("%s (%s%%)" % (round(_variacionN, 3),round(_variacionP, 2)))
        self.uiMasterWallet.lblRentabilidadValue.setText("%s (%s%%)" % (round(_rentabilidadN, 3), round(_rentabilidadP, 2)))
        
        
        
        
    
    
    def cargaCartera(self):
        self.pintatvWallet()
        self.uiMasterWallet.pbAdd.clicked.connect(self.addCartera_clicked)
        self.uiMasterWallet.pbDel.clicked.connect(self.delCartera_clicked)
        self.uiMasterWallet.pbMod.clicked.connect(self.modifyCartera_clicked)

        
    
    def formCartera(self, titulo= None):
        self.uiWallet = None
        self.uiWallet = formRecord(titulo)

        _resultado = self.db.sqlSelect("valores","name, description")
        _dValores = {}
        for registro in _resultado:
            _name, _description = registro
            _dValores[_name] = _description

        cdescripcion = fieldData("Descripción")
        cacciones = fieldData("Acciones")            
        cvalores = fieldData("Valores", _dValores)
        pcompra = fieldData("P.Compra")
        

        self.uiWallet.addFieldData(cdescripcion)
        self.uiWallet.addFieldData(cacciones)
        self.uiWallet.addFieldData(cvalores)
        self.uiWallet.addFieldData(pcompra)
        
        
        
        
        
        
        
    def addCartera_clicked(self):
        self.formCartera("Nueva Cartera")
        self.uiWallet.callAceptar(self.saveCartera)
        
    
    def saveCartera(self):
        for registro in self.db.sqlSelect("valores","id","description ='%s'" % self.uiWallet.fieldDataValue("Valores")):
            _idValor = registro
        #print("idValor vale %s" % _idValor[0])    
        sqlQuery = "INSERT INTO cartera (description, acciones, idvalor, precioc) values ('%s','%s','%s','%s')" % (self.uiWallet.fieldDataValue("Descripción"), self.uiWallet.fieldDataValue("Acciones"),
                                                                                            _idValor[0], self.uiWallet.fieldDataValue("P.Compra"))
        #print("Consulta ... %s" % sqlQuery)
        self.db.sqlQuery(sqlQuery)
        self.pintatvWallet()

    def updateCartera(self):
        _valorDescription = self.uiWallet.fieldDataValue("Valores")
        #print("Recogiendo ... %s" % _valorDescription)
        _resultSql = self.db.sqlSelect("valores","id","description = '%s'" % _valorDescription)[0]
        for _value in _resultSql:
            sqlQuery = "UPDATE cartera SET description ='%s', acciones=%s, idvalor=%s, precioc=%s WHERE description = '%s'" % (self.uiWallet.fieldDataValue("Descripción"), self.uiWallet.fieldDataValue("Acciones"),
                                                                                            _value, self.uiWallet.fieldDataValue("P.Compra"), self._oldDescription)
        print(sqlQuery)
        self.db.sqlQuery(sqlQuery)
        self.pintatvWallet()

    def modifyCartera_clicked(self):
        if self._tableViewWallet.valorGridSeleccionado(0) is -1:
            return
        self.formCartera("Modificar cartera Cartera")
        _resultado = self.db.sqlSelect("cartera","id, description, acciones, precioc, idvalor", "id = %s" %self._tableViewWallet.valorGridSeleccionado(0))
        _dValores = {}
        for registro in _resultado:
            _id, _description, _acciones, _precioc, _idValor = registro
            _descriptionValor = self.db.sqlSelect("valores","description","id = %s" % _idValor)[0]
            for _descrip in _descriptionValor:
                #print("Description = %s" % _descrip)
                _dValores[_idValor] = _descrip            
            
            self.uiWallet.setfieldDataValue("Descripción", _description)
            self.uiWallet.setfieldDataValue("Acciones", _acciones)
            self.uiWallet.setfieldDataValue("Valores", _dValores)
            self.uiWallet.setfieldDataValue("P.Compra", _precioc)
        self._oldDescription = _description   
        self.uiWallet.callAceptar(self.updateCartera)    
        
        
    def delCartera_clicked(self):
        if self._tableViewWallet.valorGridSeleccionado(0) is -1:
            return
        reply = QMessageBox.question(self.uiMasterWallet, 'Message', "¿Desea eliminar la cartera seleccionada ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            _sqlQuery = "DELETE FROM cartera WHERE id=%s" %  self._tableViewWallet.valorGridSeleccionado(0)
            self.db.sqlQuery(_sqlQuery) 
            self.pintatvWallet()

    
    def pintatvWallet(self):
        #print("Pintando cabecera de tvWallet")
        self._tableViewWallet = None
        self._tableViewWallet = tableviewQt5(self.uiMasterWallet.tvWallet)
        self._tableViewWallet.cargaCabecera(0,"ID", 0)
        self._tableViewWallet.cargaCabecera(1,"DESCRIPCION", 0)
        self._tableViewWallet.cargaCabecera(2,"ACCIONES", 0 )
        self._tableViewWallet.cargaCabecera(3,"VALOR", 0 )
        
        #Rellenamos grid
        _resultado = self.db.sqlSelect('cartera','id, description, acciones, idvalor')
        i = 0
        for registro in _resultado:
            _id, _description, _acciones, _idValor = registro
            self._tableViewWallet.cargaGrid(i,0,_id)
            self._tableViewWallet.cargaGrid(i,1,_description)
            self._tableViewWallet.cargaGrid(i,2,_acciones)
            _resultValores = self.db.sqlSelect('valores','description','id = %s' % _idValor)
            for _valor in _resultValores:
                _valorDescription = _valor
            
            self._tableViewWallet.cargaGrid(i,3,_valorDescription[0])
            i = i + 1