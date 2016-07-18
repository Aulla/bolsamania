#!/usr/bin/env python3
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

from tools.recolector import recolector
from tools.database import database
from tools.controlesqt5 import tableviewQt5
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import uic

import os, sys

qtFolder = "./forms/"
qtMainWindow = "%smainwindow.ui" % qtFolder
qtWalletWindow = "%smasterwallet.ui" % qtFolder

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtMainWindow)
Ui_wallet = uic.loadUiType(qtWalletWindow)

version = "0.1"

class BolsaMania(QMainWindow):
    
    db = None
    fichero = "./data/bolsamania.db"
    cursor = None
    uiMW = None
    uiWallet = None
    _tableViewWallet = None
    
    def __init__(self):
        super(BolsaMania, self).__init__()
        self.uiMW = Ui_MainWindow()
        self.uiMW.setupUi(self)        
        self.uiMW.pbSalir.clicked.connect(self.close)
        self.uiMW.pbCartera.clicked.connect(self.cartera_clicked)
        self.uiMW.pbPrevision.clicked.connect(self.prevision_clicked)
        self.uiMW.pbComparativa.clicked.connect(self.comparativa_clicked)
        self.uiMW.lbVersion.setText("Versión %s" % version)
        
        self.db = database()
        self.db.setFilename(self.fichero)
        db_is_new = not os.path.exists(self.db.filename())
        if db_is_new:
            self.db.createSchema()
        
        self.db.conecta()
        self.cursor = self.db.conn.cursor()

    def __del__(self):
        self.db.desconecta()
        self.close()
        
    def cartera_clicked(self):
        print("Abriendo mi cartera ...")
        self.uiWallet = uic.loadUi(qtWalletWindow)
        self.cargaCartera()
        self.uiWallet.show()
    
    def prevision_clicked(self):
        print("Abriendo prevision ...")  
    
    def comparativa_clicked(self):
        print("Abriendo comparativa ...")
    
    def cargaCartera(self):
        self.pintatvWallet()
        self.uiWallet.pbAdd.clicked.connect(self.addCartera_clicked)
        self.uiWallet.pbDel.clicked.connect(self.delCartera_clicked)
        #self.uiWallet.pbModify.clicked.connect(self.modifyCartera_clicked)
        
    
    
    def addCartera_clicked(self):
        print ("Valor = %s" % self._tableViewWallet.valorGridSeleccionado(0))

    def delCartera_clicked(self):
        reply = QMessageBox.question(self, 'Message', "¿Desea eliminar la cartera seleccionada ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print("Borrando registro id ... %s" % self._tableViewWallet.valorGridSeleccionado(0))

    
    def pintatvWallet(self):
        print("Pintando cabecera de tvWallet")
        self._tableViewWallet = tableviewQt5(self.uiWallet.tvWallet)
        self._tableViewWallet.cargaCabecera(0,"ID", 0)
        self._tableViewWallet.cargaCabecera(1,"DESCRIPCION", 0)
        self._tableViewWallet.cargaCabecera(2,"ACCIONES", 0 )
        
        #Rellenamos grid
        self.cursor.execute("select id, description, acciones from cartera where 1 = 1")
        i = 0
        for registro in self.cursor.fetchall():
            _id, description, acciones = registro
            self._tableViewWallet.cargaGrid(i,0,_id)
            self._tableViewWallet.cargaGrid(i,1,description)
            self._tableViewWallet.cargaGrid(i,2,acciones)
            i = i + 1
        
        

            
            
        #self.uiWallet.tvWallet.refresh()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = BolsaMania()
    window.show()
    sys.exit(app.exec_())
#cursor = conn.cursor()


#for v in valores:
#    print("Cargando ... %s" % v)
#    recolector(v,datetime.datetime(2016, 1, 19), datetime.datetime(2016, 1, 30),'h')
