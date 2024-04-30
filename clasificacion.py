##### Inteligencia Artificial Avanzada
##### Hugo Hernández Martín (alu0101481227)

import pln
import ficheros as f
import math

## Función que lee un modelo de lenguaje
## Retorna:
## - Número de correos del corpus
## - Número de palabras del corpus
## - Mapa de palabras con su logaritmo de probabilidad
def lecturaModeloLenguaje(nombreFichero):
  fichero = open(nombreFichero)
  lineas = fichero.read()
  lineas = lineas.split('\n')
  # print(len(lineas))
  
  numeroCorreos = int(lineas[0].split()[-1])
  numeroPalabras = int(lineas[1].split()[-1])
  lineas = lineas[2:]
  palabraProbabilidad = {}
  for linea in lineas:
    aux = linea.split() # Separa por espacios
    palabra = aux[1]
    probabilidad = float(aux[-1])
    palabraProbabilidad[palabra] = probabilidad

  # print(numeroCorreos)
  # print(numeroPalabras)
  # print(len(palabraProbabilidad))
  return [numeroCorreos, numeroPalabras, palabraProbabilidad]

def main():
  corpusClasificar = input('Introduce el nombre del fichero a clasificar (por defecto PH_train_sin_clases.csv): ') or 'PH_train_sin_clases.csv'
  print(corpusClasificar)

  ############## SEGÚN EL FORMATO DEL FICHERO DE CLASES ESPERADAS ################
  lecturaFichero = f.leerFicheroSinClase(corpusClasificar)    # Fichero con ';' como separador
  # lecturaFichero = f.leerFicheroSinClaseCsv(corpusClasificar)   # Fichero CSV (';' como separador y una línea para cada entrada)

  print('Fichero leído con ' + str(len(lecturaFichero)) + ' correos.')

  nombreModeloPhishing = input('Introduce el nombre del fichero con el modelo de lenguaje de phishing (por defecto modelo_lenguaje_P.txt): ') or 'modelo_lenguaje_P.txt'
  nombreModeloSafe = input('Introduce el nombre del fichero con el modelo de lenguaje de correos seguros (por defecto modelo_lenguaje_S.txt): ') or 'modelo_lenguaje_S.txt'

  modeloLenguajePhishing = lecturaModeloLenguaje(nombreModeloPhishing)
  modeloLenguajeSafe = lecturaModeloLenguaje(nombreModeloSafe)

  probabilidadesPhishing = modeloLenguajePhishing[2]
  probabilidadesSafe = modeloLenguajeSafe[2]

  probabilidadPhishing = math.log(modeloLenguajePhishing[0] / (modeloLenguajePhishing[0] + modeloLenguajeSafe[0]))
  probabilidadSafe = math.log(modeloLenguajeSafe[0] / (modeloLenguajePhishing[0] + modeloLenguajeSafe[0]))

  print('Clasificando los correos...')

  caracteres = []
  probabilidadCorreoPhishing = []
  probabilidadCorreoSafe = []
  clasificacion = []

  for correo in lecturaFichero:
    caracteres.append(correo[0:10])
    tokens = pln.Procesado([correo], False)
    probabilidadP = probabilidadPhishing
    probabilidadS = probabilidadSafe

    for token in tokens:
      if token in probabilidadesPhishing:
        # Como el modelo de lenguaje es sobre el mismo vocabulario, no es necesario comprobar si está en el otro
        probabilidadP += probabilidadesPhishing[token]
        probabilidadS += probabilidadesSafe[token]
      else:
        probabilidadP += probabilidadesPhishing['<UNK>']
        probabilidadS += probabilidadesSafe['<UNK>']

    probabilidadCorreoPhishing.append(probabilidadP)
    probabilidadCorreoSafe.append(probabilidadS)

    if (probabilidadS > probabilidadP):
      clasificacion.append('S')
    else:
      clasificacion.append('P')
  
  print('Clasificación terminada.')
  print('Guardando clasificación en fichero...')

  ficheroDetallado = open('clasificacion_alu0101481227.csv', 'w')
  ficheroResumido = open('resumen_alu0101481227.csv', 'w')

  for posicion in range(len(clasificacion)):
    lineaDetallada = caracteres[posicion] + ',' + str(round(probabilidadCorreoSafe[posicion], 2))
    lineaDetallada += ',' + str(round(probabilidadCorreoPhishing[posicion], 2)) + ',' + clasificacion[posicion] + '\n'
    ficheroDetallado.write(lineaDetallada)
    ficheroResumido.write(clasificacion[posicion] + '\n')
  ficheroDetallado.close()
  ficheroResumido.close()
  

if __name__ == "__main__":
  main()