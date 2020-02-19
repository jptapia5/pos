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

class mantUsuarios(QMainWindow):

         def __init__(self):
                  QMainWindow.__init__(self)
                  self.setWindowTitle("Ingreso de Nuevo Usuarios") #Título
                  uic.loadUi("gui/MantUsuarios.ui", self)
                  self.statusBar().showMessage("Complete los datos para inglesar un nuevo usuario al sistema.")
                  self.btnGuardar.clicked.connect(self.Insertar)
                  self.btnCancelar.clicked.connect(self.Cancelar)
                  conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
                  cursor = conn.cursor()
                  cursor.execute("SELECT MAX(idUsuario) FROM usuarios")
                  consulta = cursor.fetchone()
                  idUsuario = int(consulta[0]) + 1
                  self.lblIdUsuario.setText(str(idUsuario))

         def Insertar(self):

                 idUsuario = self.lblIdUsuario.text()
                 nombreUsuario= self.txtNombre.text()
                 apellidoPaterno= self.txtApellidoPaterno.text()
                 apellidoMaterno= self.txtApellidoMaterno.text()
                 fono= self.txtFono.value()
                 contrasena= self.txtContrasena.text()
                 contrasenna = self.txtContrasenna.text()
                 if (contrasenna == contrasena):
                     if (nombreUsuario and apellidoPaterno and apellidoMaterno and contrasena) :
                         conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
                         cursor = conn.cursor()
                         cursor.execute("SELECT * FROM usuarios WHERE idUsuario = %s",idUsuario)
                         consulta = cursor.fetchone()
                         if consulta:
                              QMessageBox.information(self, "Error", "El usuario ingresado ya existe",QMessageBox.Ok)
                         else:
                              cursor.execute("INSERT INTO usuarios(idUsuario, nombreUsuario, apellidoPaterno, apellidoMaterno, fono, contrasena) VALUES (%s,%s,%s,%s,%s,%s)", (idUsuario, nombreUsuario, apellidoPaterno, apellidoMaterno, fono, contrasena))
                              conn.commit()
                              conn.close()
                              self.close()
                              process1 = subprocess.run(['python','login.py'])
                     else:
                          QMessageBox.information(self, "Error", "Por favor, rellene los campos obligatorios",QMessageBox.Ok)
                 else:
                      QMessageBox.information(self, "Error", "Las Contraseñas no coinciden, reintente",QMessageBox.Ok)



         def Cancelar(self):
                  self.close()

app = QApplication(sys.argv)
#  ===================================== Traduccion de botones de QMessageBox ============================================
qt_traductor = QTranslator()
qt_traductor.load("qtbase_" + QLocale.system().name(),QLibraryInfo.location(QLibraryInfo.TranslationsPath))
app.installTranslator(qt_traductor)
mantUsuarios = mantUsuarios()
mantUsuarios.show()
app.exec_()
