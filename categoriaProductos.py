import sys
import subprocess
import pymysql
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
#clase heredada de QMainWindow (Constructor Ventana)
class categoria_productos(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("gui\categoriaProductos.ui", self)
        self.setWindowTitle("Listado de Categoria de Productos") #Título
        self.listar()
        self.habilitarBotones()
        self.btnRefrescar.clicked.connect(self.listar)
        self.btnAgregar.clicked.connect(self.agregar)
        self.btnEliminar.clicked.connect(self.eliminar)
        self.btnModificar.clicked.connect(self.modificar)
        self.btnCancelar.clicked.connect(self.listar)
        self.btnSalir.clicked.connect(self.salir)
        self.btnBuscar.clicked.connect(self.buscar)
        self.btnRefrescar.clicked.connect(self.listar)
        self.tablaCategoriaProductos.verticalHeader().setVisible(False)    # Ocultar encabezado vertical
        self.tablaCategoriaProductos.setDragDropOverwriteMode(False)    # Deshabilitar el comportamiento de arrastrar y soltar
        self.tablaCategoriaProductos.horizontalHeader().setHighlightSections(False)    # Deshabilitar resaltado del texto del encabezado al seleccionar una fila

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

    def listar(self):
        self.tablaCategoriaProductos.setRowCount(0)
        self.tablaCategoriaProductos.clearContents()        
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        cursor = conn.cursor()
        cursor.execute ("SELECT * FROM categoria_producto")
        #self.habilitarBotones()
        self.tablaCategoriaProductos.clearContents()
        self.tablaCategoriaProductos.horizontalHeader().setStretchLastSection(True)
        # Establecer el número de columnas
        self.tablaCategoriaProductos.setColumnCount(2)
        self.tablaCategoriaProductos.setSortingEnabled(False) # Habilita orden descendente o ascendente
        # Establecer el número de filas
        self.tablaCategoriaProductos.setRowCount(0)
        # Ocultar encabezado vertical
        self.tablaCategoriaProductos.verticalHeader().setVisible(False)
        # Deshabilitar el comportamiento de arrastrar y soltar
        self.tablaCategoriaProductos.setDragDropOverwriteMode(False)
        # Deshabilitar resaltado del texto del encabezado al seleccionar una fila
        self.tablaCategoriaProductos.horizontalHeader().setHighlightSections(False)
        columnas = ('Codigo', 'Categoria')
        self.tablaCategoriaProductos.setHorizontalHeaderLabels(columnas)
        #deshabilita la edición de la tabla
        self.tablaCategoriaProductos.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Deshabilitar el comportamiento de arrastrar y soltar
        self.tablaCategoriaProductos.setDragDropOverwriteMode(False)
        consultas = cursor.fetchall()
        row = 0
        for consulta in consultas:
             #print (consulta)
             self.tablaCategoriaProductos.insertRow(row)
             idCategoria = QTableWidgetItem(str(consulta[0]))
             nombreCategoria = QTableWidgetItem(str(consulta[1]))
             self.tablaCategoriaProductos.setItem(row, 0, idCategoria)
             self.tablaCategoriaProductos.setItem(row, 1, nombreCategoria)
             row = row + 1
        conn.close()

    def agregar(self):
         print("agregar productos")
         self.close()
         process1 = subprocess.run(['python','mantCategoria.py'])

    def eliminar(self):
        filaSeleccionada = self.tablaCategoriaProductos.selectedItems()
        if filaSeleccionada:
            respuesta = QMessageBox.critical(self, 'Advertencia', "Está a punto de eliminar el item seleccionado. Los productos relacionados al item pasaran a categoria genérica ¿Está usted seguro de querer hacerlo?",
                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if respuesta == QMessageBox.Yes:
                filas = self.tablaCategoriaProductos.selectionModel().selectedRows()
                indice = []
                for i in filas:
                    indice.append(i.row())
                indice.sort(reverse = True)
                for i in indice:
                    id = self.tablaCategoriaProductos.item(i, 0).text()
                    if (id == "0"):
                        QMessageBox.information(self, 'Información', "No se puede eliminar la categoria 'Generica'",  QMessageBox.Ok)
                    else:
                            self.tablaCategoriaProductos.removeRow(i)
                            print(id)
                            # UPDATE PRODUCTOS DE CATEGORIA id
                            sql = "UPDATE productos SET idCategoriaProducto = 0 WHERE idCategoriaProducto =" + id
                            print(sql)
                            conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
                            cursor = conn.cursor()
                            cursor.execute(sql)
                            conn.commit()
                            sql = "DELETE FROM categoria_producto WHERE idCategoriaProducto=" + id
                            print(sql)
                            cursor = conn.cursor()
                            cursor.execute(sql)
                            conn.commit()
                            conn.close()
        else:
            QMessageBox.information(self, 'Información', "Debe seleccionar una fila",  QMessageBox.Ok)
                      

    def modificar(self):
        respuesta = QMessageBox.warning(self, 'Advertencia', "¿Está usted seguro de modificar las categorias de productos?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if respuesta == QMessageBox.Yes:
                        filaSeleccionada = self.tablaCategoriaProductos.selectedItems()
                        if filaSeleccionada:
                            indice = self.tablaCategoriaProductos.currentRow() #la fila que modificará, solo una a la vez
                        else:
                            indice = 0
                            #habilita la edición de la tabla
                            self.deshabilitarBotones()
                            #self.listaProductos.setEnabled(False)
                            self.tablaCategoriaProductos.setEditTriggers(QAbstractItemView.DoubleClicked)
                            #self.listaProductos.setEditTriggers(QAbstractItemView.AllEditTriggers)
                            #self.listaProductos.setEditTriggers(QAbstractItemView.NoEditTriggers)
                            #self.listaProductos.setEditTriggers(QAbstractItemView.CurrentChanged)
                            #self.listaProductos.setEditTriggers(QAbstractItemView.SelectedClicked)  
                            self.tablaCategoriaProductos.setSelectionBehavior(QAbstractItemView.SelectItems)              
                            #self.btnGuardar.clicked.connect(self.guardar)
                            idProducto = str(self.tablaCategoriaProductos.item(indice,0).text()) # lee valor de la primera columna, el identificador de la fila que modificara
                            #self.statusBar().showMessage('Barra de estado : ' + str(idProducto) + "")
                            self.tablaCategoriaProductos.itemChanged.connect(self.guardar)
                            self.btnCancelar.clicked.connect(self.cancelar)

    def buscar(self):
        busqueda = str(self.txtBuscar.text())
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        cursor = conn.cursor()
        if busqueda == "":
            QMessageBox.warning(self, 'Información', "No ha aplicado ningun criterio de búsqueda",QMessageBox.Ok)
        else:
            if self.filtroDescripcion.isChecked():
                #self.contruirTabla()
                sql = "SELECT * FROM categoria_producto WHERE nombreCategoria LIKE '%" + busqueda + "%';"                
                print(sql)
                cursor.execute(sql)
                consultas = cursor.fetchall()
                print(consultas)
                self.tablaCategoriaProductos.setRowCount(0)
                self.tablaCategoriaProductos.clearContents()                
                row = 0
                #self.habilitarBotones()
                #self.tablaCategoriaProductos.setEditTriggers(QAbstractItemView.NoEditTriggers)
                #self.tablaCategoriaProductos.setDragDropOverwriteMode(False)
                if not consultas:
                        QMessageBox.information(self, 'Información', "No se encontraron resultados",QMessageBox.Ok)
                else :                
                        for consulta in consultas:
                                print(row)
                                self.tablaCategoriaProductos.insertRow(row)
                                idCategoria = QTableWidgetItem(str(consulta[0]))
                                nombreCategoria = QTableWidgetItem(str(consulta[1]))
                                self.tablaCategoriaProductos.setItem(row, 0, idCategoria)
                                self.tablaCategoriaProductos.setItem(row, 1, nombreCategoria)
                                row = row + 1
                        self.txtBuscar.setText("")     
            if self.filtroCodigo.isChecked():
                if busqueda.isdigit():
                        #self.contruirTabla()
                        self.tablaCategoriaProductos.setRowCount(0)
                        self.tablaCategoriaProductos.clearContents()
                        sql = "SELECT * FROM categoria_producto WHERE idCategoriaProducto = " + busqueda + ";"
                        print(sql)
                        cursor.execute(sql)
                        consultas = cursor.fetchall()
                        row = 0
                        #self.habilitarBotones()
                        #self.tablaCategoriaProductos.setEditTriggers(QAbstractItemView.NoEditTriggers)
                        #self.tablaCategoriaProductos.setDragDropOverwriteMode(False)
                        if not consultas:
                                QMessageBox.information(self, 'Información', "No se encontraron resultados",QMessageBox.Ok)
                        else :                
                                for consulta in consultas:
                                        self.tablaCategoriaProductos.insertRow(row)
                                        idCategoria = QTableWidgetItem(str(consulta[0]))
                                        nombreCategoria = QTableWidgetItem(str(consulta[1]))
                                        self.tablaCategoriaProductos.setItem(row, 0, idCategoria)
                                        self.tablaCategoriaProductos.setItem(row, 1, nombreCategoria)
                                        row = row + 1
                        self.txtBuscar.setText("")          
                else:
                    self.tablaCategoriaProductos.setRowCount(0)
                    self.tablaCategoriaProductos.clearContents()
                    QMessageBox.information(self, 'Información', "No se encontraron resultados",QMessageBox.Ok)
                            

    def guardar(self):
        columna = self.tablaCategoriaProductos.currentColumn() #la columna que modificará, solo una a la vez
        if columna == 0 :
            QMessageBox.warning(self, 'Error', "No puede modificar el campo id de categoria, intente nuevamenta",	QMessageBox.Ok)
            #print("ENTRO AL IF")
            #self.habilitarBotones()
            #self.tablaCategoriaProductos.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.listar()
        if columna == 1 :
            #print("ENTRO AL ELSE")
            #columna = self.tablaCategoriaProductos.currentColumn() #la columna que modificará, solo una a la vez
            fila = self.tablaCategoriaProductos.currentRow() #la fila que modificará, solo una a la vez
            #el id de la fila que modificara
            id = str(self.tablaCategoriaProductos.item(fila,0).text()) # lee valor de la primera columna, el identificador
            valor = self.tablaCategoriaProductos.currentItem().text()#el valor que le dio al campo que modificará
            #print(campo)
            sql = ("UPDATE categoria_producto SET nombreCategoria = '" + valor + "' WHERE idCategoriaProducto = " + id )
            print(sql)
            conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            conn.close()

    def cancelar(self):
        self.close() 
        #self.listarTodo()
        process1 = subprocess.run(['python','categoriaProductos.py'])         

    def dobleClick(self):
       QMessageBox.warning(self, 'DobleClick', "Hizo doble click en un item de la tabla",QMessageBox.Ok)


    def salir(self):
        #print("******** SALIR DEL PROGRAMA ********")
        self.close()

app = QApplication(sys.argv)
categoria_productos = categoria_productos()
categoria_productos.show()
app.exec_()
