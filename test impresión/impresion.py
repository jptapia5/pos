import sys
import win32print
import win32ui
import win32con
import barcode

# how about a font?  Lucida Cons




dc = win32ui.CreateDC()             # create a dc (Device Context) object (actually a PyCDC)
dc.CreatePrinterDC("3NSTART")       # define la impresora a usar segun nombre que tiene en windows
# you need to set the map mode mainly so you know how
# to scale your output.  I do everything in points, so setting
# the map mode as "twips" works for me.
dc.SetMapMode(win32con.MM_TWIPS)  # 1440 per inch
# here's that scaling I mentioned:
scale_factor = 20  # i.e. 20 giros al punto
dc.StartDoc("TICKET DE VENTA POS")          # INICIA LA IMPRESION DEL DOCUMENTO. ESTE ES UN STRIG QUE SE MUESTRA EN LA COLA DE IMRPESIÓN.
# para dibujar algo necesitas un lapiz. Las variables son estilo de pluma, ancho de pluma y color de pluma.
pen = win32ui.CreatePen(0, int(scale_factor), 0)
# SelectObject is used to apply a pen or font object to a dc.
dc.SelectObject(pen)
font = win32ui.CreateFont({
    "name": "Lucida Console",
    "height": int(scale_factor * 7),               # tamaño de la letra
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



crear_ean13("123456789012", "ean13")
crear_isbn13("978123456", "isbn13")
crear_code39("123456789012", "code39")








dc.StartPage()
dc.TextOut(scale_factor * 0, 10 * scale_factor * 0,
    "<**********************************************>")  # 49 caracteres
dc.EndPage()



# for completeness, I'll draw a line.
# from x = "1", y = "1"
#dc.MoveTo((scale_factor * 72, scale_factor * -72))
dc.MoveTo((scale_factor * 0, scale_factor * 0))
# to x = 6", y = 3"
#dc.LineTo((scale_factor * 6 * 72, scale_factor * 3 * -72))
dc.LineTo((scale_factor * 72 * 10, scale_factor * 0))
# must not forget to tell Windows we're done.
dc.EndDoc()
