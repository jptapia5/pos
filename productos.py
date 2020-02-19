import sys
import os
import subprocess
import pymysql
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5 import QtGui
import time
import datetime
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog

class productos(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("gui/productos.ui", self)
        self.setWindowTitle("Lista Productos") #Título
        self.statusBar().showMessage("Muestra el listado de los productos registrado en el sistema")
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        #Indica a que método ejecutar al precionar alguno de los botones
        self.btnMostrarTodo.clicked.connect(self.listarTodo)
        self.btnAgregar.clicked.connect(self.agregar)
        self.btnEliminar.clicked.connect(self.eliminar)
        self.btnModificar.clicked.connect(self.modificar)
        self.btnSalir.clicked.connect(self.salir)
        self.btnMostrarCat.clicked.connect(self.listarPorCategoria)
        self.btnBuscar.clicked.connect(self.buscar)

        # ==================== CONSTRUCCION DE LA TABLAS ================================
        self.contruirTabla()
        self.listarTodo()
        self.listaProductos.itemSelectionChanged.connect(self.seleccionItem)
        self.listaProductos.itemDoubleClicked.connect(self.dobleClick)
       
    def contruirTabla(self):
            # ==================== CONSTRUCCION DE LA TABLAS ================================
            self.listaProductos.setColumnCount(9) 
            self.listaProductos.verticalHeader().setVisible(False)    # Ocultar encabezado vertical
            self.listaProductos.setDragDropOverwriteMode(False)    # Deshabilitar el comportamiento de arrastrar y soltar
            self.listaProductos.horizontalHeader().setHighlightSections(False)    # Deshabilitar resaltado del texto del encabezado al seleccionar una fila
            self.listaProductos.setSortingEnabled(False) # Habilita orden descendente o ascendente
            #MODIFICAR HAY QUE CONSULTAR OTRAS TABLAS
            columnas = ('CODIGO','DESCRIPCION','STOCK','STOCK MIN','STOCK MÁX','PRECIO COSTO','PRECIO VENTA','CATEGORIA','PROVEEDOR')
            self.listaProductos.setHorizontalHeaderLabels(columnas)
            for indice, ancho in enumerate((150, 500, 50, 70, 75, 100, 100, 150,150), start=0):
                self.listaProductos.setColumnWidth(indice, ancho)

    def seleccionItem(self):
        indice =  self.listaProductos.currentRow()
        seleccionados = self.listaProductos.selectedIndexes()
        self.statusBar().showMessage('Barra de estado : ' + str(indice) + "")

    def dobleClick(self):
       #QMessageBox.warning(self, 'DobleClick', "Hizo doble click en un item de la tabla",QMessageBox.Ok)
       #AL HACER DOBLECLICK RESCATA EL VALOR DEL ID PRODUCTO
       fila = self.listaProductos.currentRow() #la fila que modificará, solo una a la vez
       columna = self.listaProductos.currentColumn() #la columna que modificará, solo una a la vez
       id = self.listaProductos.item(fila, 0).text() #el id de la fila que modificará
       #print(id)

    #Deshabilita botones guardar cancelar
    def habilitarBotones(self):
        self.btnMostrarTodo.setEnabled(True)
        self.btnAgregar.setEnabled(True)
        self.btnEliminar.setEnabled(True)
        self.btnModificar.setEnabled(True)
        self.btnSalir.setEnabled(True)
        self.btnGuardar.setEnabled(False)
        self.btnCancelar.setEnabled(False)

    #Habilita botones guardar cancelar
    def deshabilitarBotones(self):
        self.btnMostrarTodo.setEnabled(False)
        self.btnAgregar.setEnabled(False)
        self.btnEliminar.setEnabled(False)
        self.btnModificar.setEnabled(False)
        self.btnSalir.setEnabled(False)
        self.btnGuardar.setEnabled(True)
        self.btnCancelar.setEnabled(True)

    def listarTodo(self):
        # ==================== ESTABLECER EL NUMERO DE FILAS ====================
        
        self.listaProductos.setRowCount(0)
        self.listaProductos.clearContents()
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        cursor = conn.cursor()
        sql = "SELECT productos.idProducto, \
                        productos.nombreProducto,  \
                        productos.stock,  \
                        productos.stockCritico,  \
                        productos.stockMaximo,  \
                        precio_producto.precioCosto,  \
                        precio_producto.precioVenta, \
                        productos.idCategoriaProducto  \
                FROM productos, precio_producto   \
                WHERE productos.idProducto = precio_producto.idProducto  \
	                AND precio_producto.fecha = (SELECT MAX(FECHA) FROM mydb.precio_producto  \
		   			                    		    WHERE productos.idProducto = precio_producto.idProducto );"
        cursor.execute(sql)
        conn.close()
        consultas = cursor.fetchall()
        row = 0
        for consulta in consultas:
                self.listaProductos.insertRow(row)
                codigo = QTableWidgetItem(str(consulta[0]))
                idProducto = consulta[0]
                descripcion = QTableWidgetItem(str(consulta[1]))                
                stock = QTableWidgetItem(str(consulta[2]))
                stockCritico = QTableWidgetItem(str(consulta[3]))
                stockMaximo = QTableWidgetItem(str(consulta[4]))
                precioCosto = QTableWidgetItem("$" + str(consulta[5]))
                precioVenta = QTableWidgetItem("$" + str(consulta[6]))
                categoria = (consulta[7])
                # define el color a destacar  
                colorStock = consulta[2]
                colorStockCritico = consulta[3]
                colorStockMaximo = consulta[4]
                conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
                sql = "SELECT nombreCategoria FROM categoria_producto WHERE idCategoriaProducto = '" + str(categoria) + "'"
                cursor = conn.cursor()
                cursor.execute(sql)
                consulta = cursor.fetchone()
                conn.close()
                categoria = QTableWidgetItem(str(consulta[0]))
                #consulta por nombre proveedor del producto
                sql = "SELECT proveedores.nombreProveedor \
                      FROM proveedores \
                      WHERE idProveedor = (SELECT idProveedor FROM producto_proveedor WHERE idProducto = '" + str(idProducto) + "');"
                conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
                cursor = conn.cursor()
                cursor.execute(sql)                           
                consulta = cursor.fetchone() 
                conn.close()
                if (consulta == None):
                    proveedor = QTableWidgetItem(" ")
                else:
                     proveedor = QTableWidgetItem(str(consulta[0]))
                self.listaProductos.setItem(row, 0, codigo)
                self.listaProductos.setItem(row, 1, descripcion)
                self.listaProductos.setItem(row, 2, stock)
                self.listaProductos.setItem(row, 3, stockCritico)
                self.listaProductos.setItem(row, 4, stockMaximo)
                self.listaProductos.setItem(row, 5, precioCosto)
                self.listaProductos.setItem(row, 6, precioVenta)
                self.listaProductos.setItem(row, 7, categoria)
                self.listaProductos.setItem(row, 8, proveedor)
                
                if (colorStock <= colorStockCritico) :  #AMARILLO SI ALCANZÓ O BAJO EL STOCK CRITICÓ
                            self.listaProductos.item(row,0).setBackground(QtGui.QColor(255,255,0))
                            self.listaProductos.item(row,1).setBackground(QtGui.QColor(255,255,0))
                            self.listaProductos.item(row,2).setBackground(QtGui.QColor(255,255,0))
                            self.listaProductos.item(row,3).setBackground(QtGui.QColor(255,255,0))
                            self.listaProductos.item(row,4).setBackground(QtGui.QColor(255,255,0))
                            self.listaProductos.item(row,5).setBackground(QtGui.QColor(255,255,0))
                            self.listaProductos.item(row,6).setBackground(QtGui.QColor(255,255,0))
                            self.listaProductos.item(row,7).setBackground(QtGui.QColor(255,255,0))
                            self.listaProductos.item(row,8).setBackground(QtGui.QColor(255,255,0))

                if (colorStock < 2):   #ROJO SI le digo que si es CERO
                            self.listaProductos.item(row,0).setBackground(QtGui.QColor(255,0,0))
                            self.listaProductos.item(row,1).setBackground(QtGui.QColor(255,0,0))
                            self.listaProductos.item(row,2).setBackground(QtGui.QColor(255,0,0))
                            self.listaProductos.item(row,3).setBackground(QtGui.QColor(255,0,0))
                            self.listaProductos.item(row,4).setBackground(QtGui.QColor(255,0,0))
                            self.listaProductos.item(row,5).setBackground(QtGui.QColor(255,0,0))
                            self.listaProductos.item(row,6).setBackground(QtGui.QColor(255,0,0))
                            self.listaProductos.item(row,7).setBackground(QtGui.QColor(255,0,0))
                            self.listaProductos.item(row,8).setBackground(QtGui.QColor(255,0,0))
                if (colorStock > colorStockMaximo):  # VERDE si el stock es igual o mayor al maximo stock
                            self.listaProductos.item(row,0).setBackground(QtGui.QColor(0,255,0))
                            self.listaProductos.item(row,1).setBackground(QtGui.QColor(0,255,0))
                            self.listaProductos.item(row,2).setBackground(QtGui.QColor(0,255,0))
                            self.listaProductos.item(row,3).setBackground(QtGui.QColor(0,255,0))
                            self.listaProductos.item(row,4).setBackground(QtGui.QColor(0,255,0))
                            self.listaProductos.item(row,5).setBackground(QtGui.QColor(0,255,0))
                            self.listaProductos.item(row,6).setBackground(QtGui.QColor(0,255,0))
                            self.listaProductos.item(row,7).setBackground(QtGui.QColor(0,255,0))
                            self.listaProductos.item(row,8).setBackground(QtGui.QColor(0,255,0))
              
                row = row + 1
        self.listaCategoria.clear()
        sql=("SELECT nombreCategoria FROM categoria_producto")
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        cursor = conn.cursor()
        cursor.execute (sql)
        lista = cursor.fetchall()
        i = 0
        while i < len(lista):
                 categoria = (str(lista[i]))
                 categoria = categoria[2:]
                 fin = categoria.find("''")
                 categoria = categoria[:fin-2]
                 self.listaCategoria.addItem(categoria)
                 self.listaCategoria.setCurrentIndex(-1)
                 i = i + 1
        conn.commit()
        conn.close()
        self.habilitarBotones()
        self.listaProductos.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listaProductos.setSelectionBehavior(QAbstractItemView.SelectRows)  
        self.listaProductos.setDragDropOverwriteMode(False)

    def buscar(self):
        busqueda = str(self.txtBuscar.text())
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        cursor = conn.cursor()
        if busqueda == "":
            QMessageBox.warning(self, 'Información', "No ha aplicado ningun criterio de búsqueda",QMessageBox.Ok)
        else:
            if self.filtroDescripcion.isChecked():
                self.contruirTabla()
                self.listaProductos.setRowCount(0)
                self.listaProductos.clearContents()
                sql = "SELECT productos.idProducto, \
                        productos.nombreProducto,  \
                        productos.stock,  \
                        productos.stockCritico,  \
                        productos.stockMaximo,  \
                        precio_producto.precioCosto,  \
                        precio_producto.precioVenta, \
                        productos.idCategoriaProducto  \
                FROM productos, precio_producto  \
                WHERE productos.nombreProducto LIKE '%" + busqueda + "%'\
                    AND productos.idProducto = precio_producto.idProducto  \
	                AND precio_producto.fecha = (SELECT MAX(FECHA) FROM mydb.precio_producto  \
		   			                    		    WHERE productos.idProducto = precio_producto.idProducto );"
                #print(sql)
                cursor.execute(sql)
                self.habilitarBotones()
                self.listaProductos.setEditTriggers(QAbstractItemView.NoEditTriggers)
                self.listaProductos.setDragDropOverwriteMode(False)
                consultas = cursor.fetchall()
                row = 0
                #print(consultas)
                if not consultas:
                        QMessageBox.information(self, 'Información', "No se encontraron resultados",QMessageBox.Ok)
                else :                
                        for consulta in consultas:
                                self.listaProductos.insertRow(row)
                                codigo = QTableWidgetItem(str(consulta[0]))
                                idProducto = consulta[0]
                                descripcion = QTableWidgetItem(str(consulta[1]))                
                                stock = QTableWidgetItem(str(consulta[2]))
                                stockCritico = QTableWidgetItem(str(consulta[3]))
                                stockMaximo = QTableWidgetItem(str(consulta[4]))
                                precioCosto = QTableWidgetItem("$" + str(consulta[5]))
                                precioVenta = QTableWidgetItem("$" + str(consulta[6]))
                                categoria = (consulta[7])
                                # define el color a destacar
                                colorStock = consulta[2]
                                colorStockCritico = consulta[3]
                                colorStockMaximo = consulta[4]
                                sql = "SELECT nombreCategoria FROM categoria_producto WHERE idCategoriaProducto = '" + str(categoria) + "'"
                                cursor.execute(sql)
                                consulta = cursor.fetchone()
                                categoria = QTableWidgetItem(str(consulta[0]))
                                #consulta por nombre proveedor del producto
                                sql = "SELECT proveedores.nombreProveedor \
                                            FROM proveedores \
                                            WHERE idProveedor = (SELECT idProveedor FROM producto_proveedor WHERE idProducto = '" + str(idProducto) + "');"
                                #print(sql)                            
                                cursor.execute(sql)                           
                                consulta = cursor.fetchone() 
                                #print(consulta)
                                if (consulta == None):
                                    proveedor = QTableWidgetItem(" ")
                                else:
                                    proveedor = QTableWidgetItem(str(consulta[0]))                        
                                self.listaProductos.setItem(row, 0, codigo)
                                self.listaProductos.setItem(row, 1, descripcion)
                                self.listaProductos.setItem(row, 2, stock)
                                self.listaProductos.setItem(row, 3, stockCritico)
                                self.listaProductos.setItem(row, 4, stockMaximo)
                                self.listaProductos.setItem(row, 5, precioCosto)
                                self.listaProductos.setItem(row, 6, precioVenta)
                                self.listaProductos.setItem(row, 7, categoria)
                                self.listaProductos.setItem(row, 8, proveedor)
                                if (colorStock <= colorStockCritico) :  #AMARILLO SI ALCANZÓ O BAJO EL STOCK CRITICÓ
                                            self.listaProductos.item(row,0).setBackground(QtGui.QColor(255,255,0))
                                            self.listaProductos.item(row,1).setBackground(QtGui.QColor(255,255,0))
                                            self.listaProductos.item(row,2).setBackground(QtGui.QColor(255,255,0))
                                            self.listaProductos.item(row,3).setBackground(QtGui.QColor(255,255,0))
                                            self.listaProductos.item(row,4).setBackground(QtGui.QColor(255,255,0))
                                            self.listaProductos.item(row,5).setBackground(QtGui.QColor(255,255,0))
                                            self.listaProductos.item(row,6).setBackground(QtGui.QColor(255,255,0))
                                            self.listaProductos.item(row,7).setBackground(QtGui.QColor(255,255,0))
                                            self.listaProductos.item(row,8).setBackground(QtGui.QColor(255,255,0))
                                if (colorStock < 2):   #ROJO SI le digo que si es CERO
                                            self.listaProductos.item(row,0).setBackground(QtGui.QColor(255,0,0))
                                            self.listaProductos.item(row,1).setBackground(QtGui.QColor(255,0,0))
                                            self.listaProductos.item(row,2).setBackground(QtGui.QColor(255,0,0))
                                            self.listaProductos.item(row,3).setBackground(QtGui.QColor(255,0,0))
                                            self.listaProductos.item(row,4).setBackground(QtGui.QColor(255,0,0))
                                            self.listaProductos.item(row,5).setBackground(QtGui.QColor(255,0,0))
                                            self.listaProductos.item(row,6).setBackground(QtGui.QColor(255,0,0))
                                            self.listaProductos.item(row,7).setBackground(QtGui.QColor(255,0,0))
                                            self.listaProductos.item(row,8).setBackground(QtGui.QColor(255,0,0))
                                        
                                if (colorStock > colorStockMaximo):  # VERDE si el stock es igual o mayor al maximo stock
                                            self.listaProductos.item(row,0).setBackground(QtGui.QColor(0,255,0))
                                            self.listaProductos.item(row,1).setBackground(QtGui.QColor(0,255,0))
                                            self.listaProductos.item(row,2).setBackground(QtGui.QColor(0,255,0))
                                            self.listaProductos.item(row,3).setBackground(QtGui.QColor(0,255,0))
                                            self.listaProductos.item(row,4).setBackground(QtGui.QColor(0,255,0))
                                            self.listaProductos.item(row,5).setBackground(QtGui.QColor(0,255,0))
                                            self.listaProductos.item(row,6).setBackground(QtGui.QColor(0,255,0))
                                            self.listaProductos.item(row,7).setBackground(QtGui.QColor(0,255,0))
                                            self.listaProductos.item(row,8).setBackground(QtGui.QColor(0,255,0))
                                row = row + 1
            if self.filtroCodigo.isChecked():
                if busqueda.isdigit():
                    #print("es digito")
                    self.listaProductos.setRowCount(0)
                    self.listaProductos.clearContents()
                    self.contruirTabla()
                    sql = "SELECT productos.idProducto, \
                                            productos.nombreProducto,  \
                                            productos.stock,  \
                                            productos.stockCritico,  \
                                            productos.stockMaximo,  \
                                            precio_producto.precioCosto,  \
                                            precio_producto.precioVenta, \
                                            productos.idCategoriaProducto  \
                                    FROM productos, precio_producto   \
                                    WHERE productos.idProducto =" + busqueda + " \
                                        AND productos.idProducto = precio_producto.idProducto  \
                                        AND precio_producto.fecha = (SELECT MAX(FECHA) FROM mydb.precio_producto  \
                                                                        WHERE productos.idProducto = precio_producto.idProducto );"
                    cursor.execute(sql)
                    self.habilitarBotones()
                    self.listaProductos.setEditTriggers(QAbstractItemView.NoEditTriggers)
                    self.listaProductos.setDragDropOverwriteMode(False)
                    consultas = cursor.fetchall()
                    row = 0
                    #print(consultas)
                    if not consultas:
                            QMessageBox.information(self, 'Información', "No se encontraron resultados",QMessageBox.Ok)
                    else :
                            for consulta in consultas:
                                    self.listaProductos.insertRow(row)
                                    codigo = QTableWidgetItem(str(consulta[0]))
                                    idProducto = consulta[0]
                                    descripcion = QTableWidgetItem(str(consulta[1]))                
                                    stock = QTableWidgetItem(str(consulta[2]))
                                    stockCritico = QTableWidgetItem(str(consulta[3]))
                                    stockMaximo = QTableWidgetItem(str(consulta[4]))
                                    precioCosto = QTableWidgetItem("$" + str(consulta[5]))
                                    precioVenta = QTableWidgetItem("$" + str(consulta[6]))
                                    categoria = (consulta[7])
                                    # define el color a destacar
                                    colorStock = consulta[2]
                                    colorStockCritico = consulta[3]
                                    colorStockMaximo = consulta[4]
                                    sql = "SELECT nombreCategoria FROM categoria_producto WHERE idCategoriaProducto = '" + str(categoria) + "'"
                                    cursor.execute(sql)
                                    consulta = cursor.fetchone()
                                    categoria = QTableWidgetItem(str(consulta[0]))
                                    #consulta por nombre proveedor del producto
                                    sql = "SELECT proveedores.nombreProveedor \
                                                FROM proveedores \
                                                WHERE idProveedor = (SELECT idProveedor FROM producto_proveedor WHERE idProducto = '" + str(idProducto) + "');"
                                    #print(sql)                            
                                    cursor.execute(sql)                           
                                    consulta = cursor.fetchone() 
                                    #print(consulta)
                                    if (consulta == None):
                                        proveedor = QTableWidgetItem(" ")
                                    else:
                                        proveedor = QTableWidgetItem(str(consulta[0]))       
                                    self.listaProductos.setItem(row, 0, codigo)
                                    self.listaProductos.setItem(row, 1, descripcion)
                                    self.listaProductos.setItem(row, 2, stock)
                                    self.listaProductos.setItem(row, 3, stockCritico)
                                    self.listaProductos.setItem(row, 4, stockMaximo)
                                    self.listaProductos.setItem(row, 5, precioCosto)
                                    self.listaProductos.setItem(row, 6, precioVenta)
                                    self.listaProductos.setItem(row, 7, categoria)
                                    self.listaProductos.setItem(row, 8, proveedor)

                                    if (colorStock <= colorStockCritico) :  #AMARILLO SI ALCANZÓ O BAJO EL STOCK CRITICÓ
                                                self.listaProductos.item(row,0).setBackground(QtGui.QColor(255,255,0))
                                                self.listaProductos.item(row,1).setBackground(QtGui.QColor(255,255,0))
                                                self.listaProductos.item(row,2).setBackground(QtGui.QColor(255,255,0))
                                                self.listaProductos.item(row,3).setBackground(QtGui.QColor(255,255,0))
                                                self.listaProductos.item(row,4).setBackground(QtGui.QColor(255,255,0))
                                                self.listaProductos.item(row,5).setBackground(QtGui.QColor(255,255,0))
                                                self.listaProductos.item(row,6).setBackground(QtGui.QColor(255,255,0))
                                                self.listaProductos.item(row,7).setBackground(QtGui.QColor(255,255,0))
                                                self.listaProductos.item(row,8).setBackground(QtGui.QColor(255,255,0))
                                    if (colorStock < 2):   #ROJO SI le digo que si es CERO
                                                self.listaProductos.item(row,0).setBackground(QtGui.QColor(255,0,0))
                                                self.listaProductos.item(row,1).setBackground(QtGui.QColor(255,0,0))
                                                self.listaProductos.item(row,2).setBackground(QtGui.QColor(255,0,0))
                                                self.listaProductos.item(row,3).setBackground(QtGui.QColor(255,0,0))
                                                self.listaProductos.item(row,4).setBackground(QtGui.QColor(255,0,0))
                                                self.listaProductos.item(row,5).setBackground(QtGui.QColor(255,0,0))
                                                self.listaProductos.item(row,6).setBackground(QtGui.QColor(255,0,0))
                                                self.listaProductos.item(row,7).setBackground(QtGui.QColor(255,0,0))
                                                self.listaProductos.item(row,8).setBackground(QtGui.QColor(255,0,0))
                                    if (colorStock > colorStockMaximo):  # VERDE si el stock es igual o mayor al maximo stock
                                                self.listaProductos.item(row,0).setBackground(QtGui.QColor(0,255,0))
                                                self.listaProductos.item(row,1).setBackground(QtGui.QColor(0,255,0))
                                                self.listaProductos.item(row,2).setBackground(QtGui.QColor(0,255,0))
                                                self.listaProductos.item(row,3).setBackground(QtGui.QColor(0,255,0))
                                                self.listaProductos.item(row,4).setBackground(QtGui.QColor(0,255,0))
                                                self.listaProductos.item(row,5).setBackground(QtGui.QColor(0,255,0))
                                                self.listaProductos.item(row,6).setBackground(QtGui.QColor(0,255,0))
                                                self.listaProductos.item(row,7).setBackground(QtGui.QColor(0,255,0))                            
                                                self.listaProductos.item(row,8).setBackground(QtGui.QColor(0,255,0))      
                                    row = row + 1
                else:
                    self.listaProductos.setRowCount(0)
                    self.listaProductos.clearContents()
                    #print("no es digito")
            conn.close()
            self.txtBuscar.setText("")

    def listarPorCategoria(self):
            conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
            cursor = conn.cursor()
            indexCategoria = self.listaCategoria.currentIndex()
            if (indexCategoria != -1):
                    self.contruirTabla()
                    itemCategoria = self.listaCategoria.currentText()
                    itemCategoria = str(itemCategoria)
                    cursor.execute("SELECT idCategoriaProducto FROM categoria_producto WHERE nombreCategoria = %s", itemCategoria)
                    consultas = cursor.fetchone()
                    idCategoriaProducto = consultas[0]
                    consultas = cursor.fetchall()
                    self.listaProductos.setRowCount(0)
                    self.listaProductos.clearContents()
                  
                    sql = "SELECT productos.idProducto, \
                        productos.nombreProducto,  \
                        productos.stock,  \
                        productos.stockCritico,  \
                        productos.stockMaximo,  \
                        precio_producto.precioCosto,  \
                        precio_producto.precioVenta, \
                        productos.idCategoriaProducto  \
                FROM productos, precio_producto  \
                WHERE productos.idProducto = precio_producto.idProducto  \
                    AND productos.idCategoriaProducto = + '" + str(idCategoriaProducto) + "' \
	                AND precio_producto.fecha = (SELECT MAX(FECHA) FROM mydb.precio_producto  \
		   			                    		    WHERE productos.idProducto = precio_producto.idProducto );"

                    cursor.execute(sql)
                    consultas = cursor.fetchall()
                    row = 0
                    for consulta in consultas:
                                self.listaProductos.insertRow(row)
                                codigo = QTableWidgetItem(str(consulta[0]))
                                idProducto = consulta[0]
                                descripcion = QTableWidgetItem(str(consulta[1]))                
                                stock = QTableWidgetItem(str(consulta[2]))
                                stockCritico = QTableWidgetItem(str(consulta[3]))
                                stockMaximo = QTableWidgetItem(str(consulta[4]))
                                precioCosto = QTableWidgetItem("$"+str(consulta[5]))
                                precioVenta = QTableWidgetItem("$"+str(consulta[6]))
                                categoria = (consulta[7])
                                     # define el color a destacar
                                colorStock = consulta[2]
                                colorStockCritico = consulta[3]
                                colorStockMaximo = consulta[4]
                                sql = "SELECT nombreCategoria FROM categoria_producto WHERE idCategoriaProducto = '" + str(categoria) + "'"
                                cursor.execute(sql)
                                consulta = cursor.fetchone()
                                categoria = QTableWidgetItem(str(consulta[0]))
                                #consulta por el nombre del proveedor
                                sql = "SELECT proveedores.nombreProveedor \
                                            FROM proveedores \
                                            WHERE idProveedor = (SELECT idProveedor FROM producto_proveedor WHERE idProducto = '" + str(idProducto) + "');"
                                #print(sql)                            
                                cursor.execute(sql)                           
                                consulta = cursor.fetchone() 
                                #print(consulta)
                                if (consulta == None):
                                    proveedor = QTableWidgetItem(" ")
                                else:
                                    proveedor = QTableWidgetItem(str(consulta[0]))      
                                self.listaProductos.setItem(row, 0, codigo)
                                self.listaProductos.setItem(row, 1, descripcion)
                                self.listaProductos.setItem(row, 2, stock)
                                self.listaProductos.setItem(row, 3, stockCritico)
                                self.listaProductos.setItem(row, 4, stockMaximo)
                                self.listaProductos.setItem(row, 5, precioCosto)
                                self.listaProductos.setItem(row, 6, precioVenta)
                                self.listaProductos.setItem(row, 7, categoria)
                                self.listaProductos.setItem(row, 8, proveedor)

                                if (colorStock <= colorStockCritico) :  #AMARILLO SI ALCANZÓ O BAJO EL STOCK CRITICÓ
                                            self.listaProductos.item(row,0).setBackground(QtGui.QColor(255,255,0))
                                            self.listaProductos.item(row,1).setBackground(QtGui.QColor(255,255,0))
                                            self.listaProductos.item(row,2).setBackground(QtGui.QColor(255,255,0))
                                            self.listaProductos.item(row,3).setBackground(QtGui.QColor(255,255,0))
                                            self.listaProductos.item(row,4).setBackground(QtGui.QColor(255,255,0))
                                            self.listaProductos.item(row,5).setBackground(QtGui.QColor(255,255,0))
                                            self.listaProductos.item(row,6).setBackground(QtGui.QColor(255,255,0))
                                            self.listaProductos.item(row,7).setBackground(QtGui.QColor(255,255,0))

                                if (colorStock < 2):   #ROJO SI le digo que si es CERO
                                            self.listaProductos.item(row,0).setBackground(QtGui.QColor(255,0,0))
                                            self.listaProductos.item(row,1).setBackground(QtGui.QColor(255,0,0))
                                            self.listaProductos.item(row,2).setBackground(QtGui.QColor(255,0,0))
                                            self.listaProductos.item(row,3).setBackground(QtGui.QColor(255,0,0))
                                            self.listaProductos.item(row,4).setBackground(QtGui.QColor(255,0,0))
                                            self.listaProductos.item(row,5).setBackground(QtGui.QColor(255,0,0))
                                            self.listaProductos.item(row,6).setBackground(QtGui.QColor(255,0,0))
                                            self.listaProductos.item(row,7).setBackground(QtGui.QColor(255,0,0))
                                
                                if (colorStock > colorStockMaximo):  # VERDE si el stock es igual o mayor al maximo stock
                                            self.listaProductos.item(row,0).setBackground(QtGui.QColor(0,255,0))
                                            self.listaProductos.item(row,1).setBackground(QtGui.QColor(0,255,0))
                                            self.listaProductos.item(row,2).setBackground(QtGui.QColor(0,255,0))
                                            self.listaProductos.item(row,3).setBackground(QtGui.QColor(0,255,0))
                                            self.listaProductos.item(row,4).setBackground(QtGui.QColor(0,255,0))
                                            self.listaProductos.item(row,5).setBackground(QtGui.QColor(0,255,0))
                                            self.listaProductos.item(row,6).setBackground(QtGui.QColor(0,255,0))
                                            self.listaProductos.item(row,7).setBackground(QtGui.QColor(0,255,0))
                                row = row + 1
            else:
                 QMessageBox.warning(self, 'Información', "Debe seleccionar una categoría de productos",
                               QMessageBox.Ok)

    def agregar(self):
        #print("agregar productos")
        self.close()
        process1 = subprocess.run(['python','mantProductos.py'])

    def eliminar(self):
        filaSeleccionada = self.listaProductos.selectedItems()
        if filaSeleccionada:
            respuesta = QMessageBox.critical(self, 'Advertencia', "Está a punto de eliminar un producto, ¿Está usted seguro de querer hacerlo?",
                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if respuesta == QMessageBox.Yes:
                filas = self.listaProductos.selectionModel().selectedRows()
                indice = []
                for i in filas:
                    indice.append(i.row())
                indice.sort(reverse = True)
                for i in indice:
                    id = self.listaProductos.item(i, 0).text()
                    self.listaProductos.removeRow(i)
                    #print(id)
                    conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
                    cursor = conn.cursor()
                    sql = "DELETE dv FROM detalle_venta dv INNER JOIN productos p ON dv.idProducto = p.idProducto WHERE p.idProducto  = " + id + ";"
                    #print(sql)
                    cursor.execute(sql)
                    sql = "DELETE pp FROM precio_producto pp INNER JOIN productos p ON pp.idProducto = p.idProducto WHERE p.idProducto  = " + id + ";"
                    #print(sql)
                    cursor.execute(sql)
                    sql = "DELETE ppr FROM producto_proveedor ppr INNER JOIN productos p ON ppr.idProducto = p.idProducto WHERE p.idProducto  = " + id + ";"
                    cursor.execute(sql)
                    #print(sql)
                    sql = "DELETE FROM productos WHERE idProducto =" + id + ";"
                    #print(sql)
                    cursor.execute(sql)
                    conn.commit()
                    conn.close()
        else:
            QMessageBox.warning(self, 'Información', "Debe seleccionar una fila",
                        QMessageBox.Ok)

    def modificar(self):
                    respuesta = QMessageBox.warning(self, 'Advertencia', "¿Está usted seguro de modificar productos?",
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if respuesta == QMessageBox.Yes:
                            filaSeleccionada = self.listaProductos.selectedItems()
                            if filaSeleccionada:
                                indice = self.listaProductos.currentRow() #la fila que modificará, solo una a la vez
                            else:
                                indice = 0
                            #habilita la edición de la tabla
                            self.deshabilitarBotones()
                            #self.listaProductos.setEnabled(False)
                            self.listaProductos.setEditTriggers(QAbstractItemView.DoubleClicked)
                            #self.listaProductos.setEditTriggers(QAbstractItemView.AllEditTriggers)
                            #self.listaProductos.setEditTriggers(QAbstractItemView.NoEditTriggers)
                            #self.listaProductos.setEditTriggers(QAbstractItemView.CurrentChanged)
                            #self.listaProductos.setEditTriggers(QAbstractItemView.SelectedClicked)  
                            self.listaProductos.setSelectionBehavior(QAbstractItemView.SelectItems)              
                            #self.btnGuardar.clicked.connect(self.guardar)
                            idProducto = str(self.listaProductos.item(indice,0).text()) # lee valor de la primera columna, el identificador de la fila que modificara
                            self.statusBar().showMessage('Barra de estado : ' + str(idProducto) + "")
                            self.listaProductos.itemChanged.connect(self.guardar)
                            self.btnCancelar.clicked.connect(self.cancelar)

    
    def cancelar(self):
        self.close() 
        #self.listarTodo()
        process1 = subprocess.run(['python','productos.py'])           
          
    
    def guardar(self):
                columna = self.listaProductos.currentColumn() #la columna que modificará, solo una a la vez
                fila = self.listaProductos.currentRow() #la fila que modificará, solo una a la vez
                idProducto = str(self.listaProductos.item(fila,0).text()) # lee valor de la primera columna, el identificador de la fila que modificara
                if columna == -1:
                    #print("id columna: " + columna)
                    self.listarTodo()
                elif columna == 0 :
                    #print("id columna: " + str(columna))
                    QMessageBox.critical(self, 'Error', "No puede modificar el campo codigo, intente nuevamenta",	QMessageBox.Ok)
                elif columna == 5 or columna == 6:
                    #print("id columna: " + str(columna))
                    conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
                    sql = "SELECT DATE_FORMAT(NOW(), '%Y-%m-%d');"
                    cursor = conn.cursor()
                    cursor.execute(sql)
                    fecha = cursor.fetchone()
                    fecha = str(fecha[0])
                    precioCosto = str(self.listaProductos.item(fila,5).text())
                    precioC = precioCosto[0:1]
                    if precioC == "$":
                        precioCosto = precioCosto[1:len(precioCosto)]
                    precioVenta = str(self.listaProductos.item(fila,6).text())
                    precioV = precioVenta[0:1]
                    if precioV == "$":
                        precioVenta = precioVenta[1:len(precioVenta)]
                    #print("precio costo:" + precioCosto + " precio venta:" + precioVenta)
                    valor = self.listaProductos.currentItem().text()#el valor que le dio al campo que modificará
                    #print("VALOR QUE SE LE DIO AL CAMPO A MODIFICAR " + valor)
                    cursor = conn.cursor()
                    cursor.execute ("INSERT INTO precio_producto(idProducto,fecha,precioCosto,precioVenta) VALUES (%s,%s,%s,%s)", (idProducto,fecha,precioCosto,precioVenta))
                    consulta = cursor.fetchone()
                    conn.commit()
                    conn.close()
                elif columna == 7:
                    #print("id columna: " + str(columna))
                    #print("debo modificar la categoria de productos")
                    valor = self.listaProductos.currentItem().text()#el valor que le dio al campo que modificará
                    #print(valor)
                    conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
                    cursor = conn.cursor()
                    sql= "SELECT idCategoriaProducto FROM categoria_producto WHERE nombreCategoria = '" + valor + "';"
                    #print(sql)
                    cursor.execute(sql)
                    consulta = cursor.fetchone()
                    if consulta:
                        idCategoria = consulta[0]
                        #print(idCategoria)
                        sql = "UPDATE productos SET idCategoriaProducto = " + str(idCategoria) + " WHERE idProducto = " + str(idProducto)
                        #print(sql)
                        cursor.execute(sql)
                        conn.commit()
                        conn.close()
                    else:
                        QMessageBox.critical(self, 'Error', "La Categoría de productos indicada no está en la base de datos. Indique la categoria correcta",QMessageBox.Ok)
                elif columna == 8:
                    #print("id columna: " + str(columna))
                    #print("debo modificar al proveedor del productos")
                    valor = self.listaProductos.currentItem().text()#el valor que le dio al campo que modificará
                    #print(valor)
                    conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
                    cursor = conn.cursor()
                    sql= "SELECT idProveedor FROM proveedores WHERE nombreProveedor = '" + valor + "';"
                    #print(sql)
                    cursor.execute(sql)
                    consulta = cursor.fetchone()
                    if consulta:
                        idProveedor = consulta[0]
                        #print(idProveedor)
                        sql = "UPDATE producto_proveedor SET idProveedor = " + str(idProveedor) + " WHERE idProducto = " + str(idProducto) 
                        #print(sql)
                        cursor.execute(sql)
                        conn.commit()
                        conn.close()
                    else:
                        QMessageBox.critical(self, 'Error', "El proveedor indicado no está en la base de datos. Indique un proveedor válido",QMessageBox.Ok)
                else:
                    #print("id columna: " + str(columna))
                    fila = self.listaProductos.currentRow() #la fila que modificará, solo una a la vez
                    #el id de la fila que modificara
                    id = self.listaProductos.item(fila,0).text() # lee valor de la primera columna, el identificadors
                    id = str(id)
                    valor = self.listaProductos.currentItem().text()#el valor que le dio al campo que modificará
                    item = ['idProducto', 'nombreProducto','stock','stockCritico','stockMaximo','precioCosto','precioVenta','idCategoriaProducto']
                    campo = item[columna]
                    conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
                    cursor = conn.cursor()
                    sql = ("UPDATE productos SET " + campo + " = '" + valor + "' WHERE idProducto = " + id)
                    #print(sql)
                    cursor.execute(sql)
                    conn.commit()
                    conn.close()

    def salir(self):
        self.close()

app = QApplication(sys.argv)
#  ===================================== Traduccion de botones de QMessageBox ============================================
qt_traductor = QTranslator()
qt_traductor.load("qtbase_" + QLocale.system().name(),QLibraryInfo.location(QLibraryInfo.TranslationsPath))
app.installTranslator(qt_traductor)
productos = productos()
productos.show()
app.exec_()
