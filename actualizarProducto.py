import sys
from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QMessageBox, QTableWidget, QTableWidgetItem, QPushButton
from PyQt5 import uic
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog

class Dialogo(QDialog):
	def __init__(self):
		QDialog.__init__(self)
		self.setWindowTitle("Administrar usuarios") #Título
		self.resize(800, 600) #Tamaño inicial
		self.layout = QGridLayout() #Crear un layout grid
		self.setLayout(self.layout) #Agregar el layout al cuadro de diálogo
		self.table = QTableWidget() #Crear la tabla
		self.btn_eliminar = QPushButton("Eliminar fila/s")
		self.layout.addWidget(self.btn_eliminar)
		self.layout.addWidget(self.table) #Agregar la tabla al layout
		#Establecer conexión a la base de datos MySql
		self.db = QSqlDatabase.addDatabase('QMYSQL')
		self.db.setHostName("localhost")
		self.db.setDatabaseName("usuarios")
		self.db.setUserName("root")
		self.db.setPassword("password")
		self.Seleccionar()
		self.table.itemChanged.connect(self.Actualizar)
		self.btn_eliminar.clicked.connect(self.Eliminar)

	def Seleccionar(self):
		estado = self.db.open()
		if estado == False:
			QMessageBox.warning(self, "Error", self.db.lastError().text(), QMessageBox.Discard)
		else:
			self.table.setColumnCount(3)
			self.table.setHorizontalHeaderLabels(['id', 'nombre', 'edad'])
			row = 0
			sql = "SELECT * FROM usuarios"
			query = QSqlQuery(sql)
			while query.next():
				self.table.insertRow(row)
				id = QTableWidgetItem(str(query.value(0)))
				nombre = QTableWidgetItem(str(query.value(1)))
				edad = QTableWidgetItem(str(query.value(2)))
				self.table.setItem(row, 0, id)
				self.table.setItem(row, 1, nombre)
				self.table.setItem(row, 2, edad)
				row = row + 1
		self.db.close()

	def Actualizar(self):
		estado = self.db.open()
		if estado == False:
			QMessageBox.warning(self, "Error", self.db.lastError().text(), QMessageBox.Discard)
		else:
			column = self.table.currentColumn()
			row = self.table.currentRow()
			id = self.table.item(row, 0).text()
			value = self.table.currentItem().text()
			columns = ['id', 'nombre', 'edad']
			query = QSqlQuery()
			sql = "UPDATE usuarios SET " + columns[column] + "=" + ":value WHERE id=:id"
			query.prepare(sql)
			query.bindValue(":id", id)
			query.bindValue(":value", value)
			estado = query.exec_()
			if estado == False:
				QMessageBox.warning(self, "Error", self.db.lastError().text(), QMessageBox.Discard)
		self.db.close()

	def Eliminar(self):
		estado = self.db.open()
		if estado == False:
			QMessageBox.warning(self, "Error", self.db.lastError().text(), QMessageBox.Discard)
		else:
			rows = self.table.selectionModel().selectedRows()
			index = []
			for i in rows:
				index.append(i.row())
			index.sort(reverse=True)
			for i in index:
				id = self.table.item(i, 0).text()
				self.table.removeRow(i)
				sql = "DELETE FROM usuarios WHERE id=:id"
				query = QSqlQuery()
				query.prepare(sql)
				query.bindValue(":id", id)
				estado = query.exec_()
				if estado == False:
					QMessageBox.warning(self, "Error", self.db.lastError().text(), QMessageBox.Discard)
		self.db.close()

app = QApplication(sys.argv)
#  ===================================== Traduccion de botones de QMessageBox ============================================
qt_traductor = QTranslator()
qt_traductor.load("qtbase_" + QLocale.system().name(),QLibraryInfo.location(QLibraryInfo.TranslationsPath))
app.installTranslator(qt_traductor)

dialogo = Dialogo()
dialogo.show()
app.exec_()
