import sys
import os
import subprocess
import pymysql
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import time
from datetime import *
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog

#clase heredada de QMainWindow (Constructor Ventana)
class mainLogin(QMainWindow):
    #Metodo constructor clase
    def __init__(self):
        #Iniciar el objeto
        QMainWindow.__init__(self)
        #Cargar archivo ui en objeto
        uic.loadUi("gui/mainLogin.ui",self)
        #self.statusBar().showMessage("Bienvenido")
      # =================== EVENTOS QPUSHBUTTON ==================
        self.btnAceptar.clicked.connect(self.login)
        self.btnSalir.clicked.connect(self.salir)
        self.fecha()

    def fecha (self):
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        sql = "SELECT DATE_FORMAT(NOW(), '%d-%m-%Y');"
        cursor = conn.cursor()
        cursor.execute(sql)
        fecha = cursor.fetchone()
        #print(fecha)
        fecha = str(fecha[0])
        #print(fecha)
        #print(fecha)
        self.lblFecha.setText(fecha)

    def login(self,fecha):
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        cursor = conn.cursor()
        idUsuario = self.txtUsuario.text()
        contrasena = self.txtPassword.text()
        montoInicial = self.txtMonto.value()
        #corrobora si se inició ya sesión
        sql = "SELECT DATE_FORMAT(NOW(),'%Y-%m-%d');"
        cursor = conn.cursor()
        cursor.execute(sql)
        fecha = cursor.fetchone()
        fecha = str(fecha[0])
        montoFinal = 0
        #print(fecha)
# ********************************** VALIDA SI INGRESÓ LOS DATOS REQUERIDOS **********************************
        #if (idUsuario and contrasena and montoInicial):
        if (idUsuario and contrasena):
                            conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
                            cursor = conn.cursor()
                            cursor.execute("SELECT contrasena FROM usuarios WHERE idUsuario = %s", idUsuario)
                            consulta = cursor.fetchone()
# ********************************** VALIDA SI EL USUARIO EXISTE **********************************
                            if consulta:
                                        validaContrasena = consulta[0]
# ********************************** VALIDA QUE LA CONTRASENA CORRESPONDA AL USUARIO **********************************
                                        if contrasena == validaContrasena:
# ********************************** CONSULTARÁ SI YA INICIÓ SESION EN EL DÍA. SI LO HIZO TOMA LOS DATOS Y LOS REUTILIZA  **********************************
                                                                        sql = "SELECT * FROM caja WHERE idUsuario = " + idUsuario + " AND fecha =' " + fecha + "'"
                                                                        cursor.execute(sql)
                                                                        query = cursor.fetchone()
                                                                        if (query):
# ********************************** ENCONTRÓ YA UN INICIO DE SESION, DEBE TOMAR DATOS GUARDADOS **********************************
                                                                                    print("INICIO DE SESIÓN OK!")
                                                                                    conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
                                                                                    cursor = conn.cursor()
                                                                                    cursor.execute("SELECT nombreUsuario,apellidoPaterno FROM usuarios WHERE idUsuario = %s", idUsuario)
                                                                                    consultas = cursor.fetchone()
                                                                                    idUsuario = consultas[0] + " " +  consultas[1]
                                                                                    conn.close()
                                                                                    if (idUsuario):
                                                                                        QMessageBox.information(self, "Inicio sesion OK", "Bienvenido %s" % idUsuario, QMessageBox.Ok)
                                                                                        idUsuario = self.txtUsuario.text()  #esta variable la pasa al programa ventas.py
                                                                                        self.close()
                                                                                        process1 = subprocess.run(['python','venta.py',idUsuario])
    # **********************************SI NO HA INICIADO SESIÓN DURANTE EL DÍA GUARDARÁ LOS DATOS DE INICIO **********************************
                                                                        else:
                                                                                conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
                                                                                cursor = conn.cursor()
                                                                                sql =("INSERT INTO caja(idUsuario, fecha, montoInicial,montoFinal) VALUES (" + str(idUsuario) + ",'" + str(fecha) + "'," + str(montoInicial) + ","+ str(montoFinal) + ")")
                                                                                cursor.execute(sql)
                                                                                conn.commit()
                                                                                cursor = conn.cursor()
                                                                                cursor.execute("SELECT nombreUsuario,apellidoPaterno FROM usuarios WHERE idUsuario = %s", idUsuario)
                                                                                consultas = cursor.fetchone()
                                                                                idUsuario = consultas[0] + " " +  consultas[1]
                                                                                conn.close()
                                                                                if (idUsuario):
                                                                                                QMessageBox.information(self, "Inicio sesion OK", "Bienvenido %s" % idUsuario, QMessageBox.Ok)
                                                                                                idUsuario = self.txtUsuario.text() # **** ESTA VARIABLE LA PASA A VENTA.PY *******
                                                                                                self.close()
                                                                                                process1 = subprocess.run(['python','venta.py',idUsuario])
                                        else:
                                             QMessageBox.critical(self, "Error de inicio sesion", "Usuario o Contraseña incorrecta",QMessageBox.Ok)
                            else:
                                 QMessageBox.critical(self, "Error de inicio sesion", "Usuario o Contraseña incorrecta",QMessageBox.Ok)
        else:
             QMessageBox.critical(self, "Error de inicio sesion", "Usuario, Contreaseña o monto incorrecto",QMessageBox.Ok)


    def salir(self):
        self.close()

app = QApplication(sys.argv)        #inicia aplicacion
mainLogin = mainLogin()                   #Crear objeto de clase ventana
mainLogin.show()                       #Mostrar la ventana
app.exec_()                         #Ejecutar la aplicacion
