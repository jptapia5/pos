archivo = open("hello.txt", “r”)
archivo.read()
archivo.close()
# read() Lee todo el archivo, pero puedes leer renglón por renglón, utilizando readlines() y simple bucle for
# para recorrer cada renglón:
archivo = open("hello.txt", “r”)
for linea in archivo.readlines():
print linea
archivo.close()
# Si quieres leer un archivo colgado en una web, debes utilizar la biblioteca urllib para abrirlo mediante
# urlopen, luego, todo se hace igual para leer el archivo.
archivo = urllib.urlopen('http: // sites.google.com/site/sugaractivities/jam/CanalesJAMediaTV?
                         attredirects=0 & d=1')
for linea in archivo.readlines():
print linea
archivo.close()
