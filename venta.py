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
import locale


class venta(QMainWindow):
    # Metodo constructor clase
    def __init__(self):
        # Iniciar el objeto
        QMainWindow.__init__(self)
        # Cargar archivo ui en objeto
        uic.loadUi("gui/venta.ui", self)
        self.statusBar().showMessage(
            "Punto de Venta. Ingrese los productos por codigo y cancele.")
        self.setWindowTitle("Punto de Venta")
        locale.setlocale(locale.LC_ALL, 'de_DE.utf-8')
        # self.btnContar.clicked.connect(self.moverLCD)
# ********************************** BOTONOES ****************************************
        self.crearTabla()
        self.btnAgregarArticulo.clicked.connect(self.agregarArticulosVenta)
        self.btnQuitarArticulo.clicked.connect(self.quitarArticulosVenta)
        self.btnAbonarDeuda.clicked.connect(self.pagoCliente)
        self.btnAnularVenta.clicked.connect(self.anularVenta)
        self.btnClientes.clicked.connect(self.clientes)
        self.btnBuscarArticulo.clicked.connect(self.productos)
        self.btnFinVenta.clicked.connect(self.finVenta)
        self.btnSalir.clicked.connect(self.salir)
        self.btnCerrarCaja.clicked.connect(self.cerrarCaja)
        self.btnCuentaClientes.clicked.connect(self.cuentaClientes)
        self.btnEfectivo.clicked.connect(self.efectivoCaja)
# ********************************** ATAJOS CON TECLADO ****************************************
        self.btnAgregarArticulo.setShortcut("Return")
        self.btnAnularVenta.setShortcut("Esc")
        self.btnEfectivo.setShortcut("F1")
        self.btnBuscarArticulo.setShortcut("F2")
        self.btnEfectivo.setShortcut("F3")
        self.btnCuentaClientes.setShortcut("F4")
        self.btnAbonarDeuda.setShortcut("F5")
        self.btnFinVenta.setShortcut("F6")
        self.btnQuitarArticulo.setShortcut("F7")
        self.btnClientes.setShortcut("F8")
        self.btnCerrarCaja.setShortcut("F12")
# ********************************** FIN ATAJOS CON TECLADO ****************************************

# ********************************** BARRA MENU ****************************************
        self.actionProductos.triggered.connect(self.productos)
        self.actionCategoriaProductos.triggered.connect(
            self.categoriaProductos)
        self.actionProveedores.triggered.connect(self.proveedores)
        self.actionCliente.triggered.connect(self.cliente)
        self.actionMediosDePagos.triggered.connect(self.medioPago)
        self.actionUsuarios.triggered.connect(self.usuarios)
        self.actionComunas.triggered.connect(self.comunas)
        self.actionEfectivoCaja.triggered.connect(self.efectivoCaja)
        self.actionReportes_por_Dia.triggered.connect(
            self.consultaVentasPorDia)
        self.actionVentas_por_Usuarios.triggered.connect(
            self.consultaVentasPorUsuario)
        self.actionHistorial_Precio_Productos.triggered.connect(
            self.consultaPrecioHistoricoProductos)
        self.actionHistorico_Aperturas_Caja.triggered.connect(
            self.consultaAperturaCaja)

# **********************************   CONSULTA POR EL USUARIO DE SISTEMA QUE ESTA TRABAJANDO Y MUESTRA SU NOMBRE Y APELLIDO EN EL TEXTO ABAJO A LA IZQUIERDA ****************************************
        conn = pymysql.connect(host='localhost', user='root',
                               password='JPTapia123', db='mydb')
        cursor = conn.cursor()
        if len(os.sys.argv) > 1:
            # VARIABLE RECUPERADA DE MAINLOGIN.PY
            idUsuario = os.sys.argv[1]
            self.lblUsuario.setText(idUsuario)
            cursor.execute(
                "SELECT nombreUsuario,apellidoPaterno FROM usuarios WHERE idUsuario = %s", idUsuario)
            consultas = cursor.fetchone()
            idUsuario = consultas[0] + " " + consultas[1]
            self.lblNombreCajero.setText(idUsuario)
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(idVenta) FROM ventas")
        consultas = cursor.fetchone()
        print(consultas[0])
        if (consultas[0] == None):
            idVenta = 1
        else:
            idVenta = int(consultas[0]) + 1
        self.lblidVenta.setText(str(idVenta))
        conn.close()


