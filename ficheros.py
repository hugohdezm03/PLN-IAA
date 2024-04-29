##### Inteligencia Artificial Avanzada
##### Hugo Hernández Martín (alu0101481227)
##### Funciones auxiliares para generar y leer archivos con correo y número (sin clase)

import pln

def generarFicheroSinClase(nombreFicheroLectura, nombreFicheroEscritura):
  ph_train = open(nombreFicheroLectura)
  lineasLeidas = ph_train.read()
  lineasLeidas = lineasLeidas.split(';')
  lineasLeidas = lineasLeidas[3:]
  textoCorreo = []
  control = 0
  for frase in lineasLeidas:
    if control == 1:
      textoCorreo.append(frase)
    control += 1
    control %= 3
  
  ficheroEscritura = open(nombreFicheroEscritura, 'w')
  ficheroEscritura.write('Number;EmailText;\n')
  for i in range(len(textoCorreo)):
    ficheroEscritura.write(str(i) + ';' + textoCorreo[i] + ';\n')
  ficheroEscritura.close()



def leerFicheroSinClase(nombreFichero):
  ph_train = open(nombreFichero)
  lineasLeidas = ph_train.read()
  lineasLeidas = lineasLeidas.split(';')
  lineasLeidas = lineasLeidas[2:]
  textoCorreo = []
  control = 0
  for frase in lineasLeidas:
    if control == 1:
      textoCorreo.append(frase)
    control += 1
    control %= 2
  return textoCorreo



def dividirFicheroPorLineas(nombreFichero, limiteLineas):
  lineas = pln.LecturaFichero(nombreFichero)

  fichero_escritura = open('PH_train_1.csv', 'w')
  fichero_escritura.write('Number;EmailText;EmailType;\n')
  for i in range(0, limiteLineas):
    fichero_escritura.write(str(i) + ';' + lineas[0][i] + ';' + lineas[1][i] + ';\n')
  fichero_escritura.close()
  
  fichero_escritura = open('PH_train_2.csv', 'w')
  fichero_escritura.write('Number;EmailText;EmailType;\n')
  for i in range(limiteLineas, len(lineas[0])):
    fichero_escritura.write(str(i) + ';' + lineas[0][i] + ';' + lineas[1][i] + ';\n')
  fichero_escritura.close()


def main():
  print('0 - Generar fichero sin clase')
  print('1 - Leer fichero sin clase')
  print('2 - Dividir fichero por lineas')
  opcion = input('Introduce una opción: ')
  if opcion == '0':
    nombreFicheroLectura = input('Introduce el nombre del fichero a leer: ')
    nombreFicheroEscritura = input('Introduce el nombre del fichero a escribir: ')
    generarFicheroSinClase(nombreFicheroLectura, nombreFicheroEscritura)
  elif opcion == '1':
    nombreFichero = input('Introduce el nombre del fichero a leer: ')
    print(len(leerFicheroSinClase(nombreFichero)))
  elif opcion == '2':
    nombreFichero = input('Introduce el nombre del fichero a leer: ')
    lineaDivision = int(input('Introduce el número de líneas del fichero: '))
    dividirFicheroPorLineas(nombreFichero, lineaDivision)
  else:
    print('Opción no válida.')

if __name__ == "__main__":
  main()