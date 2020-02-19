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

class clientes(QMainWindow):
    #Metodo constructor clase
    def __init__(self):
        #Iniciar el objeto
        QMainWindow.__init__(self)
        #Cargar archivo ui en objeto
        uic.loadUi("gui/clientes.ui",self)
        self.statusBar().showMessage("Bienvenido")
        # ==================================== EVENTOS ============================================
        self.btnRefrescar.clicked.connect(self.listar)
        self.btnRefrescar.setShortcut("F5")    # Establece atajo con teclado
        self.btnAgregar.clicked.connect(self.agregar)
        self.btnAgregar.setShortcut("Ins")    # Establece atajo con teclado
        self.btnEliminar.clicked.connect(self.eliminar)
        self.btnEliminar.setShortcut("Del")    # Establece atajo con teclado
        self.btnModificar.clicked.connect(self.modificar)
        self.btnGuardar.clicked.connect(self.guardar)
        self.btnCancelar.clicked.connect(self.listar)
        self.btnSalir.clicked.connect(self.salir)
        self.btnSalir.setShortcut("Esc")    # Establece atajo con teclado
        self.btnRefrescar.clicked.connect(self.listar)
        self.btnBuscar.clicked.connect(self.buscar)
        self.btnBuscar.setShortcut("Return")    # Establece atajo con teclado
        # ==================================== TABLET QTWIDGETS ============================================
        self.listaClientes.setSelectionBehavior(QAbstractItemView.SelectRows) #Selecciona la fila completa
        self.listaClientes.setSelectionMode(QAbstractItemView.SingleSelection) # Selecciona una fila a la vez
        self.listaClientes.verticalHeader().setVisible(False)    # Ocultar encabezado vertical
        self.listaClientes.verticalHeader().setVisible(False)
        self.listaClientes.setDragDropOverwriteMode(False)    # Deshabilitar el comportamiento de arrastrar y soltar
        self.listaClientes.horizontalHeader().setHighlightSections(False)    # Deshabilitar resaltado del texto del encabezado al seleccionar una fila
        self.listaClientes.setSortingEnabled(True) # Habilita orden descendente o ascendente
        self.listaClientes.setAlternatingRowColors(True) #alterna colores entre filas
        self.listar()

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
            if self.filtronombre.isChecked():
                self.listaClientes.setRowCount(0)
                self.listaClientes.clearContents()
                sql = "SELECT * FROM clientes WHERE nombreCliente LIKE '%" + busqueda + "%' OR apellidoPaterno LIKE '%" + busqueda + "%' OR apellidoMaterno LIKE '%" + busqueda + "%'"
                #print(sql)
                cursor.execute(sql)
                self.habilitarBotones()
                self.listaClientes.setEditTriggers(QAbstractItemView.NoEditTriggers)
                self.listaClientes.setDragDropOverwriteMode(False)
                consultas = cursor.fetchall()
                row = 0
                for consulta in consultas:
                    #print (consulta)
                    self.listaClientes.insertRow(row)
                    idCliente = QTableWidgetItem(str(consulta[0]))
                    rut = QTableWidgetItem(str(consulta[1]))
                    nombre = QTableWidgetItem(consulta[2])
                    apellidoPaterno = QTableWidgetItem(consulta[3])
                    apellidoMaterno = QTableWidgetItem(consulta[4])
                    direccion = QTableWidgetItem(consulta[5])
                    comuna = consulta[6]
                    fonoFijo = QTableWidgetItem(str(consulta[7]))
                    celular = QTableWidgetItem(str(consulta[8]))
                    deudaTotal = QTableWidgetItem("$ " + str(consulta[9]))
                    deudaMaxima = QTableWidgetItem("$ " + str(consulta[10]))
                    sql = "SELECT nombreComuna FROM comunas WHERE idComuna = " + str(comuna)
                    #print (sql)
                    cursor.execute(sql)
                    consultaComuna = cursor.fetchone()
                    comuna = QTableWidgetItem(consultaComuna[0])
                    self.listaClientes.setItem(row, 0, idCliente)
                    self.listaClientes.setItem(row, 1, rut)
                    self.listaClientes.setItem(row, 2, nombre)
                    self.listaClientes.setItem(row, 3, apellidoPaterno)
                    self.listaClientes.setItem(row, 4, apellidoMaterno)
                    self.listaClientes.setItem(row, 5, direccion)
                    self.listaClientes.setItem(row, 6, comuna)
                    self.listaClientes.setItem(row, 7, fonoFijo)
                    self.listaClientes.setItem(row, 8, celular)
                    self.listaClientes.setItem(row, 9, deudaTotal)
                    self.listaClientes.setItem(row, 10, deudaMaxima)
                    row = row + 1
            if self.filtroRut.isChecked():
                if busqueda.isdigit():
                        self.listaClientes.setRowCount(0)
                        self.listaClientes.clearContents()
                        #print(busqueda)
                        sql = ("SELECT * FROM clientes WHERE idCliente = " + busqueda + " OR rut = " + busqueda)
                        #print(sql)
                        cursor.execute(sql)
                        self.habilitarBotones()
                        self.listaClientes.setEditTriggers(QAbstractItemView.NoEditTriggers)
                        self.listaClientes.setDragDropOverwriteMode(False)
                        consultas = cursor.fetchall()
                        row = 0
                        for consulta in consultas:
                            #print (consulta)
                            self.listaClientes.insertRow(row)
                            idCliente = QTableWidgetItem(str(consulta[0]))
                            rut = QTableWidgetItem(str(consulta[1]))
                            nombre = QTableWidgetItem(consulta[2])
                            apellidoPaterno = QTableWidgetItem(consulta[3])
                            apellidoMaterno = QTableWidgetItem(consulta[4])
                            direccion = QTableWidgetItem(consulta[5])
                            comuna = consulta[6]
                            fonoFijo = QTableWidgetItem(str(consulta[7]))
                            celular = QTableWidgetItem(str(consulta[8]))
                            deudaTotal = QTableWidgetItem("$ " + str(consulta[9]))
                            deudaMaxima = QTableWidgetItem("$ " + str(consulta[10]))
                            sql = "SELECT nombreComuna FROM comunas WHERE idComuna = " + str(comuna)
                            #print (sql)
                            cursor.execute(sql)
                            consultaComuna = cursor.fetchone()
                            comuna = QTableWidgetItem(consultaComuna[0])
                            self.listaClientes.setItem(row, 0, idCliente)
                            self.listaClientes.setItem(row, 1, rut)
                            self.listaClientes.setItem(row, 2, nombre)
                            self.listaClientes.setItem(row, 3, apellidoPaterno)
                            self.listaClientes.setItem(row, 4, apellidoMaterno)
                            self.listaClientes.setItem(row, 5, direccion)
                            self.listaClientes.setItem(row, 6, comuna)
                            self.listaClientes.setItem(row, 7, fonoFijo)
                            self.listaClientes.setItem(row, 8, celular)
                            self.listaClientes.setItem(row, 9, deudaTotal)
                            self.listaClientes.setItem(row, 10, deudaMaxima)
                else:
                        self.listaClientes.setRowCount(0)
                        self.listaClientes.clearContents()
                        print("no es digito")
            conn.close()
            self.txtBuscar.setText("")

    def listar(self):
         conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
         cursor = conn.cursor()
         sql = "SELECT * FROM clientes"
         #print(sql)
         cursor.execute(sql)
         self.habilitarBotones()
         self.listaClientes.clearContents()
         self.listaClientes.horizontalHeader().setStretchLastSection(True)
         # Establece Selecciona filas
         self.listaClientes.setSelectionBehavior(QAbstractItemView.SelectRows)
         # Establece Bloquear modificar items
         self.listaClientes.setEditTriggers(QAbstractItemView.NoEditTriggers)
         # Establecer el número de columnas
         self.listaClientes.setColumnCount(11)
         # Establecer el número de filas
         self.listaClientes.setRowCount(0)
         # Ocultar encabezado vertical
         self.listaClientes.verticalHeader().setVisible(False)
         # Deshabilitar el comportamiento de arrastrar y soltar
         self.listaClientes.setDragDropOverwriteMode(False)
         # Deshabilitar resaltado del texto del encabezado al seleccionar una fila
         self.listaClientes.horizontalHeader().setHighlightSections(False)
         columnas = ('ID','RUT', 'NOMBRE', 'APELLIDO PATERNO', 'APELLIDO MATERNO', 'DIRECCIÓN','COMUNA','FONO FIJO','CELULAR','DEUDA','CUPO')
         self.listaClientes.setHorizontalHeaderLabels(columnas)
         for indice, ancho in enumerate((15, 70, 150, 150, 150, 370, 90, 80, 80, 80, 80), start=0):
             self.listaClientes.setColumnWidth(indice, ancho)
         #deshabilita la edición de la tabla
         self.listaClientes.setEditTriggers(QAbstractItemView.NoEditTriggers)
         # Deshabilitar el comportamiento de arrastrar y soltar
         self.listaClientes.setDragDropOverwriteMode(False)
         consultas = cursor.fetchall()
         #print(consultas)
         row = 0
         for consulta in consultas:
             #print (consulta)
             self.listaClientes.insertRow(row)
             idCliente = QTableWidgetItem(str(consulta[0]))
             rut = QTableWidgetItem(str(consulta[1]))
             nombre = QTableWidgetItem(consulta[2])
             apellidoPaterno = QTableWidgetItem(consulta[3])
             apellidoMaterno = QTableWidgetItem(consulta[4])
             direccion = QTableWidgetItem(consulta[5])
             comuna = consulta[6]
             fonoFijo = QTableWidgetItem(str(consulta[7]))
             celular = QTableWidgetItem(str(consulta[8]))
             deudaTotal = QTableWidgetItem("$ " + str(consulta[9]))
             deudaMaxima = QTableWidgetItem("$ " + str(consulta[10]))
             sql = "SELECT nombreComuna FROM comunas WHERE idComuna = '" + str(comuna) + "'"
             #print (sql)
             cursor.execute(sql)
             consultaComuna = cursor.fetchone()
             comuna = QTableWidgetItem(consultaComuna[0])
             self.listaClientes.setItem(row, 0, idCliente)
             self.listaClientes.setItem(row, 1, rut)
             self.listaClientes.setItem(row, 2, nombre)
             self.listaClientes.setItem(row, 3, apellidoPaterno)
             self.listaClientes.setItem(row, 4, apellidoMaterno)
             self.listaClientes.setItem(row, 5, direccion)
             self.listaClientes.setItem(row, 6, comuna)
             self.listaClientes.setItem(row, 7, fonoFijo)
             self.listaClientes.setItem(row, 8, celular)
             self.listaClientes.setItem(row, 9, deudaTotal)
             self.listaClientes.setItem(row, 10, deudaMaxima)
             row = row + 1
         conn.commit()
         conn.close()

    def agregar(self):
         #print("agregar productos")
         self.close()
         process1 = subprocess.run(['python','mantClientes.py'])

    def eliminar(self):
        filaSeleccionada = self.listaClientes.selectedItems()
        if filaSeleccionada:
            respuesta = QMessageBox.warning(self, 'Advertencia', "Está a punto de eliminar un producto, ¿Está usted seguro de querer hacerlo?",
                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if respuesta == QMessageBox.Yes:
                filas = self.listaClientes.selectionModel().selectedRows()
                indice = []
                for i in filas:
                    indice.append(i.row())
                indice.sort(reverse = True)
                for i in indice:
                    id = self.listaClientes.item(i, 0).text()
                    self.listaClientes.removeRow(i)
                    print(id)
                    conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
                    cursor = conn.cursor()
                    sql = ("SELECT totalDeuda FROM clientes WHERE idCliente = " + id)
                    cursor.execute(sql)
                    pendientePago = cursor.fetchone()
                    pendientePago = int(pendientePago)
                    if valida > 0 :
                        QMessageBox.warning(self, 'ERROR', "No puede eliminar cliente, tiene deudas por compras pendientes de pago", QMessageBox.Ok)
                        self.listar()
                    else:
                        sql = "UPDATE clientes SET idCliente = '0' WHERE idCliente = " + id
                        sql = "DELETE FROM clientes WHERE idCliente = " + id
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
            #habilita la edición de la tabla
                self.listaClientes.setEditTriggers(QAbstractItemView.DoubleClicked)
                self.deshabilitarBotones()
                self.listaClientes.setSelectionBehavior(QAbstractItemView.SelectItems)
                respuesta = QMessageBox.No
                self.btnGuardar.setShortcut("Return")    # Establece atajo con teclado
                self.btnBuscar.setShortcut("Ctrl+F")    # Establece atajo con teclado
        else :
            #print(" ************ NO MODIFICARÁ NADA *****************")
            self.listaClientes.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.habilitarBotones()
        #self.listar()

    def guardar(self):
        columna = self.listaClientes.currentColumn() #la columna que modificará, solo una a la vez
        if (columna == 0 or columna == 1 ):
            QMessageBox.warning(self, 'Error', "No puede modificar el campo ID o RUT",	QMessageBox.Ok)
            self.listar()
            self.listaClientes.setEditTriggers(QAbstractItemView.NoEditTriggers)
        else:
            conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
            cursor = conn.cursor()
            self.btnGuardar.setEnabled(True)
            #print("ENTRO AL ELSE")
            columna = self.listaClientes.currentColumn() #la columna que modificará, solo una a la vez
            fila = self.listaClientes.currentRow() #la fila que modificará, solo una a la vez
            #el id de la fila que modificara
            id = self.listaClientes.item(fila,0).text() # lee valor de la primera columna, el identificador
            id = str(id)
            valor = self.listaClientes.currentItem().text()#el valor que le dio al campo que modificará
            print(columna)
            print(valor)
            if columna == 6 :
                sql = ("SELECT idComuna FROM comunas WHERE nombreComuna = '" + valor + "'")
                print(sql)
                cursor.execute(sql)
                consultaComuna = cursor.fetchone()
                if consultaComuna:
                                print(consultaComuna[0])
                                valor = str(consultaComuna[0])
                                item = ('idCliente','rut','nombreCliente','apellidoPaterno','apellidoMaterno','direccion','comuna','fonoFijo','celular','deudaMaxima')
                                campo = item[columna]
                                #print(campo)
                                '''===================================== SOLO ME MODIFICA UN CAMPO POR VEZ ========================================   '''
                                sql = ("UPDATE clientes SET " + campo + " = '" + valor + "' WHERE idCliente = " + id )
                                print(sql)
                                cursor.execute(sql)
                                conn.commit()
                                conn.close()
                                #self.habilitarBotones()
                                self.listar()
                else:
                    QMessageBox.warning(self, 'Error', "La comuna ingresada no se encuentra en los registros de comunas",	QMessageBox.Ok)
            else:
                    item = ('idCliente','rut','nombreCliente','apellidoPaterno','apellidoMaterno','direccion','comuna','fonoFijo','celular','deudaMaxima')
                    campo = item[columna]
                    #print(campo)
                    '''===================================== SOLO ME MODIFICA UN CAMPO POR VEZ ========================================   '''
                    sql = ("UPDATE clientes SET " + campo + " = '" + valor + "' WHERE idCliente = " + id )
                    print(sql)
                    cursor.execute(sql)
                    conn.commit()
                    conn.close()
            self.habilitarBotones()

   
    def salir(self):
        #print("******** SALIR DEL PROGRAMA ********")
        self.close()

app = QApplication(sys.argv)
clientes = clientes()
clientes.show()
app.exec_()
