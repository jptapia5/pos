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
import locale

#clase heredada de QMainWindow (Constructor Ventana)
class cuentaCliente(QMainWindow):
    #Metodo constructor clase
    def __init__(self):
        #Iniciar el objeto
        QMainWindow.__init__(self)
        #Cargar archivo ui en objeto
        uic.loadUi("gui/cuentaClientes.ui",self)
        self.statusBar().showMessage("Bienvenido")
        self.btnConsulta.clicked.connect(self.consulta)
        self.btnAbonar.clicked.connect(self.abonar)
        self.btnSalir.clicked.connect(self.salir)
        idUsuario = os.sys.argv[1]  #recibe el valor desde ventas
        self.lblIdUsuario.setText(idUsuario)
        self.contruirPagos()
        self.btnAbonar.setEnabled(False)
        
     


    def contruirPagos(self):
            # ==================== CONSTRUCCION DE LA TABLA LISTA ABONO ================================
            self.listaAbonos.setColumnCount(3) #MODIFICAR TENGO QUE CONSULTAR OTRAS TABLAS
            self.listaAbonos.verticalHeader().setVisible(False)    # Ocultar encabezado vertical
            self.listaAbonos.setDragDropOverwriteMode(False)    # Deshabilitar el comportamiento de arrastrar y soltar
            self.listaAbonos.horizontalHeader().setHighlightSections(False)    # Deshabilitar resaltado del texto del encabezado al seleccionar una fila
            self.listaAbonos.setSortingEnabled(True) # Habilita orden descendente o ascendente
            self.listaAbonos.setSelectionBehavior(QAbstractItemView.SelectRows) #Selecciona la fila completa
            self.listaAbonos.setSelectionMode(QAbstractItemView.SingleSelection) # Selecciona una fila a la vez
            self.listaAbonos.verticalHeader().setVisible(False)    # Ocultar encabezado vertical
            self.listaAbonos.setEditTriggers(QAbstractItemView.NoEditTriggers)
            #MODIFICAR HAY QUE CONSULTAR OTRAS TABLAS
            columnas = ('FECHA PAGO', 'MONTO', 'CAJERO')
            self.listaAbonos.setHorizontalHeaderLabels(columnas)
            for indice, ancho in enumerate((206, 206, 206), start=0):
                self.listaAbonos.setColumnWidth(indice, ancho)
            # ==================== CONSTRUCCION DE LA TABLA LISTA VENTAS ================================
            self.listaVentas.setColumnCount(4) #MODIFICAR TENGO QUE CONSULTAR OTRAS TABLAS
            self.listaVentas.verticalHeader().setVisible(False)    # Ocultar encabezado vertical
            self.listaVentas.setDragDropOverwriteMode(False)    # Deshabilitar el comportamiento de arrastrar y soltar
            self.listaVentas.horizontalHeader().setHighlightSections(False)    # Deshabilitar resaltado del texto del encabezado al seleccionar una fila
            self.listaVentas.setSortingEnabled(True) # Habilita orden descendente o ascendente
            self.listaVentas.setSelectionBehavior(QAbstractItemView.SelectRows) #Selecciona la fila completa
            self.listaVentas.setSelectionMode(QAbstractItemView.SingleSelection) # Selecciona una fila a la vez
            self.listaVentas.verticalHeader().setVisible(False)    # Ocultar encabezado vertical
            self.listaVentas.setEditTriggers(QAbstractItemView.NoEditTriggers)
            #MODIFICAR HAY QUE CONSULTAR OTRAS TABLAS
            columnas = ('FECHA COMPRA','BOLETA', 'MONTO', 'CAJERO')
            self.listaVentas.setHorizontalHeaderLabels(columnas)
            for indice, ancho in enumerate((155, 155, 154, 154), start=0):
                self.listaVentas.setColumnWidth(indice, ancho)

    def limpiar(self):
        items = self.listaAbonos.rowCount()
        #print(str(items) + " cantidad items en lista de abono debe dar cero")
        for row in range(0, items):
                #print(row)
                self.listaAbonos.removeRow(0) #borra el item 1 la cantidad de veces que item habia al precionar anular.
        #limpiar lista de ventas
        items = self.listaVentas.rowCount()
        #print(str(items) + " cantidad items en lista de ventas debe dar cero")
        for row in range(0, items):
                #print(row)
                self.listaVentas.removeRow(0) #borra el item 1 la cantidad de veces que item habia al precionar anular.
        self.contruirPagos()

    def consulta(self):
        #consulta por las pagos que realizó el cliente
        self.limpiar()
        idCliente  = str(self.txtCliente.text())
        print(idCliente + " Cliente consultado")
        self.lbIdlCliente.setText(idCliente)
        if idCliente:
                    self.btnAbonar.setEnabled(True)
                    self.lblNombreCliente.setText(idCliente)
                    conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
                    sql = "SELECT nombreCliente, apellidoPaterno, apellidoMaterno FROM clientes WHERE idCliente = " + idCliente
                    cursor = conn.cursor()
                    cursor.execute(sql)
                    consultaNombre = cursor.fetchone()
                    print(consultaNombre)
                    if consultaNombre:
                            nombreCompleto = str(consultaNombre[0]) + " " + str(consultaNombre[1]) + " " + str(consultaNombre[2])
                            self.lblNombreCliente.setText(nombreCompleto)
                            sql = "SELECT DATE_FORMAT(fechaPago,'%d/%m/%y'), monto, idUsuario FROM abono_cliente WHERE idCliente = " + idCliente
                            cursor = conn.cursor()
                            cursor.execute(sql)
                            consultas = cursor.fetchall()
                    # CONSULTA SI EL CLIENTE EXISTE Y AGREGA TODAS LOS ABONOS A LA LISTA
                            row = 0
                            for consulta in consultas:
                                            self.listaAbonos.insertRow(row)
                                            fechaPago = QTableWidgetItem(str(consulta[0]))
                      # PODRÍA AGREGAR EL PUNTO AL VALOR DE MILES
                                            monto = QTableWidgetItem("$" + str(consulta[1]))
                                            idUsuario = QTableWidgetItem(str(consulta[2]))
                                            self.listaAbonos.setItem(row, 0, fechaPago)
                                            self.listaAbonos.setItem(row, 1, monto)
                                            self.listaAbonos.setItem(row, 2, idUsuario)
                                            row = row + 1
                            # ***********         OBTENDRÁ LA SUMA DE ABONOS DEL CLIENTE     ***********
                            sql = "SELECT SUM(monto) FROM abono_cliente WHERE idCliente = " + idCliente
                            cursor = conn.cursor()
                            cursor.execute(sql)
                            consultaAbonos = cursor.fetchone()
                            print("Consulta Total Abonos")
                            print(consultaAbonos[0])
                            if consultaAbonos[0] != None:
                                    abonos = int(consultaAbonos[0])
                                    print(abonos)
                                    self.lcdTotalAbonos.setValue(abonos)
                                    print("Segunda iteracion, devuelve datos de la consulta")
                            else  :
                                    abonos = 0
                                    self.lcdTotalAbonos.setValue(abonos)
                                    print("Segunda iteracion, NO devuelve datos de la consulta asigna cero")
                        # *****   consulta por las compras que realizó el cliente        
                            #columnas = ('FECHA COMPRA','BOLETA', 'MONTO', 'CAJERO')
                            #conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
                            sql = "SELECT DATE_FORMAT(fechaVenta,'%d/%m/%y'), folioBoleta ,montoVenta, idUsuario FROM ventas WHERE idCliente = " + idCliente
                            cursor = conn.cursor()
                            cursor.execute(sql)
                            consultas2 = cursor.fetchall()
                            row = 0
                            # *********          LLENAR LISTA DE VENTAS DEL CLIENTE        ***********
                            for consultas in consultas2:
                                        self.listaVentas.insertRow(row)
                                        fechaVenta = QTableWidgetItem(str(consultas[0]))
                                        folioBoleta = QTableWidgetItem(str(consultas[1]))
                    # PODRÍA AGREGAR EL PUNTO AL VALOR DE MILES
                                        montoVenta = QTableWidgetItem("$ " + str(consultas[2]))
                                        idUsuario = QTableWidgetItem(str(consultas[3]))
                                        self.listaVentas.setItem(row, 0, fechaVenta)
                                        self.listaVentas.setItem(row, 1, folioBoleta)
                                        self.listaVentas.setItem(row, 2, montoVenta)
                                        self.listaVentas.setItem(row, 3, idUsuario)
                                        row = row + 1
                            sql = "SELECT SUM(montoVenta) FROM ventas WHERE idCliente = " + idCliente
                            cursor = conn.cursor()
                            cursor.execute(sql)
                            consultaVentas = cursor.fetchone()
                            print("la siguiente linea devuelve")
                            print(consultaVentas)
                    # 
                            if consultaVentas[0] != None:
                                ventas = int(consultaVentas[0])
                                print(ventas)
                                self.lcdTotalVentas.setValue(ventas)
                                deuda = int(ventas) - int(abonos)
                                self.lblDeudaTotal.setValue(deuda)
                                conn.close()
                            else:   
                                    ventas = 0
                                    self.lcdTotalVentas.setValue(ventas)
                                    deuda = int(ventas) - int(abonos)
                                    self.lblDeudaTotal.setValue(deuda)
                            if deuda == 0:
                                        self.btnAbonar.setEnabled(False)
                        
                    else:
                            self.btnAbonar.setEnabled(False)
                            self.lcdTotalVentas.setValue(0)
                            self.lblDeudaTotal.setValue(0)
                            self.lcdTotalAbonos.setValue(0)
                            QMessageBox.critical(self, "Error", "Cliente consultado no existe",QMessageBox.Ok)

        else:
                self.lcdTotalVentas.setValue(0)
                self.lblDeudaTotal.setValue(0)
                self.lcdTotalAbonos.setValue(0)
                QMessageBox.critical(self, "Error", "Debe ingresar el número de cliente a consultar",QMessageBox.Ok)
       
    def abonar(self):
        idUsuario = self.lblIdUsuario.text()
        idCliente = self.lbIdlCliente.text()
        print(idUsuario + " " + idCliente)
        if idUsuario and idCliente:
                    self.close()
                    process1 = subprocess.run(['python','abonoCliente2.py', idUsuario, idCliente])
        else:
                     QMessageBox.critical(self, "Error", "Debe ingresar el número de cliente a consultar",QMessageBox.Ok)            
    def salir(self):
        self.close()

app = QApplication(sys.argv)        #inicia aplicacion
#  ===================================== Traduccion de botones de QMessageBox ============================================
qt_traductor = QTranslator()
qt_traductor.load("qtbase_" + QLocale.system().name(),QLibraryInfo.location(QLibraryInfo.TranslationsPath))
app.installTranslator(qt_traductor)
cuentaCliente = cuentaCliente()                   #Crear objeto de clase ventana
cuentaCliente.show()                       #Mostrar la ventana
app.exec_()                         #Ejecutar la aplicacion