# ********************************** DEFINE EL CARRO DE COMPRAS **********************************

    def crearTabla(self):
        # MODIFICAR TENGO QUE CONSULTAR OTRAS TABLAS
        self.listaVenta.setColumnCount(5)
        self.listaVenta.setSelectionBehavior(
            QAbstractItemView.SelectRows)  # Selecciona la fila completa
        # Selecciona una fila a la vez
        self.listaVenta.setSelectionMode(QAbstractItemView.SingleSelection)
        self.listaVenta.verticalHeader().setVisible(
            False)    # Ocultar encabezado vertical
        # Deshabilitar el comportamiento de arrastrar y soltar
        self.listaVenta.setDragDropOverwriteMode(False)
        # Deshabilitar resaltado del texto del encabezado al seleccionar una fila
        self.listaVenta.horizontalHeader().setHighlightSections(False)
        # Habilita orden descendente o ascendente
        self.listaVenta.setSortingEnabled(True)
        self.listaVenta.setEditTriggers(QAbstractItemView.NoEditTriggers)
        columnas = ('Codigo', 'Descripcion', 'Cantidad',
                    'Precio Unitario', 'Subtotal')
        # define el ancho de las columnas
        self.listaVenta.setHorizontalHeaderLabels(columnas)
        for indice, ancho in enumerate((200, 500, 90, 90, 180), start=0):
            self.listaVenta.setColumnWidth(indice, ancho)
        self.fechaActual()    # DespLegar Fecha Actual

