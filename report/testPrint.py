import tempfile
import win32api
import win32print

filename = tempfile.mktemp (".txt")
texto =" ESTE ES MI ARCHIVO DE IMPRESION" + "ESTE ES EL CUERPO DEL TEXTO"


open (filename, "w").write (texto)
win32api.ShellExecute (
  0,
  "print",
  filename,
  "aaaaaaaaa"
   #If this is None, the default printer will
   #be used anyway.

  '/d:"%s"' % win32print.GetDefaultPrinter (),
  ".",
  0
)
