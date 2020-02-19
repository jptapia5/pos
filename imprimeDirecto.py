import tempfile
import win32api
import win32print

filename = tempfile.mktemp (".txt")
open (filename, "w").write ("This is a test")
win32api.ShellExecute (
  0,
  "printto",
  filename,
  '"%s"' % win32print.GetDefaultPrinter (),
  ".",
  0
)
