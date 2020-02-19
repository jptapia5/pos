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
class window(QMainWindow):
    #Metodo constructor clase
    def __init__(self):
        #Iniciar el objeto
        QMainWindow.__init__(self)
        #Cargar archivo ui en objeto
        uic.loadUi("gui/pagoEfectivo.ui",self)
        self.statusBar().showMessage("Bienvenido")
        totalVenta = os.sys.argv[1]   #recibe el valor de selMedioPago como float
        idUsuario = os.sys.argv[2]  #recibe el valor desde ventas
        idVenta = os.sys.argv[3]  #recibe el valor desde ventas
        print(totalVenta)
        print(idUsuario)
        print(idVenta)
        totalVenta =  totalVenta[0:len(totalVenta)-2]
        self.lcdTotalVenta.display(totalVenta)
        self.displayTotalVenta.setValue(int(totalVenta))
        self.lblIdUsuario.setText(idUsuario)
        self.lblidVenta.setText(idVenta)
        int(totalVenta)
        self.btnAceptar.clicked.connect(self.aceptar)
        self.btnCancelar.clicked.connect(self.cancelar)
        self.btnFin.clicked.connect(self.fin)

        #    DOC IMPRIMIR TICKET
        self.documento = QTextDocument()
        self.treeWidgetVentas.setFont(QFont(self.treeWidgetVentas.font().family(), 10, False))
        self.treeWidgetVentas.setRootIsDecorated(False)
        self.treeWidgetVentas.setHeaderLabels(("PRODUCTO", "PRECIO", "CANTIDAD", "SUBTOTAL" ))
        self.model = self.treeWidgetVentas.model()

        for indice, ancho in enumerate((250, 250, 250, 250, 250), start=0):
            self.model.setHeaderData(indice, Qt.Horizontal, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.treeWidgetVentas.setColumnWidth(indice, ancho)

        self.treeWidgetVentas.setAlternatingRowColors(True)

    def aceptar(self,totalVenta):
        totalVenta = int(self.lcdTotalVenta.value())
        efectivo = self.txtPagaCon.value()
        vuelto = efectivo - totalVenta
        self.lcdVuelto.display(vuelto)
        self.displayVuelto.setValue(vuelto)
        #self.btnAceptar.setEnabled(False)
        self.btnFin.setEnabled(True)
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        sql = "SELECT MAX(folioBoleta) FROM ventas"
        cursor = conn.cursor()
        cursor.execute(sql)
        consulta = cursor.fetchone()
        nroBoleta = int(consulta[0]) + 1
        print(nroBoleta)
        self.txtNboleta.setValue(nroBoleta)

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
        #totalVenta = self.lcdTotalVenta.value()
        folioBoleta = str(self.txtNboleta.text())
        idMedioPago = str(1)  # YA SE SABE QUE EL MEDIO DE PAGO ES EN EFECTIVO POR LO TANTO EL ID QUE CORRESPONDE ES 1
        idCliente = str(0) # EN MEDIO DE PAGO EFECTIVO NO REGISTRA CLIENTE
        idUsuario = self.lblIdUsuario.text()
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        cursor = conn.cursor()
        sql = "SELECT * FROM ventas WHERE folioBoleta = " + folioBoleta
        print(sql)
        cursor.execute(sql)
        valida = cursor.fetchone()
        if valida:
                QMessageBox.warning(self, "ERROR", "Le numero de boleta ya fue utilizado.",QMessageBox.Ok)
        else:
                sql = "UPDATE ventas SET idMedioPago = " + idMedioPago + ", idCliente = " + idCliente + ", folioBoleta = " + folioBoleta + " WHERE idVenta = " + idVenta
                print(sql)
                cursor.execute(sql)
                conn.commit()
                #******************************************   IMPRIMIR TICKET DE VENTA ******************************** ********
                #***************************************************************************************************************

                conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
                cursor = conn.cursor()
                sql = "SELECT detalle_venta.cantidad, productos.nombreProducto, detalle_venta.precioUnitario, detalle_venta.subtotal FROM productos, detalle_venta WHERE detalle_venta.idVenta = " + idVenta + " AND  detalle_venta.idProductos = productos.idProducto"
                print(sql)
                cursor.execute(sql)
                datosDB = cursor.fetchall()
                print(datosDB)
                conn.close()
                if datosDB:
                    self.documento.clear()
                    self.treeWidgetVentas.clear()
                    datos = ""
                    item_widget = []
                    for dato in datosDB:
                        datos += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" %dato
                        item_widget.append(QTreeWidgetItem((str(dato[0]), str(dato[1]), str(dato[2]), str(dato[3]))))
                        reporteHtml = """
                                    <!DOCTYPE html>
                                    <html>
                                    <head>
                                    <meta charset="UTF-8">
                                    <style>
                                    table {
                                        width: 720mm;
                                          }
                                    td {

                                       }
                                    th {
                                        width: 180mm;
                                       }
                                       tr {
                                         width: 180mm;
                                          }
                                    body
                                        {
                                        width: 720mm;
                                        }
                                    </style>
                                    </head>
                                    <body>
                                    <table>
                                      <tr>
                                        <th style="text-align:center;">Cant</th>
                                        <th style="text-align:center;">Articulo</th>
                                        <th style="text-align:center;">Precio</th>
                                        <th style="text-align:center;">Subtotal</th>
                                      </tr>
                                      [DATOS]
                                    </table>
                                    </body>
                                    </html>
        """.replace("[DATOS]", datos)
                    datos = QByteArray()
                    datos.append(str(reporteHtml))
                    codec = QTextCodec.codecForHtml(datos)
                    unistr = codec.toUnicode(datos)
                    if Qt.mightBeRichText(unistr):
                        self.documento.setHtml(unistr)
                    else:
                        self.documento.setPlainText(unistr)
                    self.treeWidgetVentas.addTopLevelItems(item_widget)

                else:
                        QMessageBox.information(self, "ERROR", "No se encontraron resultados.      ", QMessageBox.Ok)

                if not self.documento.isEmpty():
                    impresion = QPrinter(QPrinter.PrinterResolution)
                    dlg = QPrintDialog(impresion, self)
                    #dlg.setWindowTitle("Imprimir documento")
                    if dlg.exec_() == QPrintDialog.Accepted:
                        self.documento.print_(impresion)
                    del dlg
                else:
                    QMessageBox.critical(self, "Imprimir", "No hay datos para imprimir.   ",
                                         QMessageBox.Ok)
                QMessageBox.information(self, "Gracias", "Agradecemos su preferencia. Vuelva cuando guste.",QMessageBox.Ok)
                self.close()
                process1 = subprocess.run(['python','venta.py',idUsuario])


    def cancelar(self):
        idUsuario = self.lblIdUsuario.text()
        self.btnAceptar.setEnabled(True)
        self.btnFin.setEnabled(False)
        self.close()
        process1 = subprocess.run(['python','venta.py',idUsuario])

app = QApplication(sys.argv)        #inicia aplicacion
#  ===================================== Traduccion de botones de QMessageBox ============================================
qt_traductor = QTranslator()
qt_traductor.load("qtbase_" + QLocale.system().name(),QLibraryInfo.location(QLibraryInfo.TranslationsPath))
app.installTranslator(qt_traductor)
window = window()                   #Crear objeto de clase ventana
window.show()                       #Mostrar la ventana
app.exec_()                         #Ejecutar la aplicacion
