import sys
import subprocess
import pymysql
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog

class Mantcategoria_producto(QMainWindow):
    #Metodo constructor clase
    def __init__(self):
        #Iniciar el objeto
        QMainWindow.__init__(self)
        #Cargar archivo ui en objeto
        uic.loadUi("gui/mantCategoria.ui",self)
        self.statusBar().showMessage("Agregue una Nueva Categoria de Productos al Sistemas")
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        self.statusBar().showMessage("Permite agregar una nueva categoria para clasificar productos en su sistema.")
        self.btnGuardar.clicked.connect(self.guardar)
        self.btnCancelar.clicked.connect(self.Cancelar)
        self.carga(conn)

    def carga(self,conn):
        cursor = conn.cursor()
        sql = ("SELECT count(idCategoriaProducto) FROM categoria_producto")
        registros = cursor.execute(sql)
        print(registros)
        conn.commit()
        conn.close()

    def guardar(self,conn):
        id = self.txtIdCategoria.text()
        nombreCategoria = self.txtNombreCategoria.text() 
        if id and nombreCategoria:
                conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
                cursor = conn.cursor()
                cursor.execute ("SELECT * FROM categoria_producto WHERE idCategoriaProducto = %s", id)
                consulta = cursor.fetchone()
                if consulta:
                    QMessageBox.information(self, "Error", "El codigo de categoria ya existe",QMessageBox.Ok)
                else:
                    nombreCategoria = self.txtNombreCategoria.text() 
                    cursor.execute ("INSERT INTO categoria_producto(idCategoriaProducto, nombreCategoria) VALUES (%s,%s)", (id,nombreCategoria))
                    conn.commit()
                    conn.close()
                    self.close()
                    process1 = subprocess.run(['python','categoriaProductos.py'])
        else:
                QMessageBox.information(self, "Error", "Ingrese todos los campos requeridos",QMessageBox.Ok)



    def Cancelar(self):
        self.close()
        process1 = subprocess.run(['python','categoriaProductos.py'])


app = QApplication(sys.argv)        #inicia aplicacion

#  ===================================== Traduccion de botones de QMessageBox ============================================
qt_traductor = QTranslator()
qt_traductor.load("qtbase_" + QLocale.system().name(),QLibraryInfo.location(QLibraryInfo.TranslationsPath))
app.installTranslator(qt_traductor)




Mantcategoria_producto = Mantcategoria_producto()                   #Crear objeto de clase ventana
Mantcategoria_producto.show()                       #Mostrar la ventana
app.exec_()                         #Ejecutar la aplicacion
