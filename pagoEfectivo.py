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
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog


class window(QMainWindow):
    # Metodo constructor clase
    def __init__(self):
        # Iniciar el objeto
        QMainWindow.__init__(self)
        # Cargar archivo ui en objeto
        uic.loadUi("gui/pagoEfectivo.ui", self)
        self.statusBar().showMessage("Bienvenido")
        self.btnAceptar.setShortcut("Return")
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
        self.btnFin.setEnabled(False)
        # idUsuario = self.lblIdUsuario.text(idUsuario)
        int(totalVenta)
        self.btnAceptar.clicked.connect(self.aceptar)
        self.btnCancelar.clicked.connect(self.cancelar)
        self.btnFin.clicked.connect(self.fin)
        self.btnAceptar.setShortcut("Return")    # Establece atajo con teclado
        self.documento = QTextDocument()
        self.treeWidgetVentas.setFont(
            QFont(self.treeWidgetVentas.font().family(), 10, False))
        self.treeWidgetVentas.setRootIsDecorated(False)
        self.treeWidgetVentas.setHeaderLabels(
            ("PRODUCTO", "PRECIO", "CANTIDAD", "SUBTOTAL"))
        self.model = self.treeWidgetVentas.model()
        for indice, ancho in enumerate((250, 250, 250, 250, 250), start=0):
            self.model.setHeaderData(
                indice, Qt.Horizontal, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.treeWidgetVentas.setColumnWidth(indice, ancho)
        self.treeWidgetVentas.setAlternatingRowColors(True)
        conn = pymysql.connect(host='localhost', user='root',
                               password='JPTapia123', db='mydb')
        sql = "SELECT MAX(folioBoleta) FROM ventas"
        cursor = conn.cursor()
        cursor.execute(sql)
        consulta = cursor.fetchone()
        nroBoleta = int(consulta[0]) + 1
        self.txtNboleta.setValue(nroBoleta)

    def aceptar(self, totalVenta):
        totalVenta = int(self.lcdTotalVenta.value())
        efectivo = self.txtPagaCon.value()
        vuelto = efectivo - totalVenta
        self.lcdVuelto.display(vuelto)
        self.displayVuelto.setValue(vuelto)
        # self.btnAceptar.setEnabled(False)
        if (efectivo >= totalVenta):
            self.btnFin.setEnabled(True)
        else:
            QMessageBox.warning(
                self, "¡Atención!", "El monto efectivo debe ser igual o mayor al que debe pagar.", QMessageBox.Ok)
            self.btnFin.setEnabled(False)

    def fin(self):
        totalVenta = int(self.lcdTotalVenta.value())
        efectivo = self.txtPagaCon.value()
        if (efectivo >= totalVenta):
            conn = pymysql.connect(host='localhost', user='root',
                                   password='JPTapia123', db='mydb')
            sql = "SELECT DATE_FORMAT(NOW(), '%d-%m-%Y');"
            cursor = conn.cursor()
            cursor.execute(sql)
            fecha = cursor.fetchone()
            fecha = str(fecha[0])
            conn.close()
            idVenta = str(self.lblidVenta.text())
            folioBoleta = str(self.txtNboleta.text())
            idMedioPago = str(1)
            idCliente = str(0)  # EN MEDIO DE PAGO EFECTIVO NO REGISTRA CLIENTE
            idUsuario = self.lblIdUsuario.text()
            conn = pymysql.connect(host='localhost', user='root',
                                   password='JPTapia123', db='mydb')
            cursor = conn.cursor()
            sql = "SELECT * FROM ventas WHERE folioBoleta = " + folioBoleta
            cursor.execute(sql)
            valida = cursor.fetchone()
            if valida:
                QMessageBox.warning(
                    self, "ERROR", "Le numero de boleta ya fue utilizado.", QMessageBox.Ok)
            else:
                sql = "UPDATE ventas SET idMedioPago = " + idMedioPago + \
                    ", folioBoleta = " + folioBoleta + " WHERE idVenta = " + idVenta
                cursor.execute(sql)
                conn.commit()
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
                totalVenta = cursor.fetchone()
                totalVoucher = str(totalVenta[0])
                totalVoucher = locale.format('%d', int(totalVoucher), 1)
                conn.close()
    # ********************************                EMPIEZA A IMPRIMIR               ********************************
                idCliente = 0
                ticketVenta = idVenta
                nroBoleta = self.txtNboleta.value()
                nombreCliente = "sin identificar"
                totalVenta = 0
                archivo = open('voucher.txt', 'w')
                archivo.write('*****************************************')
                archivo.write(
                    '\n' + '    	     "ALMACÉN DON TITO"             ')
                archivo.write(
                    '\n' + '             ESMERALDA 113               ')
                archivo.write(
                    '\n' + '                EL MELÓN                 ')
                archivo.write('*****************************************\n')
                archivo.write(
                    '\n' + '           "TICKET DE VENTA"             ')
                archivo.write(
                    '\n' + '                                         ')
                archivo.write('\n' + 'CLIENTE ID : ' + str(idCliente))
                archivo.write('\n' + 'TICKET : ' + str(ticketVenta))
                archivo.write('\n' + 'N° BOLETA: ' + str(nroBoleta))
                archivo.write('\n' + 'FECHA: ' + str(fecha))
                archivo.write('\n' + 'MEDIO DE PAGO : EFECTIVO')
                archivo.write('\n' + 'NOMBRE CLIENTE : ' + nombreCliente)
                archivo.write(
                    '\n' + '                                         ')
                archivo.write(
                    '\n' + '                                         ')
                archivo.write(
                    '\n' + '-----------------------------------------')
                archivo.write(
                    '\n' + 'CANT -      ARTÍCULOS 	  -       SUBTOTAL')
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
                    cantidadArticulos = cantidadArticulos + \
                        int(detalleCantidad)
                archivo.write(
                    '\n' + '-----------------------------------------')
                archivo.write(
                    '\n' + '                                         ')
                archivo.write(
                    '\n' + '                                         ')
                archivo.write('\n' + 'CANT ARTICULOS : ' +
                              str(cantidadArticulos))
                archivo.write('\n' + 'TOTAL DE COMPRA: $' + totalVoucher)
                archivo.write(
                    '\n' + '-----------------------------------------')
                archivo.write('\n' + '       GRACIAS POR SU PREFERENCIA')
                archivo.close()
                # IMPRIME EL ARCHIVO TXT
                subprocess.run(['python', 'imprimirVoucher.py'])
    # ********************************                  FIN IMPRIMIR                  ********************************
                vuelto = self.displayVuelto.value()
                locale.setlocale(locale.LC_ALL, 'de_DE.utf-8')
                vuelto = locale.format_string('%d', vuelto, 1)
                entregarVuelto = "Recuerde que el vuelto del clientes es de : $" + \
                    str(vuelto) + " Pesos"
                QMessageBox.information(
                    self, "Entregue vuelto a cliente", entregarVuelto, QMessageBox.Ok)
                self.close()
                process1 = subprocess.run(['python', 'venta.py', idUsuario])
        else:
            QMessageBox.warning(
                self, "¡Atención!", "El monto efectivo debe ser igual o mayor al que debe pagar.", QMessageBox.Ok)
            self.btnFin.setEnabled(False)

    def cancelar(self):
        idUsuario = self.lblIdUsuario.text()
        self.btnAceptar.setEnabled(True)
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
window = window()  # Crear objeto de clase ventana
window.show()  # Mostrar la ventana
app.exec_()  # Ejecutar la aplicacion
