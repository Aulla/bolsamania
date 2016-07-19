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
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox
    
class wallet(object):
    uiMasterWallet = None
    uiWallet = None
    db = None
    _oldDescription = None
    
    def __init__(self,masterW, db):
        self.db = db
        self.uiMasterWallet = uic.loadUi(masterW)
        self.uiMasterWallet.setModal(True)
        self.cargaCartera()
        self.uiMasterWallet.show()  
    
    
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