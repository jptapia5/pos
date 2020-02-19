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

class usuarios(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("gui\login.ui", self)
        self.setWindowTitle("Listado de Usuarios del Sistema") #Título
        self.statusBar().showMessage("Lista de los Usuarios disponibles en el Sistema.")
        self.listar()
        self.habilitarBotones()
        self.btnRefrescar.clicked.connect(self.listar)
        self.btnAgregar.clicked.connect(self.agregar)
        self.btnEliminar.clicked.connect(self.eliminar)
        self.btnModificar.clicked.connect(self.modificar)
        self.btnGuardar.clicked.connect(self.guardar)
        self.btnCancelar.clicked.connect(self.salir)
        self.btnSalir.clicked.connect(self.salir)
        self.btnRefrescar.clicked.connect(self.listar)
        self.btnBuscar.clicked.connect(self.buscar)
        self.tablaListaUsuarios.verticalHeader().setVisible(False)    # Ocultar encabezado vertical
        self.tablaListaUsuarios.setDragDropOverwriteMode(False)    # Deshabilitar el comportamiento de arrastrar y soltar
        self.tablaListaUsuarios.horizontalHeader().setHighlightSections(False)    # Deshabilitar resaltado del texto del encabezado al seleccionar una fila
        self.tablaListaUsuarios.setSortingEnabled(True) # Habilita orden descendente o ascendente


    def habilitarBotones(self):
        self.btnRefrescar.setEnabled(True)
        self.btnAgregar.setEnabled(True)
        self.btnEliminar.setEnabled(True)
        self.btnModificar.setEnabled(True)
        self.btnSalir.setEnabled(True)
        self.btnGuardar.setEnabled(False)
        self.btnCancelar.setEnabled(False)

    def deshabilitarBotones(self):
        self.btnRefrescar.setEnabled(False)
        self.btnAgregar.setEnabled(False)
        self.btnEliminar.setEnabled(False)
        self.btnModificar.setEnabled(False)
        self.btnSalir.setEnabled(False)
        self.btnGuardar.setEnabled(True)
        self.btnCancelar.setEnabled(True)

    def buscar(self):
        busqueda = self.txtBuscar.text()
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        cursor = conn.cursor()
        if busqueda == "":
            QMessageBox.warning(self, 'Información', "No ha aplicado ningun criterio de búsqueda",QMessageBox.Ok)
        else:
            if self.filtroDescripcion.isChecked():
                self.tablaListaUsuarios.setRowCount(0)
                self.tablaListaUsuarios.clearContents()
                sql = "SELECT * FROM usuarios WHERE nombreUsuario LIKE '%" + busqueda + "%' OR apellidoPaterno LIKE '%" + busqueda + "%' OR apellidoMaterno LIKE '%" + busqueda + "%'"
                print(sql)
                cursor.execute(sql)
                self.habilitarBotones()
                self.tablaListaUsuarios.setEditTriggers(QAbstractItemView.NoEditTriggers)
                self.tablaListaUsuarios.setDragDropOverwriteMode(False)
                consultas = cursor.fetchall()
                row = 0
                for consulta in consultas:
                         self.tablaListaUsuarios.insertRow(row)
                         codigo = QTableWidgetItem(str(consulta[0]))
                         descripcion = QTableWidgetItem(str(consulta[1]))
                         categoria = QTableWidgetItem(str(consulta[2]))
                         stock = QTableWidgetItem(str(consulta[3]))
                         stockCritico = QTableWidgetItem(str(consulta[4]))
                         stockMaximo = QTableWidgetItem(str(consulta[5]))
                         self.tablaListaUsuarios.setItem(row, 0, codigo)
                         self.tablaListaUsuarios.setItem(row, 1, descripcion)
                         self.tablaListaUsuarios.setItem(row, 2, categoria)
                         self.tablaListaUsuarios.setItem(row, 3, stock)
                         self.tablaListaUsuarios.setItem(row, 4, stockCritico)
                         self.tablaListaUsuarios.setItem(row, 5, stockMaximo)
                         row = row + 1
            if self.filtroCodigo.isChecked():
                self.tablaListaUsuarios.setRowCount(0)
                self.tablaListaUsuarios.clearContents()
                #print(busqueda)
                sql = ("SELECT * FROM usuarios WHERE idUsuario LIKE '%" + busqueda + "%'")
                #print(sql)
                cursor.execute(sql)
                self.habilitarBotones()
                self.tablaListaUsuarios.setEditTriggers(QAbstractItemView.NoEditTriggers)
                self.tablaListaUsuarios.setDragDropOverwriteMode(False)
                consultas = cursor.fetchall()
                row = 0
                for consulta in consultas:
                        self.tablaListaUsuarios.insertRow(row)
                        idUsuario = QTableWidgetItem(str(consulta[0]))
                        nombreUsuario = QTableWidgetItem(consulta[1])
                        apellidoPaterno = QTableWidgetItem(consulta[2])
                        apellidoMaterno = QTableWidgetItem(consulta[3])
                        fono = QTableWidgetItem(str(consulta[4]))
                        correo = QTableWidgetItem(consulta[5])
                        self.tablaListaUsuarios.setItem(row, 0, idUsuario)
                        self.tablaListaUsuarios.setItem(row, 1, nombreUsuario)
                        self.tablaListaUsuarios.setItem(row, 2, apellidoPaterno)
                        self.tablaListaUsuarios.setItem(row, 3, apellidoMaterno)
                        self.tablaListaUsuarios.setItem(row, 4, fono)
                        self.tablaListaUsuarios.setItem(row, 5, correo)
                        row = row + 1
            conn.commit()
            conn.close()

    def listar(self):
         conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
         cursor = conn.cursor()
         cursor.execute ("SELECT * FROM usuarios")
         #self.habilitarBotones()
         self.tablaListaUsuarios.clearContents()
         self.tablaListaUsuarios.horizontalHeader().setStretchLastSection(True)
         self.tablaListaUsuarios.setSelectionBehavior(QAbstractItemView.SelectRows)
         self.tablaListaUsuarios.setEditTriggers(QAbstractItemView.NoEditTriggers)
         self.tablaListaUsuarios.setSelectionBehavior(QAbstractItemView.SelectRows)
         # Establecer el número de columnas
         self.tablaListaUsuarios.setColumnCount(5)
         # Establecer el número de filas
         self.tablaListaUsuarios.setRowCount(0)
         # Ocultar encabezado vertical
         self.tablaListaUsuarios.verticalHeader().setVisible(False)
         # Deshabilitar el comportamiento de arrastrar y soltar
         self.tablaListaUsuarios.setDragDropOverwriteMode(False)
         # Deshabilitar resaltado del texto del encabezado al seleccionar una fila
         self.tablaListaUsuarios.horizontalHeader().setHighlightSections(False)
         columnas = ('Identificador', 'Nombre', 'Apellido Paterno', 'Apellido Materno', 'Fono')
         self.tablaListaUsuarios.setHorizontalHeaderLabels(columnas)
         for indice, ancho in enumerate((150, 250, 250, 250, 90), start=0):
             self.tablaListaUsuarios.setColumnWidth(indice, ancho)
         #deshabilita la edición de la tabla
         self.tablaListaUsuarios.setEditTriggers(QAbstractItemView.NoEditTriggers)
         # Deshabilitar el comportamiento de arrastrar y soltar
         self.tablaListaUsuarios.setDragDropOverwriteMode(False)
         consultas = cursor.fetchall()
         #print(consultas)
         row = 0
         for consulta in consultas:
             #print (consulta)
             self.tablaListaUsuarios.insertRow(row)
             idUsuario = QTableWidgetItem(str(consulta[0]))
             nombreUsuario = QTableWidgetItem(consulta[1])
             apellidoPaterno = QTableWidgetItem(consulta[2])
             apellidoMaterno = QTableWidgetItem(consulta[3])
             fono = QTableWidgetItem(str(consulta[4]))
             self.tablaListaUsuarios.setItem(row, 0, idUsuario)
             self.tablaListaUsuarios.setItem(row, 1, nombreUsuario)
             self.tablaListaUsuarios.setItem(row, 2, apellidoPaterno)
             self.tablaListaUsuarios.setItem(row, 3, apellidoMaterno)
             self.tablaListaUsuarios.setItem(row, 4, fono)
             row = row + 1
         conn.commit()
         conn.close()

    def agregar(self):
         print("agregar productos")
         self.close()
         process1 = subprocess.run(['python','mantUsuarios.py'])

    def eliminar(self):
        filaSeleccionada = self.tablaListaUsuarios.selectedItems()
        if filaSeleccionada:
            respuesta = QMessageBox.warning(self, 'Advertencia', "Está a punto de eliminar un producto, ¿Está usted seguro de querer hacerlo?",
                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if respuesta == QMessageBox.Yes:
                filas = self.tablaListaUsuarios.selectionModel().selectedRows()
                indice = []
                for i in filas:
                    indice.append(i.row())
                indice.sort(reverse = True)
                for i in indice:
                    id = self.tablaListaUsuarios.item(i, 0).text()
                    self.tablaListaUsuarios.removeRow(i)
                    print(id)
                    sql = ("DELETE FROM usuarios WHERE idUsuario=" + id)
                    print(sql)
                    conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
                    cursor = conn.cursor()
                    cursor.execute(sql)
                    conn.commit()
                    conn.close()
        else:
            QMessageBox.warning(self, 'Información', "Debe seleccionar una fila",
                        QMessageBox.Ok)

    def modificar(self):
        respuesta = QMessageBox.critical(self, 'Advertencia', "¿Está usted seguro de modificar las categorias de productos?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if respuesta == QMessageBox.Yes:
            #habilita la edición de la tabla
                self.tablaListaUsuarios.setEditTriggers(QAbstractItemView.DoubleClicked)
                self.deshabilitarBotones()
                self.tablaListaUsuarios.setSelectionBehavior(QAbstractItemView.SelectItems)
                respuesta = QMessageBox.No
        else :
            #print(" ************ NO MODIFICARÁ NADA *****************")
            self.tablaListaUsuarios.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.habilitarBotones()
        #self.listar()

    def guardar(self):
        print(" ***** PRESIONO GUARDAR **********++++")
        columna = self.tablaListaUsuarios.currentColumn() #la columna que modificará, solo una a la vez
        if columna == 0 :
            QMessageBox.warning(self, 'Error', "No puede modificar el campo id de categoria, intente nuevamenta",	QMessageBox.Ok)
            #print("ENTRO AL IF")
            self.habilitarBotones()
            self.tablaListaUsuarios.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.listar()
        else:
            self.btnGuardar.setEnabled(True)
            #print("ENTRO AL ELSE")
            columna = self.tablaListaUsuarios.currentColumn() #la columna que modificará, solo una a la vez
            fila = self.tablaListaUsuarios.currentRow() #la fila que modificará, solo una a la vez
            #el id de la fila que modificara
            id = self.tablaListaUsuarios.item(fila,0).text() # lee valor de la primera columna, el identificador
            id = str(id)
            valor = self.tablaListaUsuarios.currentItem().text()#el valor que le dio al campo que modificará
            item = ('idUsuario','nombreUsuario', 'apellidoPaterno', 'apellidoMaterno', 'fono', 'correo', 'contrasena')
            campo = item[columna]
            #print(campo)
            '''===================================== SOLO ME MODIFICA UN CAMPO POR VEZ ========================================   '''
            sql = ("UPDATE usuarios SET " + campo + " = '" + valor + "' WHERE idUsuario = " + id )
            print(sql)
            conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            conn.close()
            self.listar()

    def dobleClick(self):
       QMessageBox.warning(self, 'DobleClick', "Hizo doble click en un item de la tabla",QMessageBox.Ok)

    def salir(self):
        #print("******** SALIR DEL PROGRAMA ********")
        self.close()

app = QApplication(sys.argv)
qt_traductor = QTranslator()
qt_traductor.load("qtbase_" + QLocale.system().name(),QLibraryInfo.location(QLibraryInfo.TranslationsPath))
app.installTranslator(qt_traductor)
usuarios = usuarios()
usuarios.show()
app.exec_()
