import sys
import pymysql
from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QMessageBox, QLabel, QPushButton, QLineEdit, QSpinBox
from PyQt5 import uic
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog



class Dialogo(QDialog):
 def __init__(self):
  QDialog.__init__(self)
  self.setWindowTitle("Insertar datos") #Título
  self.resize(300, 300) #Tamaño inicial
  self.setMinimumSize(300, 300) #Tamaño mínimo
  self.setMaximumSize(300, 300) #Tamaño máximo
  #Crear un layout grid
  self.layout = QGridLayout()
  self.setLayout(self.layout) #Agregar el layout al cuadro de diálogo
  self.label_codigo = QLabel("Codigo Producto:") #Etiqueta nombre
  self.txt_codigo = QLineEdit() #Campo para ingresar el nombre
  self.label_nombre = QLabel("Descripción:") #Etiqueta nombre producto
  self.txt_nombre  = QLineEdit() #Campo para ingresar la edad

  self.label_categoria = QLabel("Categoria:") #Etiqueta nombre producto
  self.txt_categoria  = QLineEdit() #Campo para ingresar categoriaProductos (cambiar por menu desplegable)

  self.label_precioCosto= QLabel("Precio Costo:") #Etiqueta nombre producto
  self.txt_precioCosto  = QLineEdit() #Campo para ingresar la edad

  self.label_precioVenta = QLabel("Precio Venta:") #Etiqueta nombre producto
  self.txt_precioVenta  = QLineEdit() #Campo para ingresar la edad

  self.label_proveedor = QLabel("Proveedor:") #Etiqueta nombre producto
  self.txt_proveedor  = QLineEdit() #Campo para ingresar Proveedor (cambiar por menu desplegable)

  self.label_stock = QLabel("Stock:") #Etiqueta nombre producto
  self.txt_stock  = QLineEdit() #Campo para ingresar la edad

  self.label_stockCritico = QLabel("Stock Critico:") #Etiqueta nombre producto
  self.txt_stockCritico  = QLineEdit() #Campo para ingresar la edad

  self.label_stockMaximo = QLabel("Stock Máximo:") #Etiqueta nombre producto
  self.txt_stockMaximo  = QLineEdit() #Campo para ingresar la edad
  #****************************************************************************

  #Botones
  self.btn_insertar = QPushButton("Insertar")
  self.btn_cancelar = QPushButton("Cancelar")

  #Agregar elementos al layout divido en dos columnas
  self.layout.addWidget(self.label_codigo, 1, 1)
  self.layout.addWidget(self.txt_codigo, 1, 2)
  self.layout.addWidget(self.label_nombre, 2, 1)
  self.layout.addWidget(self.txt_nombre, 2, 2)
  self.layout.addWidget(self.label_categoria, 3, 1)
  self.layout.addWidget(self.txt_categoria, 3, 2)
  self.layout.addWidget(self.label_precioCosto, 4, 1)
  self.layout.addWidget(self.txt_precioCosto, 4, 2)
  self.layout.addWidget(self.label_precioVenta, 5, 1)
  self.layout.addWidget(self.txt_precioVenta, 5, 2)
  self.layout.addWidget(self.label_proveedor, 6, 1)
  self.layout.addWidget(self.txt_proveedor, 6, 2)
  self.layout.addWidget(self.label_stock, 7, 1)
  self.layout.addWidget(self.txt_stock, 7, 2)
  self.layout.addWidget(self.label_stockCritico, 8, 1)
  self.layout.addWidget(self.txt_stockCritico, 8, 2)
  self.layout.addWidget(self.label_stockMaximo, 9, 1)
  self.layout.addWidget(self.txt_stockMaximo, 9, 2)

  self.layoutButton = QGridLayout()
#Layout para agrupar los botones
  #Agregar los botones al layoutButton
  self.layoutButton.addWidget(self.btn_insertar, 1, 1)
  self.layoutButton.addWidget(self.btn_cancelar, 1, 2)
#Agregar el layoutButton en la fila 3 columna 2
  self.layout.addLayout(self.layoutButton, 10, 2)

  #Establecer conexión a la base de datos MySql
  self.btn_insertar.clicked.connect(self.Insertar)
  self.btn_cancelar.clicked.connect(self.Cancelar)

 def Insertar(self,conn):
     conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
     a = conn.cursor()
     codigo = self.txt_codigo.text()
     nombre = self.txt_nombre.text()
     categoria = self.txt_categoria.text()
     precioCosto = self.txt_precioCosto.text()
     precioVenta = self.txt_precioVenta.text()
     stock = self.txt_stock.text()
     stockCritico = self.txt_stockCritico.text()
     stockMaximo = self.txt_stockMaximo.text()
     proveedor = self.txt_proveedor.text()
     a.execute ("INSERT INTO productos(idProducto, nombreProducto,idCategoriaProducto,stock,stockCritico,stockMaximo,proveedor, precioCosto,precioVenta) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (codigo,nombre,categoria,stock,stockCritico,stockMaximo,proveedor, precioCosto,precioVenta))
     estado = a.exec_()
     if estado == True:
         QMessageBox.information(self, "Correcto", "Datos guardados", QMessageBox.Discard)
     else:
         QMessageBox.warning(self, "Error", self.db.lastError().text(), QMessageBox.Discard)
     conn.commit()
     conn.close()

 def Cancelar(self):
  self.close()

app = QApplication(sys.argv)
#  ===================================== Traduccion de botones de QMessageBox ============================================
qt_traductor = QTranslator()
qt_traductor.load("qtbase_" + QLocale.system().name(),QLibraryInfo.location(QLibraryInfo.TranslationsPath))
app.installTranslator(qt_traductor)
dialogo = Dialogo()
dialogo.show()
app.exec_()
