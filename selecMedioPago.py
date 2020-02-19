import sys
import os
import subprocess
import pymysql
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import time
import datetime
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog


#clase heredada de QMainWindow (Constructor Ventana)
class selMedioPago(QDialog):
    #Metodo constructor clase
    def __init__(self):
        #Iniciar el objeto
        QDialog.__init__(self)
        #Cargar archivo ui en objeto
        uic.loadUi("gui/selecMedioPago.ui",self)
        self.btnEfectivo.clicked.connect(self.efectivo)
        self.btnLibreta.clicked.connect(self.libreta)
        totalVenta = os.sys.argv[1]  #recibe el valor desde ventas
        idUsuario = os.sys.argv[2]  #recibe el valor desde ventas
        idVenta = os.sys.argv[3]  #recibe el valor desde ventas
        #print(totalVenta)
        print(idUsuario)
        print("************** LO QUE RECIBE ***********")
        self.lblIdUsuario.setText(idUsuario)
        self.lcdTotalPagar.display(totalVenta)
        self.lblidVenta.setText(idVenta)


    def efectivo(self,totalVenta):
        totalVenta = str(self.lcdTotalPagar.value())  # toma el valor desde el lcd para enviarlo a pago efectivo
        idUsuario = self.lblIdUsuario.text()
        idVenta= self.lblidVenta.text()
        self.close()
        process1 = subprocess.run(['python','pagoEfectivo.py',totalVenta,idUsuario,idVenta])

    def libreta(self):
            totalVenta = str(self.lcdTotalPagar.value())  # toma el valor desde el lcd para enviarlo a pago efectivo
            totalVenta = str(self.lcdTotalPagar.value())  # toma el valor desde el lcd para enviarlo a pago efectivo
            idUsuario = self.lblIdUsuario.text()
            idVenta= self.lblidVenta.text()
            self.close()
            process1 = subprocess.run(['python','pagoLibreta.py',totalVenta,idUsuario,idVenta])

app = QApplication(sys.argv)        #inicia aplicacion
qt_traductor = QTranslator()
qt_traductor.load("qtbase_" + QLocale.system().name(),QLibraryInfo.location(QLibraryInfo.TranslationsPath))
app.installTranslator(qt_traductor)
selMedioPago = selMedioPago()                   #Crear objeto de clase ventana
selMedioPago.show()                       #Mostrar la ventana
app.exec_()                         #Ejecutar la aplicacion
