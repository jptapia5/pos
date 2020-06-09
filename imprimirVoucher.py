import win32api
import win32print

archivo =  ("voucher.txt")
impresora =  ("POS-PRINTER")
#open (archivo)
#win32api.ShellExecute (0,"printto",archivo, win32print.GetDefaultPrinter(),".",0)


def win_print(archivo, impresora = None):
    if not impresora:
        impresora = win32print.GetDefaultPrinter()
    out = '/d:"%s"' % (impresora)
    win32api.ShellExecute(0, "print", archivo, out, ".", 0)

def test_print():
    win_print('voucher.txt')

if __name__ == '__main__':
    test_print()