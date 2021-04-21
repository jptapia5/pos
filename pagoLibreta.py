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
import tempfile
import win32api
import win32print
import win32ui
import win32con
import locale

# clase heredada de QMainWindow (Constructor Ventana)


class Window(QMainWindow):
    # Metodo constructor clase
    def __init__(self):
        # Iniciar el objeto
        QMainWindow.__init__(self)
        # Cargar archivo ui en objeto
        uic.loadUi("gui/pagoLibreta.ui", self)
        self.statusBar().showMessage("Bienvenido")
        # recibe el valor de selMedioPago como float
        totalVenta = os.sys.argv[1]
        idUsuario = os.sys.argv[2]  # recibe el valor desde ventas
        idVenta = os.sys.argv[3]  # recibe el valor desde ventas
        locale.setlocale(locale.LC_ALL, 'de_DE.utf-8')
        totalVenta = totalVenta[0:len(totalVenta)-2]
        self.lcdTotalVenta.display(totalVenta)
        self.displayTotalVenta.setValue(int(totalVenta))
        self.lblIdUsuario.setText(idUsuario)
        self.lblidVenta.setText(idVenta)
        int(totalVenta)
        self.btnConsultar.clicked.connect(self.consultar)
        self.btnCancelar.clicked.connect(self.cancelar)
        self.btnFin.clicked.connect(self.fin)
        self.btnFin.setEnabled(False)

        conn = pymysql.connect(host='localhost', user='root',
                               password='JPTapia123', db='mydb')
        sql = "SELECT MAX(folioBoleta) FROM ventas"
        cursor = conn.cursor()
        cursor.execute(sql)
        consulta = cursor.fetchone()
        nroBoleta = int(consulta[0]) + 1
        self.txtNboleta.setValue(nroBoleta)

    def consultar(self, totalVenta):
        conn = pymysql.connect(host='localhost', user='root',
                               password='JPTapia123', db='mydb')
        cursor = conn.cursor()
        idCliente = self.txtIdCliente.value()
        cursor.execute(
            "SELECT nombreCliente,apellidoPaterno,apellidoMaterno,deudaTotal, deudaMaxima FROM clientes WHERE idCliente = %s", idCliente)
        consultas = cursor.fetchone()
        if (consultas):
            nombreCliente = consultas[0] + " " + \
                consultas[1] + " " + consultas[2]
            deudaTotal = int(consultas[3])
            deudaMaxima = int(consultas[4])
            cupo = int(deudaMaxima) - int(deudaTotal)
            pago = int(self.lcdTotalVenta.value())
            self.lblNombreCliente.setText(nombreCliente)
            self.displayDeudaTotal.setValue(deudaTotal)
            self.displayCupoDisponible.setValue(deudaMaxima)
            if (pago > cupo):
                self.btnFin.setEnabled(False)
                QMessageBox.information(
                    self, "Sin cupo", "No tiene cupo disponible.", QMessageBox.Ok)
            else:
                self.btnFin.setEnabled(True)

        else:
            self.btnFin.setEnabled(False)
            QMessageBox.information(
                self, "Error", "No existe el cliente ingresado", QMessageBox.Ok)
            nombreCliente = " "
            deudaTotal = 0
            cupo = 0
            self.lblNombreCliente.setText(nombreCliente)
            self.displayDeudaTotal.setValue(int(deudaTotal))
            self.displayCupoDisponible.setValue(int(cupo))
        cursor.close()

    def fin(self):
        # OBTIENE LA FECHA DE LA BASE DE DATOS
        conn = pymysql.connect(host='localhost', user='root',
                               password='JPTapia123', db='mydb')
        sql = "SELECT DATE_FORMAT(NOW(), '%d-%m-%Y');"
        cursor = conn.cursor()
        cursor.execute(sql)
        fecha = cursor.fetchone()
        fecha = str(fecha[0])
        idVenta = str(self.lblidVenta.text())
        idUsuario = self.lblIdUsuario.text()
        totalVenta = int(self.lcdTotalVenta.value())
        folioBoleta = str(self.txtNboleta.text())
        folioBoleta = str(self.txtNboleta.text())
        idMedioPago = str(2)
        idCliente = self.txtIdCliente.text()
        conn = pymysql.connect(host='localhost', user='root',
                               password='JPTapia123', db='mydb')
        cursor = conn.cursor()
        sql = "SELECT * FROM ventas WHERE folioBoleta = " + folioBoleta
        cursor.execute(sql)
        valida = cursor.fetchone()
        print(valida)
        if valida:
            QMessageBox.warning(
                self, "ERROR", "El numero de boleta ya fue utilizado.", QMessageBox.Ok)
        else:
            sql = "UPDATE ventas SET idMedioPago = " + idMedioPago + ", idCliente = " + \
                idCliente + ", folioBoleta = " + folioBoleta + " WHERE idVenta = " + idVenta
            print(sql)
            cursor.execute(sql)
            conn.commit()
            sql = "SELECT deudaTotal FROM clientes WHERE idCliente = " + idCliente
            cursor.execute(sql)
            consulta = cursor.fetchone()
            deuda = consulta[0]
            deudaActuaizada = int(deuda) + totalVenta
            print(deudaActuaizada)
            sql = "UPDATE clientes SET deudaTotal = '" + \
                str(deudaActuaizada) + "' WHERE idCliente = " + idCliente
            cursor.execute(sql)
            conn.commit()
            print(sql)
            cursor.execute(sql)
