##### Inteligencia Artificial Avanzada
##### Hugo Hernández Martín (alu0101481227)

import pln
  
def main():
  corpusClasificar = input('Introduce el nombre del fichero a clasificar (por defecto PH_train.csv): ') or 'PH_train.csv'
  print(corpusClasificar)
  print('Clasificando los correos...')
  lecturaFichero = pln.LecturaFichero(corpusClasificar)
  tokens = pln.CreacionVocabulario(lecturaFichero[0])
  tokens.sort()
  # ficheroEscritura = open('vocabulario.txt', 'w')
  # ficheroEscritura.write('Número de palabras: ' + str(len(tokens)))
  # for token in tokens:
  #   ficheroEscritura.write('\n' + token)
  # ficheroEscritura.close()
  

if __name__ == "__main__":
  main()