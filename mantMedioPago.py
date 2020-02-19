import sys
import subprocess
import pymysql
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog

class mantMedioPago(QMainWindow):
         def __init__(self):
                  QMainWindow.__init__(self)
                  self.setWindowTitle("Agregar Producto") #Título
                  uic.loadUi("gui/mantMedioPago.ui", self)
                  self.statusBar().showMessage("Ingresará un nuevo medio de pago al sistema")
                  #Establecer conexión a la base de datos MySql
                  self.btnGuardar.clicked.connect(self.Insertar)
                  self.btnCancelar.clicked.connect(self.Cancelar)

         def Insertar(self):
                 QMessageBox.question(self, 'Error', "¿Está usted seguro de guardar los datos ingresados?",
                                  QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
                 codigo = self.txtIdMedioPago.value()
                 descripcion = self.txtMedioPago.text() #COMO OBTENER EL TEXTO
                 print(codigo)
                 print(descripcion)
                 conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
                 cursor = conn.cursor()
                 cursor.execute ("INSERT INTO medio_de_pago(idMedioPago, nombreMedioPago) VALUES (%s,%s)", (codigo,descripcion))
                 conn.commit()
                 conn.close()
                 self.close()
                 process1 = subprocess.run(['python','medioPago.py'])

                 """======================== DEBO VALIDAR INGRESO DE DATOS SI OCURRE ERRORES O NO =============================="""

         def Cancelar(self):
                  self.close()
                  process1 = subprocess.run(['python','medioPago.py'])

app = QApplication(sys.argv)
#  ===================================== Traduccion de botones de QMessageBox ============================================
qt_traductor = QTranslator()
qt_traductor.load("qtbase_" + QLocale.system().name(),QLibraryInfo.location(QLibraryInfo.TranslationsPath))
app.installTranslator(qt_traductor)
mantMedioPago = mantMedioPago()
mantMedioPago.show()
app.exec_()
