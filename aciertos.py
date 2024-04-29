##### Inteligencia Artificial Avanzada
##### Hugo Hernández Martín (alu0101481227)

import pln

def main():
  ficheroClasesEsperadas = input('Introduce el nombre del fichero con las clases esperadas (por defecto PH_train.csv): ') or 'PH_train.csv'
  clasesEsperadas = pln.LecturaFichero(ficheroClasesEsperadas)[1]
  ficheroResumen = input('Introduce el nombre del fichero con el resumen de los resultados (por defecto resumen_alu0101481227.csv): ') or 'resumen_alu0101481227.csv'
  resumenResultados = open('resumen_alu0101481227.csv')
  clasesObtenidas = resumenResultados.read().split('\n')
  
  # print(clasesEsperadas[0:10])

  for i in range(len(clasesEsperadas)):
    if clasesEsperadas[i] == 'Safe Email':
      clasesEsperadas[i] = 'S'
    else:
      clasesEsperadas[i] = 'P'
  
  # print(clasesEsperadas[0:10])

  contador_errores = 0
  for i in range(len(clasesEsperadas)):
    if clasesEsperadas[i] != clasesObtenidas[i]:
      contador_errores += 1
  print('Errores: ' + str(contador_errores))
  porcentajeError = contador_errores / len(clasesEsperadas) * 100
  print('Porcentaje de error: ' + str(porcentajeError) + '%' )
  print('Porcentaje de aciertos: ' + str(100 - porcentajeError) + '%')


if __name__ == "__main__":
  main()