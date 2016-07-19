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
from tools.database import database
from libs.wallet import wallet
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic

import os, sys

qtFolder = "./forms/"
qtMainWindow = "%smainwindow.ui" % qtFolder
qtMasterWalletWindow = "%smasterwallet.ui" % qtFolder

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtMainWindow)

version = "0.2"

class BolsaMania(QMainWindow):
    
    db = None
    fichero = "./data/bolsamania.db"
    _cursor = None
    uiMW = None
    _wallet = None
    uiMasterWallet = None
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

    def __del__(self):
        self.db.desconecta()
        self.close()
        
    def cartera_clicked(self):     
        self.wallet = wallet(qtMasterWalletWindow, self.db)
    
    def prevision_clicked(self):
        print("Abriendo prevision ...")  
    
    def comparativa_clicked(self):
        print("Abriendo comparativa ...")
    
    
        
        

            
 
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
