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
        uic.loadUi("gui/pagoLibreta.ui",self)
        self.statusBar().showMessage("Bienvenido")
        totalVenta = os.sys.argv[1]   #recibe el valor de selMedioPago como float
        idUsuario = os.sys.argv[2]  #recibe el valor desde ventas
        idVenta = os.sys.argv[3]  #recibe el valor desde ventas
        totalVenta =  totalVenta[0:len(totalVenta)-2]
        self.lcdTotalVenta.display(totalVenta)
        self.displayTotalVenta.setValue(int(totalVenta))
        self.lblIdUsuario.setText(idUsuario)
        self.lblidVenta.setText(idVenta)
        int(totalVenta)
        self.btnAceptar.clicked.connect(self.aceptar)
        self.btnCancelar.clicked.connect(self.cancelar)
        self.btnFin.clicked.connect(self.fin)



    def aceptar(self,totalVenta):
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        cursor = conn.cursor()
        idCliente = self.txtIdCliente.value()
        cursor.execute("SELECT nombreCliente,apellidoPaterno,apellidoMaterno,deudaTotal, deudaMaxima FROM clientes WHERE idCliente = %s", idCliente)
        consultas = cursor.fetchone()
        if (consultas):
            nombreCliente = consultas[0] + " " + consultas[1] + " " + consultas[2]
            deudaTotal = consultas[3]
            deudaMaxima = consultas[4]
            cupo = int(deudaMaxima) - int(deudaTotal)
            pago = int(self.lcdTotalVenta.value())
            self.lblNombreCliente.setText(nombreCliente)
            self.lcdDeudaTotal.display(deudaTotal)
            self.lcdCupoDisponible.display(cupo)
            if (pago > cupo):
                QMessageBox.information(self, "Error", "No tiene cupo disponible. Cancele en Efectivo",QMessageBox.Ok)
            else:
                QMessageBox.information(self, "Error", "PODEMOS PROCEDER A CARGAR A LA CUENTA DEL CLIENTE",QMessageBox.Ok)
        else:
            QMessageBox.information(self, "Error", "No existe el cliente ingresado",QMessageBox.Ok)

    def cancelar(self):
        self.close()

    def fin(self):
        #OBTIENE LA FECHA DE LA BASE DE DATOS
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        sql = "SELECT DATE_FORMAT(NOW(), '%Y-%m-%d');"
        cursor = conn.cursor()
        cursor.execute(sql)
        #fecha = cursor.fetchone()
        conn.close()
        #fechaVenta = str(fecha[0])
        idVenta = str(self.lblidVenta.text())
        totalVenta = int(self.lcdTotalVenta.value())
        folioBoleta = str(self.txtNboleta.text())
        idMedioPago = str(2)  # YA SE SABE QUE EL MEDIO DE PAGO ES EN EFECTIVO POR LO TANTO EL ID QUE CORRESPONDE ES 1
        idCliente = self.txtIdCliente.text() # EN MEDIO DE PAGO EFECTIVO NO REGISTRA CLIENTE
        #idUsuario = self.lblIdUsuario.text()
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        cursor = conn.cursor()
        sql = "SELECT * FROM ventas WHERE folioBoleta = " + folioBoleta
        cursor.execute(sql)
        valida = cursor.fetchone()
        if valida:
                    QMessageBox.warning(self, "ERROR", "Le numero de boleta ya fue utilizado.",QMessageBox.Ok)
        else:
                sql = "UPDATE ventas SET idMedioPago = " + idMedioPago + ", idCliente = " + idCliente + ", folioBoleta = " + folioBoleta + " WHERE idVenta = " + idVenta
                print(sql)
                cursor.execute(sql)
                conn.commit()
                sql = "SELECT deudaTotal FROM clientes WHERE idCliente = " + idCliente 
                cursor.execute(sql)
                consulta = cursor.fetchone()
                deuda = consulta[0]
                deudaActual = int(deuda) + totalVenta
                print(deudaActual)
                sql = "UPDATE clientes set deudaTotal = " + str(deudaActual) + " WHERE idCliente = " + idCliente 
                print(sql)
                cursor.execute(sql)
            #******************************************   IMPRIMIR TICKET DE VENTA ********************************
                QMessageBox.information(self, "Gracias", "Agradecemos su preferencia. Vuelva cuando guste.",QMessageBox.Ok)
                conn.commit()
        conn.close()
        self.close()
        process1 = subprocess.run(['python','venta.py',idUsuario])

app = QApplication(sys.argv)        #inicia aplicacion
#  ===================================== Traduccion de botones de QMessageBox ============================================
qt_traductor = QTranslator()
qt_traductor.load("qtbase_" + QLocale.system().name(),QLibraryInfo.location(QLibraryInfo.TranslationsPath))
app.installTranslator(qt_traductor)
window = Window()                   #Crear objeto de clase ventana
window.show()                       #Mostrar la ventana
app.exec_()                         #Ejecutar la aplicacion
