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
class medioPago(QMainWindow):
    #Metodo constructor clase
    def __init__(self):
        #Iniciar el objeto
        QMainWindow.__init__(self)
        #Cargar archivo ui en objeto
        uic.loadUi("gui/medioPago.ui",self)
        self.statusBar().showMessage("Muestra el Listado de los medios de pago ingresados en sistema.")

        self.btnRefrescar.clicked.connect(self.listarTodo)
        self.btnAgregar.clicked.connect(self.agregar)
        self.btnEliminar.clicked.connect(self.eliminar)
        self.btnModificar.clicked.connect(self.modificar)
        self.btnSalir.clicked.connect(self.salir)
        self.btnBuscar.clicked.connect(self.buscar)
        # ==================== CONSTRUCCION DE LA TABLAS ================================
        self.listaMedioPago.setColumnCount(2) #MODIFICAR TENGO QUE CONSULTAR OTRAS TABLAS
        self.listaMedioPago.verticalHeader().setVisible(False)    # Ocultar encabezado vertical
        self.listaMedioPago.setDragDropOverwriteMode(False)    # Deshabilitar el comportamiento de arrastrar y soltar
        self.listaMedioPago.horizontalHeader().setHighlightSections(False)    # Deshabilitar resaltado del texto del encabezado al seleccionar una fila
        self.listaMedioPago.setSortingEnabled(True) # Habilita orden descendente o ascendente
        #MODIFICAR HAY QUE CONSULTAR OTRAS TABLAS
        columnas = ('Codigo', 'Medio de Pago')
        #columnas = ('Id', 'Descripcion', 'Categoria', 'Precio Costo', 'Precio Venta', 'Stock', 'Stock Critico', 'Stock Maximo', 'Proveedor')
        self.listaMedioPago.setHorizontalHeaderLabels(columnas)
        self.listarTodo()
        self.listaMedioPago.itemSelectionChanged.connect(self.seleccionItem)
        self.listaMedioPago.itemDoubleClicked.connect(self.dobleClick)

    def seleccionItem(self):
        indice =  self.listaMedioPago.currentRow()
        #seleccionados = self.listaMedioPago.selectedIndexes()
        id = self.listaMedioPago.item(indice,0)
        #self.statusBar().showMessage('Barra de estado : indice = ' + str(indice) + " - id = " + str(id))
        #self.statusBar().showMessage('Barra de estado : indice = ' + str(indice))

    def dobleClick(self):
       #QMessageBox.warning(self, 'DobleClick', "Hizo doble click en un item de la tabla",QMessageBox.Ok)
       fila = self.listaMedioPago.currentRow() #la fila que modificará, solo una a la vez
       columna = self.listaMedioPago.currentColumn() #la columna que modificará, solo una a la vez
       id = self.listaMedioPago.item(fila, 0).text() #el id de la fila que modificará
       print(id)

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
        self.listaMedioPago.setRowCount(0)
        self.listaMedioPago.clearContents()
        #self.listaMedioPago.itemDoubleClicked.connect(self. dobleClick)
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        cursor = conn.cursor()
        cursor.execute ("SELECT * FROM medio_de_pago")
        self.habilitarBotones()
        self.listaMedioPago.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listaMedioPago.setDragDropOverwriteMode(False)
        consultas = cursor.fetchall()
        row = 0
        for consulta in consultas:
                 self.listaMedioPago.insertRow(row)
                 codigo = QTableWidgetItem(str(consulta[0]))
                 descripcion = QTableWidgetItem(str(consulta[1]))
                 self.listaMedioPago.setItem(row, 0, codigo)
                 self.listaMedioPago.setItem(row, 1, descripcion)
                 row = row + 1
        conn.commit()
        conn.close()

    def buscar(self):
        busqueda = str(self.txtBuscar.text())
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        cursor = conn.cursor()
        if busqueda == "":
            QMessageBox.warning(self, 'Información', "No ha aplicado ningun criterio de búsqueda",QMessageBox.Ok)
        else:
            if self.filtroDescripcion.isChecked():
                self.listaMedioPago.setRowCount(0)
                self.listaMedioPago.clearContents()
                sql = "SELECT * FROM medio_de_pago WHERE nombreMedioPago LIKE '%" + busqueda + "%'"
                print(sql)
                cursor.execute(sql)
                self.habilitarBotones()
                self.listaMedioPago.setEditTriggers(QAbstractItemView.NoEditTriggers)
                self.listaMedioPago.setDragDropOverwriteMode(False)
                consultas = cursor.fetchall()
                row = 0
                for consulta in consultas:
                         self.listaMedioPago.insertRow(row)
                         codigo = QTableWidgetItem(str(consulta[0]))
                         descripcion = QTableWidgetItem(str(consulta[1]))
                         self.listaMedioPago.setItem(row, 0, codigo)
                         self.listaMedioPago.setItem(row, 1, descripcion)

                         row = row + 1
            if self.filtroCodigo.isChecked():
                self.listaMedioPago.setRowCount(0)
                self.listaMedioPago.clearContents()
                sql = "SELECT * FROM medio_de_pago WHERE idMedioPago LIKE '%" + busqueda + "%'"
                cursor.execute(sql)
                self.habilitarBotones()
                self.listaMedioPago.setEditTriggers(QAbstractItemView.NoEditTriggers)
                self.listaMedioPago.setDragDropOverwriteMode(False)
                consultas = cursor.fetchall()
                row = 0
                for consulta in consultas:
                         self.listaMedioPago.insertRow(row)
                         codigo = QTableWidgetItem(str(consulta[0]))
                         descripcion = QTableWidgetItem(str(consulta[1]))
                         self.listaMedioPago.setItem(row, 0, codigo)
                         self.listaMedioPago.setItem(row, 1, descripcion)
                         row = row + 1
            conn.commit()
            conn.close()

    def agregar(self):
        print("agregar productos")
        self.close()
        process1 = subprocess.run(['python','mantMedioPago.py'])

    def eliminar(self):
        filaSeleccionada = self.listaMedioPago.selectedItems()
        if filaSeleccionada:
            respuesta = QMessageBox.warning(self, 'Advertencia', "Está a punto de eliminar un producto, ¿Está usted seguro de querer hacerlo?",
                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if respuesta == QMessageBox.Yes:
                filas = self.listaMedioPago.selectionModel().selectedRows()
                indice = []
                for i in filas:
                    indice.append(i.row())
                indice.sort(reverse = True)
                for i in indice:
                    id = self.listaMedioPago.item(i, 0).text()
                    self.listaMedioPago.removeRow(i)
                    print(id)
                    sql = ("DELETE FROM medio_de_pago WHERE idMedioPago=" + id)
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
                self.listaMedioPago.setEditTriggers(QAbstractItemView.DoubleClicked)
                self.deshabilitarBotones()
                self.btnGuardar.clicked.connect(self.guardar)
                self.btnCancelar.clicked.connect(self.listarTodo)
        else :
            #print(" ************ NO MODIFICARÁ NADA *****************")
            self.listaMedioPago.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def guardar(self):
        print(" ***** PRESIONO GUARDAR **********++++")
        columna = self.listaMedioPago.currentColumn() #la columna que modificará, solo una a la vez
        fila = self.listaMedioPago.currentRow() #la fila que modificará, solo una a la vez
        #el id de la fila que modificara
        id = self.listaMedioPago.item(fila,0)# lee valor de la primera columna, el identificador
        id = id.text()
        if columna == 0 :
            QMessageBox.warning(self, 'Error', "No puede modificar el campo id de categoria, intente nuevamenta",	QMessageBox.Ok)
            #print("ENTRO AL IF")
            self.listaMedioPago.setEditTriggers(QAbstractItemView.NoEditTriggers)
        else:
            self.btnGuardar.setEnabled(True)
            #print("ENTRO AL ELSE")
            #columna = self.listaMedioPago.currentColumn() #la columna que modificará, solo una a la vez
            #fila = self.listaMedioPago.currentRow() #la fila que modificará, solo una a la vez
            #el id de la fila que modificara
            #id = self.listaMedioPago.item(fila,0).text() # lee valor de la primera columna, el identificador
            valor = self.listaMedioPago.currentItem().text()#el valor que le dio al campo que modificará
            item = ['idMedioPago', 'nombreMedioPago']
            campo = item[columna]
            #print(campo)
            conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
            cursor = conn.cursor()
            sql = ("UPDATE medio_de_pago SET " + campo + " = '" + valor + "' WHERE idMedioPago = " + id)
            print(sql)
            cursor.execute(sql)
            conn.commit()
            conn.close()
            self.listaMedioPago.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.habilitarBotones()


    def salir(self):
        #print("******** SALIR DEL PROGRAMA ********")
        self.close()




app = QApplication(sys.argv)        #inicia aplicacion
#  ===================================== Traduccion de botones de QMessageBox ============================================
qt_traductor = QTranslator()
qt_traductor.load("qtbase_" + QLocale.system().name(),QLibraryInfo.location(QLibraryInfo.TranslationsPath))
app.installTranslator(qt_traductor)
medioPago = medioPago()                   #Crear objeto de clase ventana
medioPago.show()                       #Mostrar la ventana
app.exec_()                         #Ejecutar la aplicacion
