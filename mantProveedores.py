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
class mantProveedores(QMainWindow):
    #Metodo constructor clase
    def __init__(self):
        #Iniciar el objeto
        QMainWindow.__init__(self)
        #Cargar archivo ui en objeto
        uic.loadUi("gui/mantProveedores.ui",self)
        self.btnCancelar.clicked.connect(self.cancelar)
        self.btnGuardar.clicked.connect(self.agregar)
        self.listarCombobox()

    def listarCombobox(self):
           conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
           cursor = conn.cursor()
           #LISTA LAS CATEGORIA DE PRODUCTOS EN COMBOBOXx
           cursor.execute ("SELECT nombreComuna FROM comunas")
           consultas = cursor.fetchall()
           for consulta in consultas:
                comunas = consulta[0]
                self.cbxComunas.addItem(comunas)
           #LISTA LOS PROVEEDORES EN COMBOBOX
           conn.close()


    def agregar(self):
         print("debe agregar un nuevo proveedor")
         idProveedor = int(self.txtIdProveedor.text())
         rutProveedor = self.txtRut.text()
         nombreProveedor = self.txtProveedor.text()
         direccion = self.txtDireccion.text()
         contacto = self.txtContacto.text()
         fono = self.txtFono.text()
         email = self.txtMail.text()
         #debo seleccionar la comuna
         idComuna = 1
         conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
         cursor = conn.cursor()
         cursor.execute("SELECT * FROM proveedores WHERE idProveedor = %s", idProveedor)
         valida = cursor.fetchone()
         if valida:
                QMessageBox.warning(self, 'Error', "El codigo de proveedor ingresado ya existe.",	QMessageBox.Ok)
         else:
                 cursor.execute ("INSERT INTO proveedores( idProveedor, rutProveedor, nombreProveedor, contacto, fono, email, idComuna, direccion) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (idProveedor, rutProveedor, nombreProveedor, contacto, fono, email, idComuna, direccion))
                 conn.commit()
         conn.close()
         self.close()
         process1 = subprocess.run(['python','proveedores.py'])

    def cancelar(self):
         self.close()

app = QApplication(sys.argv)        #inicia aplicacion
#  ===================================== Traduccion de botones de QMessageBox ============================================
qt_traductor = QTranslator()
qt_traductor.load("qtbase_" + QLocale.system().name(),QLibraryInfo.location(QLibraryInfo.TranslationsPath))
app.installTranslator(qt_traductor)
mantProveedores = mantProveedores()                   #Crear objeto de clase ventana
mantProveedores.show()                       #Mostrar la ventana
app.exec_()                         #Ejecutar la aplicacion
