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
from itertools import cycle

#clase heredada de QMainWindow (Constructor Ventana)
class mantClientes(QMainWindow):
    #Metodo constructor clase
    def __init__(self):
        #Iniciar el objeto
        QMainWindow.__init__(self)
        #Cargar archivo ui en objeto
        uic.loadUi("gui/mantClientes.ui",self)
        self.statusBar().showMessage("Ingrese un nuevo cliente en el sistema")
        self.btnGuardar.clicked.connect(self.Insertar)
        self.btnCancelar.clicked.connect(self.Cancelar)
        self.cboxComunas.currentIndexChanged.connect(self.obtenerComuna)
        self.listarComunas()

    def listarComunas(self):
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        cursor = conn.cursor()
        sql = "SELECT nombreComuna FROM comunas ORDER BY nombreComuna ASC"
        #print(sql)
        cursor.execute(sql)
        consultas = cursor.fetchall()
        conn.commit()
        conn.close()
        row = 0
        for consulta in consultas:
            self.cboxComunas.addItem(consulta[0])

    def obtenerComuna(self):
        itemComuna = self.cboxComunas.currentText()
        index = str(self.cboxComunas.currentIndex())
        self.LBLTEST.setText(index + ".-" + itemComuna)

    def Insertar(self):

        def digito_verificador(rut):
            reversed_digits = map(int, reversed(str(rut)))
            factors = cycle(range(2, 8))
            s = sum(d * f for d, f in zip(reversed_digits, factors))
            return (-s) % 11


        # ============ CONEXION A BD ===========
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        cursor = conn.cursor()
        itemComuna = self.cboxComunas.currentText()
        id = str(self.txtIdCliente.value())
        rut = self.txtRut.text()
        nombre = self.txtNombreCliente.text()
        apellidoPaterno = self.txtapellidoPaterno.text()
        apellidoMaterno = self.txtapellidoMaterno.text()
        direccion = str(self.txtDireccion.text())
        digitoV = self.txtDV.text()
        # ============ Consigue el valor del id Comuna para hacer la relacion en bd
        sql = "SELECT idComuna FROM comunas WHERE nombreComuna = '" + itemComuna + "'"
        print (sql)
        cursor.execute(sql)
        consultas = cursor.fetchone()
        comuna = consultas[0]
        fonoFijo = self.txtFono.value()
        celular = self.txtCelular.value()
        credito = self.txtCredito.value()
        dv = digito_verificador(rut)
        dv = str(dv)
        rut = str(rut)
        if (dv == digitoV):
            sql = "SELECT * FROM clientes WHERE idCliente = " + id
            cursor = conn.cursor()
            cursor.execute(sql)
            existe = cursor.fetchone()
            if existe:
                QMessageBox.information(self, "ERROR", "Identificador de cliente ya existe.",QMessageBox.Ok)
            else :
                rut = str(rut) + "-" +str(dv)
                # Ejecuta la sentencia para ingresar el nuevo cliente
                cursor.execute("INSERT INTO clientes(idCliente,rut,nombreCliente,apellidoPaterno,apellidoMaterno,direccion,comuna,fonoFijo,celular,deudaMaxima) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (id,rut,nombre,apellidoPaterno,apellidoMaterno,direccion,comuna,fonoFijo,celular,credito))
                conn.commit()
                conn.close()
                self.close()
                process1 = subprocess.run(['python','C:/Repositorio/Sistema POS/clientes.py'])
        else:
            QMessageBox.information(self, "ERROR", "RUT INCORRECTO, reingrese.",QMessageBox.Ok)

    def Cancelar(self):
         self.close()
         process1 = subprocess.run(['python','C:/Repositorio/Sistema POS/clientes.py'])



app = QApplication(sys.argv)        #inicia aplicacion
#  ===================================== Traduccion de botones de QMessageBox ============================================
qt_traductor = QTranslator()
qt_traductor.load("qtbase_" + QLocale.system().name(),QLibraryInfo.location(QLibraryInfo.TranslationsPath))
app.installTranslator(qt_traductor)


mantClientes = mantClientes()                   #Crear objeto de clase ventana
mantClientes.show()                       #Mostrar la ventana
app.exec_()                         #Ejecutar la aplicacion