# ******************************************   IMPRIMIR TICKET DE VENTA ******************************** ********
            conn = pymysql.connect(
                host='localhost', user='root', password='JPTapia123', db='mydb')
            cursor = conn.cursor()
            sql = "SELECT detalle_venta.cantidad, productos.nombreProducto, detalle_venta.precioUnitario \
                   FROM productos INNER JOIN detalle_venta \
                   ON detalle_venta.idProducto = productos.idProducto \
                   WHERE detalle_venta.idVenta=" + str(idVenta)
            cursor.execute(sql)
            detalleVoucher = cursor.fetchall()
            cursor = conn.cursor()
            sql = "SELECT montoVenta \
                   FROM ventas \
                   WHERE idVenta=" + str(idVenta)
            cursor.execute(sql)
            conn.commit()
            totalVenta = cursor.fetchone()
            totalVoucher = str(totalVenta[0])
            totalVoucher = locale.format('%d', int(totalVoucher), 1)
            idCliente = self.txtIdCliente.text()
            cursor.execute(
                "SELECT deudaTotal, deudaMaxima FROM clientes WHERE idCliente = %s", (idCliente))
            consulta = cursor.fetchone()
            saldoPendiente = consulta[0]
            cupoTotal = consulta[1]
            cupoTotal = cupoTotal-saldoPendiente
            conn.close()
