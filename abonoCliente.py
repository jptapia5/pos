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
import locale
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog


class Window(QMainWindow):
    # Metodo constructor clase
    def __init__(self):
        # Iniciar el objeto
        QMainWindow.__init__(self)
        # Cargar archivo ui en objeto
        uic.loadUi("gui/abonoCliente2.ui", self)
        self.statusBar().showMessage("Ingrese un pago realizado por un cliente.")
        self.btnAceptar.clicked.connect(self.aceptar)
        self.btnFin.clicked.connect(self.finalizar)
        self.btnCancelar.clicked.connect(self.cancelar)
        self.fechaActual()
        if len(os.sys.argv) > 1:
            idUsuario = os.sys.argv[1]
            idCliente = os.sys.argv[2]
            self.lblidUsuario.setText(idUsuario)
            self.lbIdlCliente.setText(idCliente)
        self.consultaCliente()
        self.btnFin.setEnabled(False)
        locale.setlocale(locale.LC_ALL, 'de_DE.utf-8')

    def fechaActual(self):
        conn = pymysql.connect(host='localhost', user='root',
                               password='JPTapia123', db='mydb')
        sql = "SELECT DATE_FORMAT(NOW(), '%d-%m-%Y');"
        cursor = conn.cursor()
        cursor.execute(sql)
        fecha = cursor.fetchone()
        fecha = str(fecha[0])
        # print(fecha)
        self.lblFechaActual.setText(fecha)
        conn.close()

    def consultaCliente(self):
        idCliente = self.lbIdlCliente.text()
        print("este abonara" + idCliente)
        if(idCliente):
            conn = pymysql.connect(
                host='localhost', user='root', password='JPTapia123', db='mydb')
            cursor = conn.cursor()
            cursor.execute(
                "SELECT deudaTotal, nombreCliente, apellidoPaterno, apellidoMaterno FROM clientes WHERE idCliente = %s", idCliente)
            consulta = cursor.fetchone()
            deuda = int(consulta[0])
            nombre = consulta[1] + " " + consulta[2] + " " + consulta[3]
            self.lcdSaldoAdeudado.setValue(deuda)
            self.lblNombreCliente.setText(nombre)
            self.txtTotalAbono.setEnabled(True)
            self.txtPaga.setEnabled(True)
            self.btnAceptar.setEnabled(True)
            conn.close()
        else:
            QMessageBox.information(
                self, 'Error', "Debe ingresar numero de cliente", QMessageBox.Ok)

    def aceptar(self):
        totalAbono = self.txtTotalAbono.value()
        efectivo = self.txtPaga.value()
        deuda = self.lcdSaldoAdeudado.value()
        if(totalAbono and efectivo and (efectivo >= totalAbono) and (totalAbono <= deuda)):
            vuelto = int(efectivo) - int(totalAbono)
            self.lcdVuelto.setValue(vuelto)
            self.btnFin.setEnabled(True)
            self.txtPaga.setEnabled(False)
        else:
            QMessageBox.information(
                self, 'Error', "No ha ingresado correctamente algun monto", QMessageBox.Ok)
            self.btnFin.setEnabled(False)

    def finalizar(self):
        fecha = self.lblFechaActual.text()
        totalAbono = self.txtTotalAbono.value()
        efectivo = self.txtPaga.value()
        vuelto = self.lcdVuelto.value()
        totalAbono = locale.format('%d', totalAbono, 1)
        respuesta = QMessageBox.warning(self, 'Advertencia', "¿Está usted seguro de abonar $" + str(
            totalAbono) + " pesos?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if respuesta == QMessageBox.Yes:
            deudaTotal = self.lcdSaldoAdeudado.value()
            idCliente = self.lbIdlCliente.text()
            montoPagado = self.txtTotalAbono.value()
            deudaActualizada = int(deudaTotal) - int(montoPagado)
            idUsuario = self.lblidUsuario.text()
            conn = pymysql.connect(host='localhost', user='root',
                                   password='JPTapia123', db='mydb')
            sql = "SELECT DATE_FORMAT(NOW(), '%Y-%m-%d %h:%m:%s');"
            cursor = conn.cursor()
            cursor.execute(sql)
            consulta = cursor.fetchone()
            fechaPago = str(consulta[0])
            cursor.execute(
                "SELECT * FROM abono_cliente WHERE idCliente = %s AND fechaPago = %s", (idCliente, fechaPago))
            consulta = cursor.fetchone()
            cursor.close()
            if (consulta):
                QMessageBox.information(
                    self, 'Información', "Ya ha realizado un abono, solo puede realizar una pago diario.", QMessageBox.Ok)
            else:
                conn = pymysql.connect(
                    host='localhost', user='root', password='JPTapia123', db='mydb')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO abono_cliente (idCliente,fechaPago,monto,IdUsuario) VALUES (%s,%s,%s,%s)",
                               (idCliente, fechaPago, montoPagado, idUsuario))
                conn.commit()
                cursor.execute(
                    "UPDATE clientes SET deudaTotal = %s WHERE idCliente = %s", (deudaActualizada, idCliente))
                conn.commit()
                cursor.execute(
                    "SELECT deudaTotal, deudaMaxima FROM clientes WHERE idCliente = %s", (idCliente))
                consulta = cursor.fetchone()
                saldoPendiente = consulta[0]
                cupoTotal = consulta[1]
                cupoTotal = cupoTotal-saldoPendiente

                # ********************************                EMPIEZA A IMPRIMIR               ********************************
                idCliente = self.lbIdlCliente.text()
                nombreCliente = self.lblNombreCliente.text()
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
                    '\n' + '           "COMPROBANTE DE PAGO"             ')
                archivo.write(
                    '\n' + '                                         ')
                archivo.write('\n' + 'CLIENTE ID : ' + str(idCliente))
                archivo.write('\n' + 'NOMBRE CLIENTE : ' + nombreCliente)
                archivo.write('\n' + 'FECHA  :' + fecha)
                archivo.write(
                    '\n' + '                                         ')
                archivo.write(
                    '\n' + '                                         ')
                archivo.write(
                    '\n' + '-----------------------------------------')
                archivo.write(
                    '\n' + '-----------------------------------------')
                archivo.write(
                    '\n' + '           EL CLIENTE HA CANCELADO      ')
                archivo.write('\n' + '        LA SUMA DE $: ' +
                              str(totalAbono) + ' PESOS')
                archivo.write(
                    '\n' + '-----------------------------------------')
                archivo.write(
                    '\n' + '-----------------------------------------')
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
            conn.close()
            self.close()

    def cancelar(self):
        self.close()


app = QApplication(sys.argv)  # inicia aplicacion
#  ===================================== Traduccion de botones de QMessageBox ============================================
qt_traductor = QTranslator()
qt_traductor.load("qtbase_" + QLocale.system().name(),
                  QLibraryInfo.location(QLibraryInfo.TranslationsPath))
app.installTranslator(qt_traductor)
window = Window()  # Crear objeto de clase ventana
window.show()  # Mostrar la ventana
app.exec_()  # Ejecutar la aplicacion
