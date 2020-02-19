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

# =============== CLASE visualizarImprimirExportar =================

class consultaVentasDia(QMainWindow):
    def __init__(self):
        #Iniciar el objeto
        QMainWindow.__init__(self)
        uic.loadUi("gui/consultaPrecioHistoricoProductos.ui",self)
        self.setWindowTitle("Visualizar, imprimir y exportar datos a PDF de Precio Historico de Productos")
        self.setWindowIcon(QIcon("Qt.png"))
        self.btnVistaPrevia.clicked.connect(self.vistaPrevia)
        self.btnLimpiarTabla.clicked.connect(self.limpiarTabla)
        self.btnExportarPDF.clicked.connect(self.exportarPDF)
        self.btnConsultar.clicked.connect(self.Buscar)
        self.btnImprimir.clicked.connect(self.Imprimir)
        self.btnSalir.clicked.connect(self.salir)
        self.documento = QTextDocument()
        self.treeWidgetVentas.setFont(QFont(self.treeWidgetVentas.font().family(), 10, False))
        self.treeWidgetVentas.setRootIsDecorated(False)
        self.treeWidgetVentas.setHeaderLabels(("CODIGO", "DESCRIPCION", "FECHA", "PRECIO COSTO", "PRECIO VENTA" ))
        self.model = self.treeWidgetVentas.model()

        for indice, ancho in enumerate((250, 250, 250, 250, 250), start=0):
            self.model.setHeaderData(indice, Qt.Horizontal, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.treeWidgetVentas.setColumnWidth(indice, ancho)

        self.treeWidgetVentas.setAlternatingRowColors(True)


  # ======================= FUNCIONES ============================
  #==============================================================
  #==============================================================
  #==============================================================
  #==============================================================
  #==============================================================

    def Buscar(self):
        idProducto = str(self.txtBuscar.text())
        if idProducto:
                    conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
                    cursor = conn.cursor()
                    #sql = "SELECT nombreUsuario, apellidoPaterno FROM usuarios WHERE idProducto = " + idProducto
                    sql = "SELECT productos.idProducto, productos.nombreProducto, precio_producto.fecha, precio_producto.precioCosto,precio_producto.precioVenta FROM productos, precio_producto WHERE productos.idProducto = precio_producto.idProducto AND productos.idProducto = " + idProducto
                    cursor.execute(sql)
                    datosDB = cursor.fetchall()
                    conn.close()
                    if datosDB:
                        self.documento.clear()
                        self.treeWidgetVentas.clear()
                        datos = ""
                        item_widget = []
                        for dato in datosDB:
                            datos += "<tr><td>%s</td> <td>%s</td> <td>%s</td><td>%s</td> <td>%s</td></tr>" %dato
                            item_widget.append(QTreeWidgetItem((str(dato[0]), str(dato[1]), str(dato[2]), str(dato[3]), str(dato[4]))))
                        reporteHtml = """
            <!DOCTYPE html>
            <html>
            <head>
            <meta charset="UTF-8">
            <style>
            h3 {
                font-family: Helvetica-Bold;
                text-align: center;
               }
            table {
                   font-family: arial, sans-serif;
                   border-collapse: collapse;
                   width: 100%;
                  }
            td {
                text-align: left;
                padding-top: 4px;
                padding-right: 6px;
                padding-bottom: 2px;
                padding-left: 6px;
               }
            th {
                text-align: left;
                padding: 4px;
                background-color: black;
                color: white;
               }
            tr:nth-child(even) {
                                background-color: #dddddd;
                               }
            #lateral { width: 200px; }
            </style>
            <div id="lateral">
            </head>
            <body>
            <h3>LISTADO DE PRECIO PRODUCTOS<br/></h3>
            <table align="left" width="100%" cellspacing="0">
              <tr>
                <th>IDPRODUCTO</th>
                <th>DESCRIPCION</th>
                <th>FECHA</th>
                <th>PRECIO COSTO</th>
                <th>PRECIO VENTA</th>
              </tr>
              [DATOS]
            </table>
            </body>
            </div>
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
                        QMessageBox.information(self, "Precio Productos", "No se encontraron resultados.      ", QMessageBox.Ok)

        else:
                QMessageBox.information(self, "Buscar Comunas", "Ingrese codigo producto a consultar.      ", QMessageBox.Ok)


    def limpiarTabla(self):
        self.documento.clear()
        self.treeWidgetVentas.clear()
        self.txtBuscar.setText("")

    def vistaPrevia(self):
        if not self.documento.isEmpty():
            impresion = QPrinter(QPrinter.HighResolution)
            vista = QPrintPreviewDialog(impresion, self)
            vista.setWindowTitle("Vista previa")
            vista.setWindowFlags(Qt.Window)
            vista.resize(800, 600)

            exportarPDF = vista.findChildren(QToolBar)
            exportarPDF[0].addAction(QIcon("exportarPDF.png"), "Exportar a PDF", self.exportarPDF)

            vista.paintRequested.connect(self.vistaPreviaImpresion)
            vista.exec_()
        else:
            QMessageBox.critical(self, "Vista previa", "No hay datos para visualizar.   ",
                                 QMessageBox.Ok)

    def vistaPreviaImpresion(self, impresion):
        self.documento.print_(impresion)

    def salir(self):
        self.close()

    def Imprimir(self):
        if not self.documento.isEmpty():
            impresion = QPrinter(QPrinter.HighResolution)

            dlg = QPrintDialog(impresion, self)
            dlg.setWindowTitle("Imprimir documento")

            if dlg.exec_() == QPrintDialog.Accepted:
                self.documento.print_(impresion)

            del dlg
        else:
            QMessageBox.critical(self, "Imprimir", "No hay datos para imprimir.   ",
                                 QMessageBox.Ok)

    def exportarPDF(self):
        if not self.documento.isEmpty():
            nombreArchivo, _ = QFileDialog.getSaveFileName(self, "Exportar a PDF", "Listado de usuarios",
                                                           "Archivos PDF (*.pdf);;All Files (*)",
                                                           options=QFileDialog.Options())

            if nombreArchivo:
                # if QFileInfo(nombreArchivo).suffix():
                #     nombreArchivo += ".pdf"

                impresion = QPrinter(QPrinter.HighResolution)
                impresion.setOutputFormat(QPrinter.PdfFormat)
                impresion.setOutputFileName(nombreArchivo)
                self.documento.print_(impresion)

                QMessageBox.information(self, "Exportar a PDF", "Datos exportados con éxito.   ",
                                        QMessageBox.Ok)
        else:
            QMessageBox.critical(self, "Exportar a PDF", "No hay datos para exportar.   ",
                                 QMessageBox.Ok)
app = QApplication(sys.argv)
consultaVentasDia = consultaVentasDia()
consultaVentasDia.show()
app.exec_()