# ********************************                EMPIEZA A IMPRIMIR               ********************************
            idCliente = self.txtIdCliente.text()
            ticketVenta = idVenta
            nroBoleta = self.txtNboleta.value()
            nombreCliente = self.lblNombreCliente.text()
            totalVenta = 0
            archivo = open('voucher.txt', 'w')
            archivo.write('*****************************************')
            archivo.write('\n' + '    	     "ALMACÉN DON TITO"             ')
            archivo.write('\n' + '             ESMERALDA 113               ')
            archivo.write('\n' + '                EL MELÓN                 ')
            archivo.write('\n' + '                                         ')
            archivo.write('\n' + '                                         ')
            archivo.write('*****************************************')
            archivo.write(
                '\n' + '           "TICKET DE VENTA"             ')
            archivo.write(
                '\n' + '                                         ')
            archivo.write('\n' + 'CLIENTE ID : ' + str(idCliente))
            archivo.write('\n' + 'TICKET : ' + str(ticketVenta))
            archivo.write('\n' + 'N° BOLETA: ' + str(nroBoleta))
            archivo.write('\n' + 'FECHA: ' + str(fecha))
            archivo.write('\n' + 'MEDIO DE PAGO : LIBRETA')
            archivo.write('\n' + 'NOMBRE CLIENTE : ' + nombreCliente)
            archivo.write('\n' + '                                         ')
            archivo.write('\n' + '                                         ')
            archivo.write('\n' + '-----------------------------------------')
            archivo.write('\n' + 'CANT -      ARTÍCULOS 	  -       SUBTOTAL')
            cantidadArticulos = 0
            for i in range(len(detalleVoucher)):
                detalleCantidad = str(detalleVoucher[i][0])
                detalleProducto = str(detalleVoucher[i][1])
                longitud = len(detalleProducto)
                while (longitud < 32):
                    detalleProducto = detalleProducto + " "
                    longitud = longitud + 1
                detallaPrecioUnitario = str(detalleVoucher[i][2])
                detallaPrecioUnitario = str(locale.format(
                    '%d', int(detallaPrecioUnitario), 1))
                archivo.write(
                    '\n' + detalleCantidad[0:1] + " " + detalleProducto[0:32] + " $"+detallaPrecioUnitario[0:6])
                cantidadArticulos = cantidadArticulos + int(detalleCantidad)
            archivo.write('\n' + '-----------------------------------------')
            archivo.write('\n' + '                                         ')
            archivo.write('\n' + '                                         ')
            archivo.write('\n' + 'CANT ARTICULOS : ' + str(cantidadArticulos))
            archivo.write('\n' + 'TOTAL DE COMPRA: $' + totalVoucher)
            archivo.write('\n' + '-----------------------------------------')
            archivo.write('\n' + 'SALDO PENDIENTE $' +
                          locale.format('%d', saldoPendiente, 1))
            archivo.write('\n' + 'CUPO DISPONIBLE  $' +
                          locale.format('%d', cupoTotal, 1))
            archivo.write(
                '\n' + '-----------------------------------------')

            archivo.write('\n' + '       GRACIAS POR SU PREFERENCIA')
            archivo.close()
            # IMPRIME EL ARCHIVO TXT
            subprocess.run(['python', 'imprimirVoucher.py'])
# ********************************                  FIN IMPRIMIR                  ********************************
            QMessageBox.information(
                self, "Gracias", "Agradecemos su preferencia. Vuelva cuando guste.", QMessageBox.Ok)
        self.close()
        process1 = subprocess.run(['python', 'venta.py', idUsuario])

    def cancelar(self):
        idUsuario = self.lblIdUsuario.text()
        self.btnFin.setEnabled(False)
        idVenta = str(self.lblidVenta.text())
        conn = pymysql.connect(host='localhost', user='root',
                               password='JPTapia123', db='mydb')
        cursor = conn.cursor()
        sql = "SELECT idProducto, cantidad \
               FROM detalle_venta \
               WHERE idVenta = " + idVenta + ";"
        cursor.execute(sql)
        carro = cursor.fetchall()
        for i in range(len(carro)):
            sql = "UPDATE productos \
                   SET stock = stock + " + str(carro[i][1]) + "\
                   WHERE idProducto = " + str(carro[i][0]) + ";"
            cursor.execute(sql)
            conn.commit()
        sql = "DELETE FROM VENTAS WHERE idVenta = " + idVenta + ";"
        cursor.execute(sql)
        conn.commit()
        conn.close()
        self.close()
        process1 = subprocess.run(['python', 'venta.py', idUsuario])


app = QApplication(sys.argv)  # inicia aplicacion
#  ===================================== Traduccion de botones de QMessageBox ============================================
qt_traductor = QTranslator()
qt_traductor.load("qtbase_" + QLocale.system().name(),
                  QLibraryInfo.location(QLibraryInfo.TranslationsPath))
app.installTranslator(qt_traductor)
window = Window()  # Crear objeto de clase ventana
window.show()  # Mostrar la ventana
app.exec_()  # Ejecutar la aplicacion
