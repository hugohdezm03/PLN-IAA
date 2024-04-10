##### Inteligencia Artificial Avanzada
##### Hugo Hernández Martín (alu0101481227)

import nltk

nltk.download('stopwords')
nltk.download('punkt')

from nltk import word_tokenize

def LecturaFichero(nombreFichero = 'PH_train.csv'):
  ph_train = open(nombreFichero)
  lineasLeidas = ph_train.read()
  lineasLeidas = lineasLeidas.split(';')
  lineasLeidas = lineasLeidas[3:]
  textoCorreo = []
  tipoCorreo = []
  control = 0
  for frase in lineasLeidas:
    if control == 1:
      textoCorreo.append(frase)
    elif control == 2:
      tipoCorreo.append(frase)
    control += 1
    control %= 3
  return [textoCorreo, tipoCorreo]


def CreacionVocabulario(TextoLeido):
  tokens = word_tokenize(TextoLeido)
  print(tokens)
    

def main():
  print('Analizando vocabulario')
  # nombreFichero = input('Introduzca el nombre del fichero a leer: ')
  lecturaFichero = LecturaFichero()
  vocabulario = CreacionVocabulario(lecturaFichero[0])
  

if __name__ == "__main__":
  main()
  