# ********************************** AQUí SERÁ EL FUERTE DEL PROGRAMA, DEBO DESCONTAR DEL INVENTARIO Y VALIDAR QUE QUEDAN ARTICULOS **********************************
# ********************************** FALTA VALIDAR EXITENCIA
# **********************************  FALTA DESCONTAR PRODUCTOS DE LA EXISTENCIA
    def agregarArticulosVenta(self):
        codigo = str(self.txtBuscarArticulo.text())
        if codigo:
            encontro = self.listaVenta.findItems(codigo, Qt.MatchExactly)
            contadorArticulos = self.listaVenta.rowCount()
            if encontro:
                for item in encontro:
                    indice = self.listaVenta.row(item)
                    # =========== AUMENTAR CANTIDAD CUANDO SE REPITE ===================
                    # =========TOMA LA CANTIDAD PARA LUEGO SUMARLA AL REGISTRO =======
                    cant = self.listaVenta.item(indice, 2).text()
                    # ************* AQUÍ VALIDO SI TENGO O NO STOCK ===================
                    conn = pymysql.connect(
                        host='localhost', user='root', password='JPTapia123', db='mydb')
                    cursor = conn.cursor()
                    sql = "SELECT stock FROM productos WHERE idProducto = " + codigo
                    cursor.execute(sql)
                    consultas = cursor.fetchall()
                    conn.close()
                    for consulta in consultas:
                        stock = int(consulta[0])
                        cant = int(cant) + 1
                        if (cant <= stock):
                            # ====================== suma una unidad al item encontrador ================================0
                            unidades = QTableWidgetItem(str(cant))
                            # Suma cantidad a la columna cantidad
                            self.listaVenta.setItem(indice, 2, unidades)
                            # ===================== Calcular el subtotal  ================================
                            rowPrecioUnit = self.listaVenta.item(
                                indice, 3).text()
                            rowPrecioUnit = int(rowPrecioUnit)
                            rowSubtotal = cant * rowPrecioUnit
                            #rowSubtotal = locale.format(
                            #    '%d', cant * rowPrecioUnit, 1)
                            subtotal = QTableWidgetItem(str(rowSubtotal))
                            self.listaVenta.setItem(indice, 4, subtotal)
                            self.txtBuscarArticulo.setText("")
                            precioUnitario = rowPrecioUnit
                        else:
                            QMessageBox.critical(
                                self, "Error de consulta", "No dispone de stock del articulo agregado", QMessageBox.Ok)
            else:
                conn = pymysql.connect(
                    host='localhost', user='root', password='JPTapia123', db='mydb')
                cursor = conn.cursor()
                sql = "SELECT productos.idProducto, productos.nombreProducto, precio_producto.precioVenta, productos.stock FROM productos, precio_producto WHERE productos.idProducto = precio_producto.idProducto AND productos.idProducto = " + \
                    codigo + \
                    " AND precio_producto.fecha = (SELECT MAX(FECHA) FROM mydb.precio_producto WHERE idProducto = " + codigo + ");"
                cursor.execute(sql)
                #cursor.execute("SELECT productos.idProducto, productos.nombreProducto, precio_producto.precioVenta FROM productos, precio_producto WHERE productos.idProducto = precio_producto.idProducto AND productos.idProducto = %s AND precio_producto.fecha = (SELECT MAX(FECHA) FROM mydb.precio_producto) AND idProducto = %s;)", codigo, codigo2)
                consultas = cursor.fetchall()
                conn.close()
                if consultas:
                    # ========================================= INSERTA el item en la tabla  ========================================
                    for consulta in consultas:
                        stock = int(consulta[3])
                        if (stock >= 1):
                            # LO INSERTA EN LA POSICION ROW
                            self.listaVenta.insertRow(contadorArticulos)
                            #code = str(consulta[0])
                            #code =  code[0:len(code)-2]
                            # codigo = QTableWidgetItem(code)    #codigo = QTableWidgetItem(code)
                            codigo = QTableWidgetItem(consulta[0])
                            descripcion = QTableWidgetItem(str(consulta[1]))
                            # definir cuantas veces se repite el mismo articulo en la tabla
                            cantidad = QTableWidgetItem("1")
                            precioUnitario = QTableWidgetItem(str(consulta[2]))
                            subtotal = QTableWidgetItem(str(consulta[2]))
                            self.listaVenta.setItem(
                                contadorArticulos, 0, codigo)
                            self.listaVenta.setItem(
                                contadorArticulos, 1, descripcion)
                            self.listaVenta.setItem(
                                contadorArticulos, 2, cantidad)
                            self.listaVenta.setItem(
                                contadorArticulos, 3, precioUnitario)
                            self.listaVenta.setItem(
                                contadorArticulos, 4, subtotal)
                            self.txtBuscarArticulo.setText("")
                        else:
                            QMessageBox.critical(
                                self, "Error de consulta", "No dispone de stock del articulo agregado", QMessageBox.Ok)
                #    else:
                #        QMessageBox.critical(self, "Sin Stock", "El artículo consultado no tiene stock",QMessageBox.Ok)
                else:
                    QMessageBox.critical(
                        self, "Error de consulta", "El artículo consultado no existe", QMessageBox.Ok)
            items = self.listaVenta.rowCount()
            totalVenta = 0
            for row in range(0, items):
                valor = self.listaVenta.item(row, 4).text()
                totalVenta = totalVenta + int(valor)
            self.lcdNumber.display(totalVenta)
            self.displayNumber.setValue(totalVenta)
            self.txtBuscarArticulo.setText("")
        else:
            QMessageBox.information(
                self, "Error", "Debe ingresar un codigo de producto", QMessageBox.Ok)

    def quitarArticulosVenta(self):
        filaSeleccionada = self.listaVenta.selectedItems()
        if filaSeleccionada:
            respuesta = QMessageBox.warning(self, 'Advertencia', "¿Está usted seguro de quitar el articulos seleccionado?",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if respuesta == QMessageBox.Yes:
                filas = self.listaVenta.selectionModel().selectedRows()
                indice = []
                for i in filas:
                    indice.append(i.row())
                indice.sort(reverse=True)
                for i in indice:
                    id = self.listaVenta.item(i, 0).text()
                    self.listaVenta.removeRow(i)
        else:
            QMessageBox.warning(self, 'Información', "Debe seleccionar una fila",
                                QMessageBox.Ok)
        items = self.listaVenta.rowCount()
        totalVenta = 0
        for row in range(0, items):
            valor = self.listaVenta.item(row, 4).text()
            totalVenta = totalVenta + int(valor)
        self.lcdNumber.display(totalVenta)
        self.displayNumber.setValue(totalVenta)

    def anularVenta(self):
        items = self.listaVenta.rowCount()
        if (items > 0):
            for row in range(0, items):
                # borra el item 1 la cantidad de veces que item habia al precionar anular.
                self.listaVenta.removeRow(0)
            self.lcdNumber.display(0)
            self.displayNumber.setValue(0)
            self.crearTabla()
        else:
            QMessageBox.information(
                self, 'Error', "Carro sin artículos", QMessageBox.Ok)

    def fechaActual(self):
        conn = pymysql.connect(host='localhost', user='root',
                               password='JPTapia123', db='mydb')
        sql = "SELECT DATE_FORMAT(NOW(), '%d-%m-%Y');"
        cursor = conn.cursor()
        cursor.execute(sql)
        fecha = cursor.fetchone()
        fecha = str(fecha[0])
        self.lblFechaActual.setText(fecha)

    def finVenta(self, totalVenta):
        items = self.listaVenta.rowCount()
        if (items < 1):
            QMessageBox.information(
                self, "Error", "No hay artículos en el carro de compra", QMessageBox.Ok)
        else:
            idVenta = int(self.lblidVenta.text())
            totalVenta = str(self.lcdNumber.value())
            totalVenta = int(totalVenta[0:len(totalVenta)-2])
            conn = pymysql.connect(
                host='localhost', user='root', password='JPTapia123', db='mydb')
            cursor = conn.cursor()
            sql = "SELECT DATE_FORMAT(NOW(), '%Y-%m-%d');"
            cursor.execute(sql)
            consulta = cursor.fetchone()
            # conn.close()
            fechaVenta = str(consulta[0])
            folioBoleta = 0
            idMedioPago = 0
            # SI EL FOLIO DE BOLETA Y FOLIO DE MEDIO Y FOLIO MEDIO PAGO ES CERO SIGNIFICARÁ QUE NO SE REGISTRADO EL PAGO DE LA CUENTA
            idUsuario = self.lblUsuario.text()
            #conn = pymysql.connect(host='localhost',user='root',password='JPTapia123',db='mydb')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO ventas(idVenta, montoVenta, folioBoleta, fechaVenta, idMedioPago, idUsuario) VALUES(%s,%s,%s,%s,%s,%s)",
                           (idVenta, totalVenta, folioBoleta, fechaVenta, idMedioPago, idUsuario))
            conn.commit()
            items = self.listaVenta.rowCount()
            for i in range(items):
                codigo = self.listaVenta.item(i, 0).text()
                articulo = self.listaVenta.item(i, 1).text()
                cantidad = self.listaVenta.item(i, 2).text()
                precioUnitario = self.listaVenta.item(i, 3).text()
                subtotal = self.listaVenta.item(i, 4).text()
                carro = [cantidad, articulo, precioUnitario, subtotal]
                cursor.execute("INSERT INTO detalle_venta(idVenta,idProducto,cantidad,precioUnitario,subtotal) VALUES(%s,%s,%s,%s,%s)", (
                    idVenta, codigo, cantidad, precioUnitario, subtotal))
                conn.commit()
                #   CONSULTO EL STOCK QUE REGISTRA LA TABLA PRODUCTOS
                sql = "SELECT stock FROM productos WHERE idProducto = " + codigo
                cursor.execute(sql)
                stock = cursor.fetchone()
                stock = int(stock[0])
                nuevoStock = stock - int(cantidad)
                sql = "UPDATE productos SET stock = '" + \
                    str(nuevoStock) + "' WHERE idProducto = " + str(codigo)
                cursor.execute(sql)
                conn.commit()
            conn.close()
            totalVenta = str(totalVenta)
            idUsuario = str(idUsuario)
            idVenta = str(idVenta)
            self.close()
            process1 = subprocess.run(
                ['python', 'selecMedioPago.py', totalVenta, idUsuario, idVenta])
            # ELIMINAR ID VENTA AL PRECIONAR CANCELAR
            # modificar stock
            # y eliminar detalle de venta y ventas

    def salir(self):
        self.close()

    def cerrarCaja(self):
        idUsuario = self.lblUsuario.text()
        self.close()
        process1 = subprocess.run(['python', 'cierreCaja.py', idUsuario])

    def cuentaClientes(self):
        idUsuario = self.lblUsuario.text()
        process1 = subprocess.run(['python', 'cuentaClientes.py', idUsuario])

    def efectivoCaja(self):
        idUsuario = self.lblUsuario.text()
        conn = pymysql.connect(host='localhost', user='root',
                               password='JPTapia123', db='mydb')
        sql = "SELECT DATE_FORMAT(NOW(), '%Y-%m-%d');"
        cursor = conn.cursor()
        cursor.execute(sql)
        fecha = cursor.fetchone()
        fecha = str(fecha[0])  # ******
        cursor = conn.cursor()
        sql = "SELECT montoInicial FROM caja WHERE idUsuario = " + \
            idUsuario + " AND fecha = '" + fecha + "'"
        cursor.execute(sql)
        consulta = cursor.fetchone()
        montoInicial = str(consulta[0])
        sql = "SELECT SUM(montoVenta) FROM ventas WHERE idUsuario = " + \
            idUsuario + " AND fechaVenta = '" + fecha + "' AND idMedioPago = 1;"
        cursor.execute(sql)
        consulta = cursor.fetchone()
        if (consulta[0] != None):
            montoVentas = int(consulta[0])
        else:
            montoVentas = 0
        cursor = conn.cursor()
        sql = "SELECT SUM(monto) FROM abono_cliente WHERE idUsuario = '" + \
            idUsuario + "' AND fechaPago LIKE '%" + fecha + "%'"
        print(sql)
        cursor.execute(sql)
        query = cursor.fetchone()
        if (query[0]):
            montoAbonos = int(query[0])
        else:
            montoAbonos = 0
        montoInicial = int(montoInicial)
        efectivoCaja = montoVentas + montoAbonos + montoInicial
        efectivoCaja = int(efectivoCaja)
        locale.setlocale(locale.LC_ALL, '')
        # +++++++++++++++++++++++++ FALTA AGREGAR EL PUNTO DE SEPARACIÓN DE NUMEROS AL EFECTIVO EN CAJA +++++++++++++++++++++++++++++++
        QMessageBox.information(self, "Información", "Actualmente dispone de : $ {:n}".format(
            efectivoCaja) + " de efectivo en caja", QMessageBox.Ok)

    # ============================ ACCIONES AL PRECIONAR EL MENU ============================
    def productos(self):
        self.setEnabled(False)
        process1 = subprocess.run(['python', 'productos.py'])

    def categoriaProductos(self):
        process1 = subprocess.run(['python', 'categoriaProductos.py'])

    def proveedores(self):
        process1 = subprocess.run(['python', 'proveedores.py'])

    def cliente(self):
        process1 = subprocess.run(['python', 'clientes.py'])

    def medioPago(self):
        process1 = subprocess.run(['python', 'medioPago.py'])

    def usuarios(self):
        process1 = subprocess.run(['python', 'login.py'])

    def pagoCliente(self):
        idUsuario = self.lblUsuario.text()
        process1 = subprocess.run(['python', 'pagoCliente.py', idUsuario])

    def clientes(self):
        process1 = subprocess.run(['python', 'clientes.py'])

    def comunas(self):
        process1 = subprocess.run(['python', 'comunas.py'])

    def productos(self):
        process1 = subprocess.run(['python', 'productos.py'])

    def comunasReport(self):
        process1 = subprocess.run(['python', 'consultaComunas.py'])

    def consultaVentasPorDia(self):
        process1 = subprocess.run(['python', 'consultaVentasDia.py'])

    def consultaVentasPorUsuario(self):
        process1 = subprocess.run(['python', 'consultaVentasUsuario.py'])

    def consultaPrecioHistoricoProductos(self):
        process1 = subprocess.run(
            ['python', 'consultaPrecioHistoricoProductos.py'])

    def consultaAperturaCaja(self):
        process1 = subprocess.run(['python', 'consultaAperturaCaja.py'])


app = QApplication(sys.argv)  # inicia aplicacion
qt_traductor = QTranslator()
qt_traductor.load("qtbase_" + QLocale.system().name(),
                  QLibraryInfo.location(QLibraryInfo.TranslationsPath))
app.installTranslator(qt_traductor)
venta = venta()  # Crear objeto de clase ventana
venta.show()  # Mostrar la ventana
app.exec_()  # Ejecutar la aplicacion
