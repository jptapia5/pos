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


#clase heredada de QMainWindow (Constructor Ventana)
class proveedores(QMainWindow):
#Metodo constructor clase
        def __init__(self):
            #Iniciar el objeto
            QMainWindow.__init__(self)
            #Cargar archivo ui en objeto
            uic.loadUi("gui/proveedores.ui",self)
            self.statusBar().showMessage("Muestra el listado de los proveedores registrado en el sistema")
            # ==================================== EVENTOS ============================================
            self.btnRefrescar.clicked.connect(self.listarTodo)
            self.btnRefrescar.setShortcut("F5")    # Establece atajo con teclado
            self.btnAgregar.clicked.connect(self.agregar)
            self.btnAgregar.setShortcut("Ins")    # Establece atajo con teclado
            self.btnEliminar.clicked.connect(self.eliminar)
            self.btnEliminar.setShortcut("Del")    # Establece atajo con teclado
            self.btnModificar.clicked.connect(self.modificar)
            self.btnCancelar.clicked.connect(self.listarTodo)
            self.btnSalir.clicked.connect(self.salir)
            self.btnSalir.setShortcut("Esc")    # Establece atajo con teclado
            self.btnBuscar.clicked.connect(self.buscar)
            self.btnBuscar.setShortcut("Return")    # Establece atajo con teclado
            # ==================================== TABLET QTWIDGETS ============================================
            self.contruirTabla()
            self.listarTodo()

        def contruirTabla(self):
                # ==================== CONSTRUCCION DE LA TABLAS ================================
                self.listaProveedores.setColumnCount(7) 
                self.listaProveedores.setDragDropOverwriteMode(False)    # Deshabilitar el comportamiento de arrastrar y soltar
                self.listaProveedores.setSortingEnabled(False) # deshabilita orden descendente o ascendente
                self.listaProveedores.setSelectionBehavior(QAbstractItemView.SelectRows) #Selecciona la fila completa
                self.listaProveedores.setSelectionMode(QAbstractItemView.SingleSelection) # Selecciona una fila a la vez
                self.listaProveedores.verticalHeader().setVisible(False)
                self.listaProveedores.setDragDropOverwriteMode(False)    # Deshabilitar el comportamiento de arrastrar y soltar
                self.listaProveedores.horizontalHeader().setHighlightSections(False)    # Deshabilitar resaltado del texto del encabezado al seleccionar una fila
                self.listaProveedores.setSortingEnabled(False) # deshabilita orden descendente o ascendente
                self.listaProveedores.setAlternatingRowColors(True) #alterna colores entre filas
                #MODIFICAR HAY QUE CONSULTAR OTRAS TABLAS
                columnas = ('Codigo','Proveedor', 'Contacto', 'Fono', 'email','Comuna', 'Direccion')
                self.listaProveedores.setHorizontalHeaderLabels(columnas)
                for indice, ancho in enumerate((50, 220, 250, 100, 228, 110, 280), start=0):
                    self.listaProveedores.setColumnWidth(indice, ancho)

        def habilitarBotones(self):
            self.btnRefrescar.setEnabled(True)
            self.btnAgregar.setEnabled(True)
            self.btnEliminar.setEnabled(True)
            self.btnModificar.setEnabled(True)
            self.btnSalir.setEnabled(True)
            self.btnCancelar.setEnabled(False)

        def deshabilitarBotones(self):
            self.btnRefrescar.setEnabled(False)
            self.btnAgregar.setEnabled(False)
            self.btnEliminar.setEnabled(False)
            self.btnModificar.setEnabled(False)
            self.btnSalir.setEnabled(False)
            self.btnCancelar.setEnabled(True)

        def buscar(self):
            busqueda = self.txtBuscar.text()
            conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
            cursor = conn.cursor()
            if busqueda == "":
                QMessageBox.warning(self, 'Información', "No ha aplicado ningun criterio de búsqueda",QMessageBox.Ok)
            else:
                if self.filtroDescripcion.isChecked():
                    self.listaProveedores.setRowCount(0)
                    self.listaProveedores.clearContents()
                    sql = "SELECT * FROM proveedores WHERE nombreProveedor LIKE '%" + busqueda + "%' OR contacto LIKE '%" + busqueda + "%'"
                    #print(sql)
                    cursor.execute(sql)
                    self.habilitarBotones()
                    self.listaProveedores.setEditTriggers(QAbstractItemView.NoEditTriggers)
                    self.listaProveedores.setDragDropOverwriteMode(False)
                    consultas = cursor.fetchall()
                    row = 0
                    for consulta in consultas:
                        self.listaProveedores.insertRow(row)
                        idProveedor = QTableWidgetItem(str(consulta[0]))
                        proveedor = QTableWidgetItem(str(consulta[1]))
                        contacto = QTableWidgetItem(str(consulta[2]))
                        fono = QTableWidgetItem(str(consulta[3]))
                        email = QTableWidgetItem(str(consulta[4]))
                        comuna = consulta[5]
                        direccion = QTableWidgetItem(str(consulta[6]))
                        sql = "SELECT nombreComuna FROM comunas WHERE idComuna = " + str(comuna)
                        cursor.execute(sql)
                        consulta = cursor.fetchone()
                        comuna = QTableWidgetItem(str(consulta[0]))
                        self.listaProveedores.setItem(row, 0, idProveedor)
                        self.listaProveedores.setItem(row, 1, proveedor)
                        self.listaProveedores.setItem(row, 2, contacto)
                        self.listaProveedores.setItem(row, 3, fono)
                        self.listaProveedores.setItem(row, 4, email)
                        self.listaProveedores.setItem(row, 5, comuna)
                        self.listaProveedores.setItem(row, 6, direccion)
                        row = row + 1

                if self.filtroCodigo.isChecked():
                    if busqueda.isdigit():
                        self.listaProveedores.setRowCount(0)
                        self.listaProveedores.clearContents()
                        #print(busqueda)
                        sql = "SELECT * FROM proveedores WHERE idProveedor = " + str(busqueda)
                        #print(sql)
                        cursor.execute(sql)
                        consultas = cursor.fetchall()
                        row = 0
                        for consulta in consultas:
                            self.listaProveedores.insertRow(row)
                            idProveedor = QTableWidgetItem(str(consulta[0]))
                            proveedor = QTableWidgetItem(str(consulta[1]))
                            contacto = QTableWidgetItem(str(consulta[2]))
                            fono = QTableWidgetItem(str(consulta[3]))
                            email = QTableWidgetItem(str(consulta[4]))
                            comuna = consulta[5]
                            direccion = QTableWidgetItem(str(consulta[6]))
                            sql = "SELECT nombreComuna FROM comunas WHERE idComuna = " + str(comuna)
                            cursor.execute(sql)
                            consulta = cursor.fetchone()
                            comuna = QTableWidgetItem(str(consulta[0]))
                            self.listaProveedores.setItem(row, 0, idProveedor)
                            self.listaProveedores.setItem(row, 1, proveedor)
                            self.listaProveedores.setItem(row, 2, contacto)
                            self.listaProveedores.setItem(row, 3, fono)
                            self.listaProveedores.setItem(row, 4, email)
                            self.listaProveedores.setItem(row, 5, comuna)
                            self.listaProveedores.setItem(row, 6, direccion)
                            row = row + 1
                    else:
                        self.listaProveedores.setRowCount(0)
                        self.listaProveedores.clearContents()
                        print("no es digito")
            conn.close()

            
        def listarTodo(self):
            self.listaProveedores.setRowCount(0)
            self.listaProveedores.clearContents()
            self.txtBuscar.setText("")
            self.habilitarBotones()
            self.listaProveedores.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.listaProveedores.setDragDropOverwriteMode(False)
            conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
            cursor = conn.cursor()
            sql = "SELECT * FROM proveedores"
            #print(sql)
            cursor.execute(sql)
            self.habilitarBotones()
            consultas = cursor.fetchall()
            row = 0
            for consulta in consultas:
                        self.listaProveedores.insertRow(row)
                        idProveedor = QTableWidgetItem(str(consulta[0]))
                        proveedor = QTableWidgetItem(str(consulta[1]))
                        contacto = QTableWidgetItem(str(consulta[2]))
                        fono = QTableWidgetItem(str(consulta[3]))
                        email = QTableWidgetItem(str(consulta[4]))
                        comuna = consulta[5]
                        direccion = QTableWidgetItem(str(consulta[6]))
                        sql = "SELECT nombreComuna FROM comunas WHERE idComuna = " + str(comuna)
                        cursor.execute(sql)
                        consulta = cursor.fetchone()
                        comuna = QTableWidgetItem(str(consulta[0]))
                        self.listaProveedores.setItem(row, 0, idProveedor)
                        self.listaProveedores.setItem(row, 1, proveedor)
                        self.listaProveedores.setItem(row, 2, contacto)
                        self.listaProveedores.setItem(row, 3, fono)
                        self.listaProveedores.setItem(row, 4, email)
                        self.listaProveedores.setItem(row, 5, comuna)
                        self.listaProveedores.setItem(row, 6, direccion)
                        row = row + 1
            conn.close()

        def agregar(self):
             #print("agregar productos")
             #self.close()
             self.close()
             process1 = subprocess.run(['python','mantproveedores.py'])


        def eliminar(self):
            filaSeleccionada = self.listaProveedores.selectedItems()
            if filaSeleccionada:
                respuesta = QMessageBox.warning(self, 'Advertencia', "Está a punto de eliminar un producto, ¿Está usted seguro de querer hacerlo?",
                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if respuesta == QMessageBox.Yes:
                    filas = self.listaProveedores.selectionModel().selectedRows()
                    indice = []
                    for i in filas:
                        indice.append(i.row())
                    indice.sort(reverse = True)
                    for i in indice:
                        id = self.listaProveedores.item(i, 0).text()
                        self.listaProveedores.removeRow(i)
                        print(id)
                        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
                        cursor = conn.cursor()
                        sql = ("SELECT * FROM ventas WHERE idProveedor = " + id)
                        cursor.execute(sql)
                        valida = cursor.fetchall()
                        if valida:
                            QMessageBox.warning(self, 'ERROR', "No puede eliminar cliente, tiene deudas o compras realizadas", QMessageBox.Ok)
                            self.listar()
                        else:
                            sql = ("DELETE FROM proveedores WHERE idProveedor = " + id)
                            print(sql)
                            #conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
                            #cursor = conn.cursor()
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
                filaSeleccionada = self.listaProveedores.selectedItems()
                if filaSeleccionada:
                    indice = self.listaProveedores.currentRow() #la fila que modificará, solo una a la vez
                else:
                    indice = 0
                    #habilita la edición de la tabla
                    self.deshabilitarBotones()
                    #self.listaProductos.setEnabled(False)
                    self.listaProveedores.setEditTriggers(QAbstractItemView.DoubleClicked)
                    #self.listaProductos.setEditTriggers(QAbstractItemView.AllEditTriggers)
                    #self.listaProductos.setEditTriggers(QAbstractItemView.NoEditTriggers)
                    #self.listaProductos.setEditTriggers(QAbstractItemView.CurrentChanged)
                    #self.listaProductos.setEditTriggers(QAbstractItemView.SelectedClicked)  
                    self.listaProveedores.setSelectionBehavior(QAbstractItemView.SelectItems)              
                    #self.btnGuardar.clicked.connect(self.guardar)
                    idProveedor = str(self.listaProveedores.item(indice,0).text()) # lee valor de la primera columna, el identificador de la fila que modificara
                    #self.statusBar().showMessage('Barra de estado : ' + str(idProducto) + "")
                    self.listaProveedores.itemChanged.connect(self.guardar)
                    self.btnCancelar.clicked.connect(self.cancelar)

        def guardar(self):
            #print(" ***** PRESIONO GUARDAR **********++++")
            columna = self.listaProveedores.currentColumn() #la columna que modificará, solo una a la vez
            if columna == 0 :
                QMessageBox.warning(self, 'Error', "No puede modificar el campo idProveedor, intente nuevamenta",	QMessageBox.Ok)
                self.cancelar()
            else:
                conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
                cursor = conn.cursor()
                self.btnGuardar.setEnabled(True)
                #print("ENTRO AL ELSE")
                columna = self.listaProveedores.currentColumn() #la columna que modificará, solo una a la vez
                fila = self.listaProveedores.currentRow() #la fila que modificará, solo una a la vez
                #el id de la fila que modificara
                id = self.listaProveedores.item(fila,0).text() # lee valor de la primera columna, el identificador
                id = str(id)
                valor = self.listaProveedores.currentItem().text()#el valor que le dio al campo que modificará
                if columna == 6 :
                    sql = ("SELECT idComuna FROM comunas WHERE nombreComuna = '" + valor + "'")
                    print(sql)
                    cursor.execute(sql)
                    consultaComuna = cursor.fetchone()
                    print(consultaComuna[0])
                    valor = str(consultaComuna[0])
                item = ('idProveedor', 'rutProveedor', 'nombreProveedor', 'contacto', 'fono', 'email', 'idComuna', 'direccion')
                campo = item[columna]
                #print(campo)
                '''===================================== SOLO ME MODIFICA UN CAMPO POR VEZ ========================================   '''
                sql = ("UPDATE proveedores SET " + campo + " = '" + valor + "' WHERE idProveedor = " + id )
                cursor.execute(sql)
                conn.commit()
                conn.close()
                #self.habilitarBotones()
                #SOLUCION PARCHE
                self.close()
                process1 = subprocess.run(['python','proveedores.py'])

        def dobleClick(self):
           QMessageBox.warning(self, 'DobleClick', "Hizo doble click en un item de la tabla",QMessageBox.Ok)


        def cancelar(self):
                self.close() 
                #self.listarTodo()
                process1 = subprocess.run(['python','proveedores.py'])     
        def salir(self):
            #print("******** SALIR DEL PROGRAMA ********")
            self.close()

app = QApplication(sys.argv)
#  ===================================== Traduccion de botones de QMessageBox ============================================
qt_traductor = QTranslator()
qt_traductor.load("qtbase_" + QLocale.system().name(),QLibraryInfo.location(QLibraryInfo.TranslationsPath))
app.installTranslator(qt_traductor)
proveedores = proveedores()
proveedores.show()
app.exec_()
