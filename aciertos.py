##### Inteligencia Artificial Avanzada
##### Hugo Hernández Martín (alu0101481227)

import pln

def main():
  clasesEsperadas = pln.LecturaFichero('PH_train.csv')[1]
  resumenResultados = open('resumen_alu0101481227.csv')
  clasesObtenidas = resumenResultados.read().split('\n')
  
  print(clasesEsperadas[0:10])

  for i in range(len(clasesEsperadas)):
    if clasesEsperadas[i] == 'Safe Email':
      clasesEsperadas[i] = 'S'
    else:
      clasesEsperadas[i] = 'P'
  
  print(clasesEsperadas[0:10])

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