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
class cierreCaja(QMainWindow):
    #Metodo constructor clase
    def __init__(self):
        #Iniciar el objeto
        QMainWindow.__init__(self)
        #Cargar archivo ui en objeto
        uic.loadUi("gui/cierreCaja.ui",self)
        self.statusBar().showMessage("Cerrar Caja Fin de Jornada")
        self.btnCancelar.clicked.connect(self.cancelar)
        self.btnAceptar.clicked.connect(self.aceptar)
        self.btnFin.clicked.connect(self.fin)
        #idUsuario = os.sys.argv[1]
        idUsuario = "1000"
        self.lblIdUsuario.setText(idUsuario)
        self.fechaCajero()
        self.montoApertura()
        self.montoRecaudado()

    def fechaCajero(self):
        idUsuario = self.lblIdUsuario.text()
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        sql = "SELECT DATE_FORMAT(NOW(), '%d-%m-%Y');"
        cursor = conn.cursor()
        cursor.execute(sql)
        fecha = cursor.fetchone()
        fecha = str(fecha[0])
        conn.close()
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        cursor = conn.cursor()
        sql = "SELECT nombreUsuario,apellidoPaterno FROM usuarios WHERE idUsuario = " + idUsuario
        cursor.execute(sql)
        consulta = cursor.fetchone()
        usuario = str(consulta[0]) + " " + str(consulta[1])
        #print(fecha)
        conn.close()
        self.lblUsuario.setText(usuario)
        self.lblFecha.setText(fecha)

    def montoApertura(self):
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        sql = "SELECT DATE_FORMAT(NOW(), '%Y-%m-%d');"
        cursor = conn.cursor()
        cursor.execute(sql)
        fecha = cursor.fetchone()
        fecha = str(fecha[0]) # ******
        conn.close()
        idUsuario = self.lblIdUsuario.text()
        #CONSULTA POR EL MONTO INICIAL DE CAJA DEL usuario EL DIA DE HOY
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        cursor = conn.cursor()
        sql = "SELECT montoInicial FROM caja WHERE idUsuario = " + idUsuario + " AND fecha = '" + fecha +"'"
        #print(sql)
        cursor.execute(sql)
        consulta = cursor.fetchone()
        #print(consulta)
        montoInicial = consulta[0]
        conn.close()
        self.lcdMontoApertura.setValue(int(montoInicial))

    def montoRecaudado(self):
        print(" ********************** CONSULTA POR MONTO RECAUDADO AL MOMENTO ****************************************")
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        sql = "SELECT DATE_FORMAT(NOW(), '%Y-%m-%d');"
        cursor = conn.cursor()
        cursor.execute(sql)
        fecha = cursor.fetchone()
        fecha = str(fecha[0]) # ******
        #YA OBTUVE LA HORA
        idUsuario = self.lblIdUsuario.text()
        cursor = conn.cursor()
# *******************************  CONSULTA EL DINERO QUE HA ENTRADO A CAJA POR VENTAS *******************************************************
        sql = "SELECT SUM(montoVenta) FROM ventas WHERE idUsuario = " + idUsuario + " AND fechaVenta = '" + fecha +"' AND idMedioPago = 1;"
        cursor.execute(sql)
        consulta = cursor.fetchone()
        print("CONSULTA MONTO VENTA :" + str(consulta[0]))
        if consulta[0]:
                    montoVenta = consulta[0]
        else:
                    montoVenta = int(0)
                    print("NO HAY VENTAS")
# *******************************  CONSULTA EL DINERO QUE HA ENTRADO A CAJA POR ABONOS DE CLIENTES *******************************************************
        sql = "SELECT SUM(monto) FROM abono_cliente WHERE idUsuario = " + idUsuario + " AND fechaPago = '" + fecha + "'"
        print(sql)
        cursor.execute(sql)
        consulta = cursor.fetchone()
        if consulta[0]:
                    montoAbonos = consulta[0]
        else:
                    montoAbonos = int(0)
                    print("NO HAY ABONOS")
        print(montoAbonos)
        print(montoVenta)
        montoRecaudado = montoAbonos +  montoVenta
        self.lcdRecaudado.setValue(int(montoRecaudado))
        conn.close()

    def aceptar(self):
        efectivo = int(self.txtMontoEfectivo.text())
        if efectivo:
            self.btnFin.setEnabled(True)
            self.btnAceptar.setEnabled(False)
            recaudacion = int(self.lcdRecaudado.value())
            apertura =  int(self.lcdMontoApertura.value())
            diferencia = efectivo - (apertura + recaudacion)
            self.lcdDiferencia.setValue(diferencia)
        else:
            QMessageBox.information(self, "Error", "Debe ingresar monto efectivo en caja.",QMessageBox.Ok)

    def fin(self):
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        sql = "SELECT DATE_FORMAT(NOW(), '%Y-%m-%d');"
        cursor = conn.cursor()
        cursor.execute(sql)
        fecha = cursor.fetchone()
        fecha = str(fecha[0]) # ******
        #YA OBTUVE LA HORA
        idUsuario = str(self.lblIdUsuario.text())
        efectivoCaja= str(self.txtMontoEfectivo.text())
        cursor = conn.cursor()
        sql = "UPDATE caja SET montoFinal = " + efectivoCaja + " WHERE idUsuario = " + idUsuario + " AND fecha = '" + fecha + "';"
        print(sql)
        cursor.execute(sql)
        conn.commit()
        self.close()

    def cancelar(self):
            idUsuario = self.lblIdUsuario.text()
            self.btnAceptar.setEnabled(True)
            self.btnFin.setEnabled(False)
            self.close()
            process1 = subprocess.run(['python','venta.py',idUsuario])

app = QApplication(sys.argv)        #inicia aplicacion
qt_traductor = QTranslator()
qt_traductor.load("qtbase_" + QLocale.system().name(),QLibraryInfo.location(QLibraryInfo.TranslationsPath))
app.installTranslator(qt_traductor)
cierreCaja = cierreCaja()                   #Crear objeto de clase ventana
cierreCaja.show()                       #Mostrar la ventana
app.exec_()                         #Ejecutar la aplicacion
