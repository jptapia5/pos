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
class mantComunas(QMainWindow):
    #Metodo constructor clase
    def __init__(self):
        #Iniciar el objeto
        QMainWindow.__init__(self)
        #Cargar archivo ui en objeto
        uic.loadUi("gui\mantComunas.ui",self)
        self.statusBar().showMessage("Le permite ingresar otra comuna al sistema")
        self.btnGuardar.clicked.connect(self.Insertar)
        self.btnCancelar.clicked.connect(self.Cancelar)
    '''    self.carga(conn)

    def carga(self):
        cursor = conn.cursor()
        sql = ("SELECT count(idCategoriaProducto) FROM categoria_producto")
        registros = cursor.execute(sql)
        print(registros)
        conn.commit()
        conn.close()'''

    def Insertar(self):
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        cursor = conn.cursor()
        idComuna = self.txtIdComuna.text()
        print(idComuna)
        nombreComuna = self.txtNombreComuna.text() #COMO OBTENER EL TEXTO
        print(nombreComuna)
        cursor.execute ("INSERT INTO comunas(idComuna, nombreComuna) VALUES (%s,%s)", (idComuna,nombreComuna))
        #FALTA VALIDAR QUE SE GUARDÓ CORRECTAMENTE EN LA BASE DE DATOS
        conn.commit()
        conn.close()
        self.close()
        process1 = subprocess.run(['python','C:\Repositorio\Sistema POS\comunas.py'])



    def Cancelar(self):
        print("Salir de programa")
        process1 = subprocess.run(['python','C:\Repositorio\Sistema POS\comunas.py'])
        self.close()



app = QApplication(sys.argv)        #inicia aplicacion
#  ===================================== Traduccion de botones de QMessageBox ============================================
qt_traductor = QTranslator()
qt_traductor.load("qtbase_" + QLocale.system().name(),QLibraryInfo.location(QLibraryInfo.TranslationsPath))
app.installTranslator(qt_traductor)


mantComunas = mantComunas()                   #Crear objeto de clase ventana
mantComunas.show()                       #Mostrar la ventana
app.exec_()                         #Ejecutar la aplicacion
