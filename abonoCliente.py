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
class Window(QMainWindow):
    #Metodo constructor clase
    def __init__(self):
        #Iniciar el objeto
        QMainWindow.__init__(self)
        #Cargar archivo ui en objeto
        uic.loadUi("gui/abonoCliente.ui",self)
        self.statusBar().showMessage("Ingrese un pago realizado por un cliente.")
        self.btnConsulta.clicked.connect(self.consultaCliente)
        self.btnAceptar.clicked.connect(self.aceptar)
        self.btnFin.clicked.connect(self.finalizar)
        self.btnCancelar.clicked.connect(self.cancelar)
        self.fechaActual()

        if len(os.sys.argv) > 1:
            idUsuario =  os.sys.argv[1]                 # variable recuperada de mainLogin.py
            print(idUsuario)
            self.lblidUsuario.setText(idUsuario)

    def fechaActual(self):
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        sql = "SELECT DATE_FORMAT(NOW(), '%Y-%m-%d');"
        cursor = conn.cursor()
        cursor.execute(sql)
        fecha = cursor.fetchone()
        fecha = str(fecha[0])
        #print(fecha)
        self.lblFechaActual.setText(fecha)
        conn.close()
        self.btnFin.setEnabled(False)

    def consultaCliente(self):
        idCliente = self.txtCliente.text()
        if(idCliente):
            conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
            cursor = conn.cursor()
            cursor.execute("SELECT deudaTotal, nombreCliente, apellidoPaterno, apellidoMaterno FROM clientes WHERE idCliente = %s", idCliente)
            consulta = cursor.fetchone()
            if consulta:
                deuda = consulta[0]
                nombre = consulta[1] + " " + consulta[2] + " " + consulta[3]
                if (deuda == 0):
                    self.lblNombreCliente.setText(nombre)
                    QMessageBox.information(self, 'Información', "Cliente no tiene deuda",QMessageBox.Ok)
                else:
                    self.lcdSaldoAdeudado.setValue(deuda)
                    self.lblNombreCliente.setText(nombre)
                    self.txtTotalAbono.setEnabled(True)
                    self.txtPaga.setEnabled(True)
                    self.txtCliente.setEnabled(True)
                    self.btnAceptar.setEnabled(True)
                    self.btnConsulta.setEnabled(True)
                    self.btnFin.setEnabled(False)
            else:
                QMessageBox.information(self, 'Error', "Cliente no existe",QMessageBox.Ok)
            conn.close()
        else:
            QMessageBox.information(self, 'Error', "Debe ingresar numero de cliente",QMessageBox.Ok)

    def aceptar(self):
        totalAbono = self.txtTotalAbono.value()
        deudaTotal = self.lcdSaldoAdeudado.value()
        efectivo = self.txtPaga.value()
        if(totalAbono and efectivo and efectivo>=totalAbono and totalAbono<=deudaTotal):
            vuelto = efectivo - totalAbono
            self.lcdVuelto.setValue(vuelto)
            self.btnFin.setEnabled(True)
        else:
            QMessageBox.information(self, 'Error', "Error en los montos ingresados. Por Favor verifique",QMessageBox.Ok)

    def finalizar(self):

        respuesta = QMessageBox.warning(self, 'Advertencia', "¿Está usted seguro de abonar dinero a su cuenta?",QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if respuesta == QMessageBox.Yes:
            deudaTotal = self.lcdSaldoAdeudado.value()
            idCliente = self.txtCliente.text()
            montoPagado = self.txtTotalAbono.value()
            deudaActualizada = deudaTotal - montoPagado
            idUsuario = self.lblidUsuario.text()
            conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
            sql = "SELECT DATE_FORMAT(NOW(), '%Y-%m-%d');"
            cursor = conn.cursor()
            cursor.execute(sql)
            consulta = cursor.fetchone()
            fechaPago = str(consulta[0])
            print(idCliente)
            print(fechaPago)
            print(montoPagado)
            print(idUsuario)
            cursor.execute("SELECT * FROM abono_cliente WHERE idCliente = %s AND fechaPago = %s",(idCliente, fechaPago))
            consulta = cursor.fetchone()
            cursor.close()
            if (consulta):
                QMessageBox.information(self, 'Información', "Ya ha realizado un abono, solo puede realizar una pago diario.",QMessageBox.Ok)
            else:
                conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
                cursor = conn.cursor()
                #cursor.execute("INSERT INTO abono_cliente (idCliente,fechaPago,monto,IdUsuario) VALUES (%s,%s,%s,%s)", (idCliente,fechaPago,montoPagado,idUsuario))
                sql = ("INSERT INTO abono_cliente (idCliente,fechaPago,monto,IdUsuario) VALUES('" + idCliente + "','" + fechaPago + "','" + montoPagado + "','" + idUsuario + "');")
                cursor.execute(sql)
                conn.commit()
                cursor.execute("UPDATE clientes SET deudaTotal = %s WHERE idCliente = %s",(deudaActualizada,idCliente))
                conn.commit()
            conn.close()
            self.close()


    def cancelar(self):
        self.close()

app = QApplication(sys.argv)        #inicia aplicacion
#  ===================================== Traduccion de botones de QMessageBox ============================================
qt_traductor = QTranslator()
qt_traductor.load("qtbase_" + QLocale.system().name(),QLibraryInfo.location(QLibraryInfo.TranslationsPath))
app.installTranslator(qt_traductor)
window = Window()                   #Crear objeto de clase ventana
window.show()                       #Mostrar la ventana
app.exec_()                         #Ejecutar la aplicacion
