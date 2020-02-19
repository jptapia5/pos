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
import tempfile
import win32api
import win32print
import win32ui
import win32con



#clase heredada de QMainWindow (Constructor Ventana)
class window(QMainWindow):
    #Metodo constructor clase
    def __init__(self):
        #Iniciar el objeto
        QMainWindow.__init__(self)
        #Cargar archivo ui en objeto
        uic.loadUi("gui/pagoEfectivo.ui",self)
        self.statusBar().showMessage("Bienvenido")
        totalVenta = os.sys.argv[1]   #recibe el valor de selMedioPago como float
        idUsuario = os.sys.argv[2]  #recibe el valor desde ventas
        idVenta = os.sys.argv[3]  #recibe el valor desde ventas
        print(totalVenta)
        print(idUsuario)
        print(idVenta)
        totalVenta =  totalVenta[0:len(totalVenta)-2]
        self.lcdTotalVenta.display(totalVenta)
        self.displayTotalVenta.setValue(int(totalVenta))
        self.lblIdUsuario.setText(idUsuario)
        self.lblidVenta.setText(idVenta)
        #idUsuario = self.lblIdUsuario.text(idUsuario)
        int(totalVenta)
        self.btnAceptar.clicked.connect(self.aceptar)
        self.btnCancelar.clicked.connect(self.cancelar)
        self.btnFin.clicked.connect(self.fin)
        self.btnAceptar.setShortcut("Return")    # Establece atajo con teclado

        #    DOC IMPRIMIR TICKET
        self.documento = QTextDocument()
        self.treeWidgetVentas.setFont(QFont(self.treeWidgetVentas.font().family(), 10, False))
        self.treeWidgetVentas.setRootIsDecorated(False)
        self.treeWidgetVentas.setHeaderLabels(("PRODUCTO", "PRECIO", "CANTIDAD", "SUBTOTAL" ))
        self.model = self.treeWidgetVentas.model()

        for indice, ancho in enumerate((250, 250, 250, 250, 250), start=0):
            self.model.setHeaderData(indice, Qt.Horizontal, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.treeWidgetVentas.setColumnWidth(indice, ancho)
        self.treeWidgetVentas.setAlternatingRowColors(True)

    def aceptar(self,totalVenta):
        totalVenta = int(self.lcdTotalVenta.value())
        efectivo = self.txtPagaCon.value()
        vuelto = efectivo - totalVenta
        self.lcdVuelto.display(vuelto)
        self.displayVuelto.setValue(vuelto)
        #self.btnAceptar.setEnabled(False)
        self.btnFin.setEnabled(True)
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        sql = "SELECT MAX(folioBoleta) FROM ventas"
        cursor = conn.cursor()
        cursor.execute(sql)
        consulta = cursor.fetchone()
        nroBoleta = int(consulta[0]) + 1
        print(nroBoleta)
        self.txtNboleta.setValue(nroBoleta)

    def fin(self):
        #OBTIENE LA FECHA DE LA BASE DE DATOS
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        sql = "SELECT DATE_FORMAT(NOW(), '%Y-%m-%d');"
        cursor = conn.cursor()
        cursor.execute(sql)
        #fecha = cursor.fetchone()
        conn.close()
        #fechaVenta = str(fecha[0])
        idVenta = str(self.lblidVenta.text())
        #totalVenta = self.lcdTotalVenta.value()
        folioBoleta = str(self.txtNboleta.text())
        idMedioPago = str(1)  # YA SE SABE QUE EL MEDIO DE PAGO ES EN EFECTIVO POR LO TANTO EL ID QUE CORRESPONDE ES 1
        idCliente = str(0) # EN MEDIO DE PAGO EFECTIVO NO REGISTRA CLIENTE
        idUsuario = self.lblIdUsuario.text()
        conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
        cursor = conn.cursor()
        sql = "SELECT * FROM ventas WHERE folioBoleta = " + folioBoleta
        print(sql)
        cursor.execute(sql)
        valida = cursor.fetchone()
        if valida:
                QMessageBox.warning(self, "ERROR", "Le numero de boleta ya fue utilizado.",QMessageBox.Ok)
        else:
                sql = "UPDATE ventas SET idMedioPago = " + idMedioPago + ", folioBoleta = " + folioBoleta + " WHERE idVenta = " + idVenta
                print(sql)
                cursor.execute(sql)
                conn.commit()
                #******************************************   IMPRIMIR TICKET DE VENTA ******************************** ********
                #***************************************************************************************************************

                conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
                cursor = conn.cursor()
                sql = "SELECT detalle_venta.cantidad, productos.nombreProducto, detalle_venta.precioUnitario, detalle_venta.subtotal FROM productos, detalle_venta WHERE detalle_venta.idVenta = " + idVenta + " AND  detalle_venta.idProducto = productos.idProducto"
                print(sql)
                cursor.execute(sql)
                datosDB = cursor.fetchall()
                print(datosDB)
                conn.close()

# ********************************                EMPIEZA A IMPRIMIR               ********************************
# create a dc (Device Context) object (actually a PyCDC)
                dc = win32ui.CreateDC()
                # convert the dc into a "printer dc"
                dc.CreatePrinterDC("POS-PRINTER") #define la impresora a usar segun nombre que tiene en windows
                # you need to set the map mode mainly so you know how
                # to scale your output.  I do everything in points, so setting 
                # the map mode as "twips" works for me.
                dc.SetMapMode(win32con.MM_TWIPS) # 1440 per inch
                # here's that scaling I mentioned:
                scale_factor = 20 # i.e. 20 giros al punto
                dc.StartDoc("TICKET DE VENTA POS") # INICIA LA IMPRESION DEL DOCUMENTO. ESTE ES UN STRIG QUE SE MUESTRA EN LA COLA DE IMRPESIÓN.
                pen = win32ui.CreatePen(0, int(scale_factor), 0) # para dibujar algo necesitas un lapiz. Las variables son estilo de pluma, ancho de pluma y color de pluma.
                # SelectObject is used to apply a pen or font object to a dc.
                dc.SelectObject(pen)
                # how about a font?  Lucida Console 10 point.
                # I'm unsure how to tell if this failed.
                font = win32ui.CreateFont({
                    "name": "Lucida Console",
                    "height": int(scale_factor * 10),               # tamaño de la letra
                    "weight": 400,
                })
                # again with the SelectObject call.
                dc.SelectObject(font)
                # okay, now let's print something.
                # TextOut takes x, y, and text values.
                # the map mode determines whether y increases in an
                # upward or downward direction; in MM_TWIPS mode, it
                # advances up, so negative numbers are required to 
                # go down the page.  If anyone knows why this is a
                # "good idea" please email me; as far as I'm concerned
                # it's garbage.
                # 30 LÍNEAS DE TEXTO EN EL PAPEL
                dc.StartPage()
                dc.TextOut(scale_factor * 0,10 * scale_factor * 0,"<*****TEXTO DE 34 CARACTERES*****>") 
                dc.EndPage()
                dc.StartPage()
                dc.TextOut(scale_factor * 0,10 * scale_factor * 0,"        ALMACÉN DON TITO          ")
                dc.EndPage()
                dc.StartPage()
                dc.TextOut(scale_factor * 0,10 * scale_factor * 0,"Esmeralda 123 Villa Sn José El Melón")
                dc.EndPage()        
                dc.StartPage()
                dc.TextOut(scale_factor * 0,10 * scale_factor * 0,"*") 
                dc.EndPage()
                dc.TextOut(scale_factor * 0,10 * scale_factor * 0,"Nro Boleta : " + str(folioBoleta))
                dc.EndPage()
                dc.StartPage()
                dc.TextOut(scale_factor * 0,10 * scale_factor * 0,"<**************************>")
                dc.EndPage()
                dc.StartPage()
                dc.TextOut(scale_factor * 0,10 * scale_factor * 0,"<**************************>")
                dc.EndPage()
                dc.StartPage()
                dc.TextOut(scale_factor * 0,10 * scale_factor * 0,"<**************************>")
                dc.EndPage()
                dc.StartPage()
                dc.TextOut(scale_factor * 0,10 * scale_factor * 0,"<**************************>")
                dc.EndPage()
                dc.StartPage()
                dc.TextOut(scale_factor * 0,10 * scale_factor * 0,"<**************************>")
                dc.EndPage()
                dc.StartPage()
                dc.TextOut(scale_factor * 0,10 * scale_factor * 0,"<**************************>")
                dc.EndPage()
                dc.StartPage()
                dc.TextOut(scale_factor * 0,10 * scale_factor * 0,"<**************************>")
                dc.EndPage()
                dc.StartPage()
                dc.TextOut(scale_factor * 0,10 * scale_factor * 0,"<**************************>")
                dc.EndPage()
                dc.StartPage()
                dc.TextOut(scale_factor * 0,10 * scale_factor * 0,"<**************************>")
                dc.EndPage()
                dc.StartPage()
                dc.TextOut(scale_factor * 0,10 * scale_factor * 0,"<**************************>")
                dc.EndPage()
                dc.StartPage()
                dc.TextOut(scale_factor * 0,10 * scale_factor * 0,"<**************************>")
                dc.EndPage()
                dc.StartPage()
                dc.TextOut(scale_factor * 0,10 * scale_factor * 0,"<**************************>")
                dc.EndPage()
                dc.StartPage()
                dc.TextOut(scale_factor * 0,10 * scale_factor * 0,"<**************************>")
                dc.EndPage()
                dc.StartPage()
                dc.TextOut(scale_factor * 0,10 * scale_factor * 0,"<**************************>")
                dc.EndPage()
                dc.StartPage()
                dc.TextOut(scale_factor * 0,10 * scale_factor * 0,"<**************************>")
                dc.EndPage()
                dc.StartPage()
                dc.TextOut(scale_factor * 0,10 * scale_factor * 0,"<**************************>")
                dc.EndPage()
                dc.StartPage()
                dc.TextOut(scale_factor * 0,10 * scale_factor * 0,"<**************************>")
                dc.EndPage()
                dc.StartPage()
                dc.TextOut(scale_factor * 0,10 * scale_factor * 0,"<**************************>")
                dc.EndPage()
                dc.StartPage()
                dc.TextOut(scale_factor * 0,10 * scale_factor * 0,"<**************************>")
                dc.EndPage()
                dc.StartPage()
                dc.TextOut(scale_factor * 0,10 * scale_factor * 0,"<**************************>")
                dc.EndPage()
                dc.StartPage()
                dc.TextOut(scale_factor * 0,10 * scale_factor * 0,"<**************************>")
                dc.EndPage()
                dc.StartPage()
                dc.TextOut(scale_factor * 0,10 * scale_factor * 0,"<**************************>")
                dc.EndPage()
                dc.StartPage()
                dc.TextOut(scale_factor * 0,10 * scale_factor * 0,"<**************************>")
                dc.EndPage()
                dc.StartPage()
                dc.TextOut(scale_factor * 0,10 * scale_factor * 0,"<**************************>")
                dc.EndPage()
                dc.StartPage()
                dc.TextOut(scale_factor * 0,10 * scale_factor * 0,"<Gracias por su preferencia>")
                dc.EndPage()
                # for completeness, I'll draw a line.
                #from x = "1", y = "1"
                #dc.MoveTo((scale_factor * 72, scale_factor * -72))
                dc.MoveTo((scale_factor * 0, scale_factor * 0))
                #to x = 6", y = 3"
                #dc.LineTo((scale_factor * 6 * 72, scale_factor * 3 * -72))
                dc.LineTo((scale_factor * 72 *  10, scale_factor * 0))
                # must not forget to tell Windows we're done.
                dc.EndDoc()
## ********************************                  FIN IMPRIMIR                  ********************************
                QMessageBox.information(self, "Gracias", "Agradecemos su preferencia. Vuelva cuando guste.",QMessageBox.Ok)
                self.close()
                process1 = subprocess.run(['python','venta.py',idUsuario])

    def cancelar(self):
        idUsuario = self.lblIdUsuario.text()
        self.btnAceptar.setEnabled(True)
        self.btnFin.setEnabled(False)
        self.close()
        process1 = subprocess.run(['python','venta.py',idUsuario])

app = QApplication(sys.argv)        #inicia aplicacion
#  ===================================== Traduccion de botones de QMessageBox ============================================
qt_traductor = QTranslator()
qt_traductor.load("qtbase_" + QLocale.system().name(),QLibraryInfo.location(QLibraryInfo.TranslationsPath))
app.installTranslator(qt_traductor)
window = window()                   #Crear objeto de clase ventana
window.show()                       #Mostrar la ventana
app.exec_()                         #Ejecutar la aplicacion
