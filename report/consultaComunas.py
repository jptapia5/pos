# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Nombre:       visualizarImprimirExportar.py
# Autor:        Miguel Andres Garcia Niño
# Correo:       andres_garcia1996@hotmail.com
# Creado:       26 de Julio 2018
# Modificado:   26 de Julio 2018
# Copyright:    (c) 2018 by Miguel Andres Garcia Niño, 2018
# License:      Apache License 2.0
# ----------------------------------------------------------------------------

__versión__ = "1.0"

"""
El módulo *visualizarImprimirExportar* permite realizar consultas a una Base de Datos, mostrar los
resultados en una tabla y en una vista previa de impresión, también permite imprimir y exportar los
resultados a un PDF.
"""

# Versión Python: 3.5.2
# Versión PyQt5: 5.10.0

from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
import pymysql
import sys
import subprocess
import pymysql
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic


# =============== CLASE visualizarImprimirExportar =================

class visualizarImprimirExportar(QDialog):
    def __init__(self, parent=None):
        super(visualizarImprimirExportar, self).__init__()

        self.setWindowTitle("Visualizar, imprimir y exportar datos a PDF de comunas")
        self.setWindowIcon(QIcon("Qt.png"))
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        self.setFixedSize(612, 408)

        self.initUI()

    def initUI(self):
        self.documento = QTextDocument()

      # =================== WIDGETS QPUSHBUTTON ==================

        buttonBuscar = QPushButton("Buscar Comunas", self)
        buttonBuscar.setFixedSize(426, 26)
        buttonBuscar.move(20, 20)

        buttonLimpiar = QPushButton("Limpiar tabla", self)
        buttonLimpiar.setFixedSize(140, 26)
        buttonLimpiar.move(452, 20)

      # =================== WIDGET QTREEWIDGET ===================

        self.treeWidgetUsuarios = QTreeWidget(self)

        self.treeWidgetUsuarios.setFont(QFont(self.treeWidgetUsuarios.font().family(), 10, False))
        self.treeWidgetUsuarios.setRootIsDecorated(False)
        self.treeWidgetUsuarios.setHeaderLabels(("Codigo", "Comuna" ))

        self.model = self.treeWidgetUsuarios.model()

        for indice, ancho in enumerate((110, 150, 150, 160), start=0):
            self.model.setHeaderData(indice, Qt.Horizontal, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.treeWidgetUsuarios.setColumnWidth(indice, ancho)

        self.treeWidgetUsuarios.setAlternatingRowColors(True)

        self.treeWidgetUsuarios.setFixedSize(572, 300)
        self.treeWidgetUsuarios.move(20, 56)

      # =================== WIDGETS QPUSHBUTTON ==================

        buttonVistaPrevia = QPushButton("Vista previa", self)
        buttonVistaPrevia.setFixedSize(140, 26)
        buttonVistaPrevia.move(156, 364)

        buttonImprimir = QPushButton("Imprimir", self)
        buttonImprimir.setFixedSize(140, 26)
        buttonImprimir.move(304, 364)

        buttonExportarPDF = QPushButton("Exportar a PDF", self)
        buttonExportarPDF.setFixedSize(140, 26)
        buttonExportarPDF.move(452, 364)

      # =================== EVENTOS QPUSHBUTTON ==================

        buttonBuscar.clicked.connect(self.Buscar)
        buttonLimpiar.clicked.connect(self.limpiarTabla)

        buttonVistaPrevia.clicked.connect(self.vistaPrevia)
        buttonImprimir.clicked.connect(self.Imprimir)
        buttonExportarPDF.clicked.connect(self.exportarPDF)

  # ======================= FUNCIONES ============================
  #==============================================================
  #==============================================================
  #==============================================================
  #==============================================================
  #==============================================================

    def Buscar(self):
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        cursor = conn.cursor()
        #cursor.execute("SELECT idUsuario, nombreUsuario, apellidoPaterno, apellidoMaterno, fono, correo, contrasena FROM usuario")
        cursor.execute("SELECT * FROM comunas")
        datosDB = cursor.fetchall()
        conn.close()
        if datosDB:
            self.documento.clear()
            self.treeWidgetUsuarios.clear()
            datos = ""
            item_widget = []
            for dato in datosDB:
                datos += "<tr><td>%s</td><td>%s</td></tr>" %dato
                item_widget.append(QTreeWidgetItem((str(dato[0]), dato[1],)))
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
<h3>LISTADO DE USUARIOS<br/></h3>
<table align="left" width="100%" cellspacing="0">
  <tr>
    <th>CODIGO</th>
    <th>COMUNA</th>
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

            self.treeWidgetUsuarios.addTopLevelItems(item_widget)
        else:
            QMessageBox.information(self, "Buscar usuarios", "No se encontraron resultados.      ",
                                    QMessageBox.Ok)

    def limpiarTabla(self):
        self.documento.clear()
        self.treeWidgetUsuarios.clear()

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


# ================================================================

if __name__ == '__main__':

    import sys

    aplicacion = QApplication(sys.argv)

    qt_traductor = QTranslator()
    qt_traductor.load("qtbase_" + QLocale.system().name(),
                       QLibraryInfo.location(QLibraryInfo.TranslationsPath))
    aplicacion.installTranslator(qt_traductor)

    fuente = QFont()
    fuente.setPointSize(10)
    fuente.setFamily("Bahnschrift Light")

    aplicacion.setFont(fuente)

    ventana = visualizarImprimirExportar()
    ventana.show()

    sys.exit(aplicacion.exec_())
