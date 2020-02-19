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
class comunas(QMainWindow):
    #Metodo constructor clase
    def __init__(self):
        #Iniciar el objeto
        QMainWindow.__init__(self)
        self.documento = QTextDocument()
        #Cargar archivo ui en objeto
        uic.loadUi("gui/comunas.ui",self)
        self.statusBar().showMessage("Listado de Comunas")
        self.setWindowTitle("Lista de Comunas")

         # ==================== INICIO BOTONES ================================
        self.btnRefrescar.clicked.connect(self.listarTodo)
        self.btnAgregar.clicked.connect(self.agregar)
        self.btnEliminar.clicked.connect(self.eliminar)
        self.btnModificar.clicked.connect(self.modificar)
        self.btnSalir.clicked.connect(self.salir)
        self.btnBuscar.clicked.connect(self.buscar)
        self.btnVistaPrevia.clicked.connect(self.vistaPrevia)
        self.btnImprimir.clicked.connect(self.Imprimir)
        self.btnExportarPDF.clicked.connect(self.exportarPDF)
         # ==================== FIN BOTONES  ============================================

        # ==================== INICIO WIDGET QTABLEWIDGET ===============================
        self.listaComunas.setColumnCount(2) #MODIFICAR TENGO QUE CONSULTAR OTRAS TABLAS
        self.listaComunas.verticalHeader().setVisible(False)    # Ocultar encabezado vertical
        self.listaComunas.setDragDropOverwriteMode(False)    # Deshabilitar el comportamiento de arrastrar y soltar
        self.listaComunas.horizontalHeader().setHighlightSections(False)    # Deshabilitar resaltado del texto del encabezado al seleccionar una fila
        self.listaComunas.setSortingEnabled(True) # Habilita orden descendente o ascendente
        columnas = ('Codigo', 'Comuna')
        self.listaComunas.setHorizontalHeaderLabels(columnas)
        self.listaComunas.itemSelectionChanged.connect(self.seleccionItem)
        # =================== FIN WIDGET QTABLEWIDGET =====================================

        # =================== INICIO EVENTOS  =====================================
        #self.listaComunas.itemDoubleClicked.connect(self.dobleClick)
        self.listaComunas.itemSelectionChanged.connect(self.seleccionItem)
        # =================== FIN EVENTOS  =======================================

        # =================== INICIO WIDGET QTREEWIDGET =====================================
        self.treeWidgetComunas.setFont(QFont(self.treeWidgetComunas.font().family(), 10, False))
        self.treeWidgetComunas.setRootIsDecorated(False)
        self.treeWidgetComunas.setHeaderLabels(("Codigo", "Comuna" ))
        self.model = self.treeWidgetComunas.model()
        for indice, ancho in enumerate((110, 150, 150, 160), start=0):
            self.model.setHeaderData(indice, Qt.Horizontal, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.treeWidgetComunas.setColumnWidth(indice, ancho)
        self.treeWidgetComunas.setAlternatingRowColors(True)
        # =================== FIN WIDGET QTREEWIDGET =======================================
        self.listarTodo()

    # =================== INICIO MÉTODOS ===================================================
    def seleccionItem(self):
        indice =  self.listaComunas.currentRow()
        seleccionados = self.listaComunas.selectedIndexes()
        self.statusBar().showMessage('Barra de estado : ' + str(indice))

    def dobleClick(self):
        QMessageBox.warning(self, 'DobleClick', "Hizo doble click en un item de la tabla",QMessageBox.Ok)

    #Deshabilita botones guardar cancelar
    def habilitarBotones(self):
        self.btnRefrescar.setEnabled(True)
        self.btnAgregar.setEnabled(True)
        self.btnEliminar.setEnabled(True)
        self.btnModificar.setEnabled(True)
        self.btnSalir.setEnabled(True)
        self.btnGuardar.setEnabled(False)
        self.btnCancelar.setEnabled(False)
    #Habilita botones guardar cancelar
    def deshabilitarBotones(self):
        self.btnRefrescar.setEnabled(False)
        self.btnAgregar.setEnabled(False)
        self.btnEliminar.setEnabled(False)
        self.btnModificar.setEnabled(False)
        self.btnSalir.setEnabled(False)
        self.btnGuardar.setEnabled(True)
        self.btnCancelar.setEnabled(True)

    def listarTodo(self):
        # ==================== ESTABLECER EL NUMERO DE FILAS ====================
        self.listaComunas.setRowCount(0)
        self.listaComunas.clearContents()
        self.exportar()
        #self.listaComunas.itemDoubleClicked.connect(self. dobleClick)
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        cursor = conn.cursor()
        cursor.execute ("SELECT * FROM comunas")
        self.habilitarBotones()
        self.listaComunas.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listaComunas.setDragDropOverwriteMode(False)
        consultas = cursor.fetchall()
        row = 0
        for consulta in consultas:
                 self.listaComunas.insertRow(row)
                 codigo = QTableWidgetItem(str(consulta[0]))
                 descripcion = QTableWidgetItem(str(consulta[1]))
                 self.listaComunas.setItem(row, 0, codigo)
                 self.listaComunas.setItem(row, 1, descripcion)
                 row = row + 1
        conn.commit()
        conn.close()

    def buscar(self):
        busqueda = str(self.txtBuscar.text())
        
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        cursor = conn.cursor()
        if busqueda == "" and busqueda.isdigit():
            QMessageBox.warning(self, 'Error', "Ingrese un nombre de comuna válido",QMessageBox.Ok)
        else:
            self.listaComunas.setRowCount(0)
            self.listaComunas.clearContents()
            sql = "SELECT * FROM comunas WHERE nombreComuna LIKE '%" + busqueda + "%'"
            print(sql)
            cursor.execute(sql)
            
            self.habilitarBotones()
            self.listaComunas.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.listaComunas.setDragDropOverwriteMode(False)
            consultas = cursor.fetchall()
            
            row = 0
            for consulta in consultas:
                     self.listaComunas.insertRow(row)
                     codigo = QTableWidgetItem(str(consulta[0]))
                     comuna = QTableWidgetItem(str(consulta[1]))
                     self.listaComunas.setItem(row, 0, codigo)
                     self.listaComunas.setItem(row, 1, comuna)
                     row = row + 1

            #aqui llena el QTREEWIDGET
            cursor.execute(sql)
            datosDB = cursor.fetchall()
            if datosDB:
                    self.documento.clear()
                    self.treeWidgetComunas.clear()
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
        <h3>LISTADO DE COMUNAS<br/></h3>
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

                    self.treeWidgetComunas.addTopLevelItems(item_widget)
            else:
                    QMessageBox.information(self, "Buscar Comunas", "No se encontraron resultados.      ",
                                            QMessageBox.Ok)
        conn.close()    



    def agregar(self):
        print("Agregar elemento")
        self.close()
        process1 = subprocess.run(['python','mantComunas.py'])

    def eliminar(self):
        filaSeleccionada = self.listaComunas.selectedItems()
        if filaSeleccionada:
            respuesta = QMessageBox.warning(self, 'Advertencia', "Está a punto de eliminar una comuna, ¿Está usted seguro de querer hacerlo?",
                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if respuesta == QMessageBox.Yes:
                filas = self.listaComunas.selectionModel().selectedRows()
                indice = []
                for i in filas:
                    indice.append(i.row())
                indice.sort(reverse = True)
                for i in indice:
                    id = self.listaComunas.item(i, 0).text()
                    self.listaComunas.removeRow(i)
                    print(id)
                    sql = ("DELETE FROM comunas WHERE idComuna=" + id)
                    print(sql)
                    conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
                    cursor = conn.cursor()
                    cursor.execute(sql)
                    conn.commit()
                    conn.close()
        else:
            QMessageBox.warning(self, 'Información', "Debe seleccionar una fila",
                        QMessageBox.Ok)

    def modificar(self,conn):
        respuesta = QMessageBox.critical(self, 'Advertencia', "¿Está usted seguro de modificar el producto seleccionado?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if respuesta == QMessageBox.Yes:
            #habilita la edición de la tabla
                self.listaComunas.setEditTriggers(QAbstractItemView.DoubleClicked)
                self.deshabilitarBotones()
                self.btnGuardar.clicked.connect(self.guardar)
                self.btnCancelar.clicked.connect(self.listarTodo)
        else :
            #print(" ************ NO MODIFICARÁ NADA *****************")
            self.listaComunas.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def guardar(self):
        print(" ***** GUARDARA LOS REGISTROS **********++++")
        fila = self.listaComunas.currentRow() #la fila que modificará, solo una a la vez
        columna = self.listaComunas.currentColumn() #la columna que modificará, solo una a la vez
        id = self.listaComunas.item(fila, 0).text() #el id de la fila que modificará
        valor = self.listaComunas.currentItem().text() #el valor que le dio al campo que modificará
        #si la columna es la del id, prohibe modificarla ya que es la primary key
        if columna == 2 :
            valor = str(valor)
            valor = (" ' " + valor +" ' ")
            print(valor)
        #    QMessageBox.warning(self, 'Error', "No puede modificar el campo id del producto, intente nuevamenta",
        #                 QMessageBox.Ok)
            #DESDE AQUI EL PROCESO PARA UPDATE LA BASE DE DATOS
        item = ['idComuna', 'nombreComuna']
        campo = item[columna]
        print(campo)
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        cursor = conn.cursor()
        sql = ("UPDATE comunas SET " + campo + " = '" + valor + "' WHERE idComuna = " + id)
        print(sql)
        cursor.execute(sql)
        conn.commit()
        conn.close()
        #SOLUCION PARCHE
        self.close()
        process1 = subprocess.run(['python','comunas.py'])

    def salir(self):
        #print("******** SALIR DEL PROGRAMA ********")
        self.close()

        # ================================== IMPRIMIR O EXPORTAR REPORTES ===============================================
    def exportar(self):
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        cursor = conn.cursor()
        #cursor.execute("SELECT idUsuario, nombreUsuario, apellidoPaterno, apellidoMaterno, fono, correo, contrasena FROM usuario")
        cursor.execute("SELECT * FROM comunas")
        datosDB = cursor.fetchall()
        conn.close()
        if datosDB:
            self.documento.clear()
            self.treeWidgetComunas.clear()
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
<h3>LISTADO DE COMUNAS<br/></h3>
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

            self.treeWidgetComunas.addTopLevelItems(item_widget)
        else:
            QMessageBox.information(self, "Buscar Comunas", "No se encontraron resultados.      ",
                                    QMessageBox.Ok)

    def limpiarTabla(self):
        self.documento.clear()
        self.treeWidgetComunas.clear()

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
            nombreArchivo, _ = QFileDialog.getSaveFileName(self, "Exportar a PDF", "Listado de Comunas",
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


app = QApplication(sys.argv)        #inicia aplicacion
qt_traductor = QTranslator() # traduccion de QMessageBox
qt_traductor.load("qtbase_" + QLocale.system().name(),QLibraryInfo.location(QLibraryInfo.TranslationsPath))
app.installTranslator(qt_traductor)
#fuente = QFont()
#fuente.setPointSize(10)
#fuente.setFamily("Bahnschrift Light")
#app.setFont(fuente)
comunas = comunas()                   #Crear objeto de clase ventana
comunas.show()                       #Mostrar la ventana
app.exec_()                         #Ejecutar la aplicacion
