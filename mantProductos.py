import sys
import subprocess
import pymysql
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog

class mantProducto(QMainWindow):

        def __init__(self):
                QMainWindow.__init__(self)
                self.setWindowTitle("Agregar Producto") #Título
                uic.loadUi("gui/Mantproductos.ui", self)
        # ----------------------------------  DEFINICIÓN DE EVENTOS   ----------------------------------
                self.btnGuardar.clicked.connect(self.Insertar)
                self.btnCancelar.clicked.connect(self.Cancelar)
                self.btnAgregaCategoria.clicked.connect(self.AgregarCategoria)
                self.btnAgregarProveedor.clicked.connect(self.AgregarProveedor)
                self.listarCombobox()
        # ----------------------------------  DEFINICIÓN PLACERHOLDER   ----------------------------------    
                self.txtCodigo.setPlaceholderText("Código de Barras")
                self.txtDescripcion.setPlaceholderText("Nombre del Producto") 

        # ----------------------------------  AGREGA ELEMENTOS AL LOS COMBOBOX PROVEEDORES Y CATEGORIA DE PRODUCTOS  ----------------------------------    
        def listarCombobox(self):
                conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
                cursor = conn.cursor()
                #LISTA LAS CATEGORIA DE PRODUCTOS
                cursor.execute ("SELECT nombreCategoria FROM categoria_producto")
                lista = cursor.fetchall()
                i = 0
                while i < len(lista):
                         categoria = (str(lista[i]))
                         categoria = categoria[2:]
                         fin = categoria.find("''")
                         categoria = categoria[:fin-2]
                         self.cbxCategoriaProductos.addItem(categoria)
                         self.cbxCategoriaProductos.setCurrentIndex(-1)
                         i = i + 1
                #LISTA LOS PROVEEDORES 
                cursor = conn.cursor()
                cursor.execute ("SELECT nombreProveedor FROM proveedores")
                lista = cursor.fetchall()
                i = 0
                while i < len(lista):
                         categoria = (str(lista[i]))
                         categoria = categoria[2:]
                         fin = categoria.find("''")
                         categoria = categoria[:fin-2]
                         self.cbxProveedores.addItem(categoria)
                         self.cbxProveedores.setCurrentIndex(-1)
                         i = i + 1
                conn.close()

        def AgregarCategoria(self):
             process1 = subprocess.run(['python','mantCategoria.py'])

        def AgregarProveedor(self):
             process1 = subprocess.run(['python','mantProveedores.py'])

        def Insertar(self):
            
            codigo = self.txtCodigo.text()
            descripcion = self.txtDescripcion.text() 
            categoria = self.cbxCategoriaProductos.currentText()
            precioCosto = self.txtPrecioCosto.value()
            precioVenta = self.txtPrecioVenta.value()
            stock = self.txtStock.value()
            stockCritico = self.txtStockCritico.value()
            stockMaximo = self.txtStockMaximo.value()
            proveedor = self.cbxProveedores.currentText()

            if (codigo and descripcion and precioCosto and precioVenta and stock and stockCritico and stockMaximo):
                if codigo.isdigit():
                    # ========== SI LOS DATOS INGRESADO ESTAN OK DEBE CONECTARSE A LA BASE DE DATOS PARA INSERTAR DATOS ========
                    conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
                    cursor = conn.cursor()
                    sql = ("SELECT * FROM productos WHERE idProducto = " + codigo)
                    cursor.execute(sql)
                    valida = cursor.fetchone()
                    print(valida)
                    if valida:
                            QMessageBox.warning(self, 'ERROR', "El codigo de producto ingresado ya existe", QMessageBox.Ok)
                    else:
                            #FECHA PARA GUARDAR EN EL PRECIO PRODUCTO
                            sql = "SELECT DATE_FORMAT(NOW(), '%Y-%m-%d');"
                            #cursor = conn.cursor()
                            cursor.execute(sql)
                            fecha = cursor.fetchone()
                            fecha = str(fecha[0])
                            sql = "SELECT idCategoriaProducto FROM categoria_producto WHERE nombreCategoria = '" + categoria + "'" #CONSULTA POR EL IDCATEGORIA PRODUCTOS USANDO EL TEXT DEL COMBOBOX
                            print(sql)
                            cursor.execute(sql)
                            consulta = cursor.fetchone()
                            categoria = consulta[0]
                            print(proveedor)
                            #INSERTA DATOS EN LA TABLA PRODUCTOS
                            sql = ("INSERT INTO productos(idProducto, nombreProducto,idCategoriaProducto,stock,stockCritico,stockMaximo) VALUES ('" + str(codigo) + "','"+ str(descripcion) + "',"+ str(categoria) + ","+ str(stock) + "," + str(stockCritico) + "," + str(stockMaximo) + ");")    
                            print(sql)
                            cursor.execute(sql)
                            #print(categoria)
                            conn.commit()
                            cursor.execute ("INSERT INTO precio_producto(idProducto,fecha,precioCosto,precioVenta) VALUES (%s,%s,%s,%s)", (codigo,fecha,precioCosto,precioVenta))
                            conn.commit()
                            # CONSULTO EL ID E proveedores y el id categoria productos para guardar en la tabla de interseccion
                            cursor = conn.cursor()
                            sql = "SELECT idProveedor FROM proveedores WHERE nombreProveedor = '" + proveedor + "'"  #CONSULTA POR EL IDPROVEEDOR USANDO EL TEXT DEL COMBOBOX
                            print(sql)
                            cursor.execute (sql)
                            consulta = cursor.fetchone()
                            proveedor = consulta[0]
                            #INSERTA DATOS EN TABLA DE INTERSECCIN PRODUCTO PROVEEDOR
                            cursor.execute("INSERT INTO producto_proveedor(idProducto, idProveedor) VALUES (%s,%s)",(codigo,proveedor))
                            conn.commit()
                            conn.close()
                            self.close()
                            process1 = subprocess.run(['python','Productos.py'])
                else:  
                        QMessageBox.warning(self, 'Error', "El código a ingresar debe ser numérico", QMessageBox.Ok)          
            else:
                    QMessageBox.warning(self, 'Error', "No ha ingresado todos los datos requeridos", QMessageBox.Ok)

        def Cancelar(self):
            self.close()
            process1 = subprocess.run(['python','Productos.py'])

app = QApplication(sys.argv)
#  ===================================== Traduccion de botones de QMessageBox ============================================
qt_traductor = QTranslator()
qt_traductor.load("qtbase_" + QLocale.system().name(),QLibraryInfo.location(QLibraryInfo.TranslationsPath))
app.installTranslator(qt_traductor)
dialogo = mantProducto()
dialogo.show()
app.exec_()
