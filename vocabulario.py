##### Inteligencia Artificial Avanzada
##### Hugo Hernández Martín (alu0101481227)

import nltk
import string

nltk.download('stopwords')
nltk.download('punkt')

from nltk import word_tokenize
from nltk.corpus import stopwords


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


def CreacionVocabulario(textoLeido):
  separador = ' '
  cadenaTexto = separador.join(textoLeido)
  minusculas = cadenaTexto.lower()
  # translate_table = dict((ord(char), ' ') for char in string.punctuation)
  # sinPuntuacion = minusculas.translate(translate_table)
  tokens = word_tokenize(minusculas)
  stop_words = set(stopwords.words('english'))
  tokens = [word for word in tokens if (word not in stop_words and word.isalpha())]
  return list(set(tokens))
    

def main():
  print('Analizando vocabulario')
  lecturaFichero = LecturaFichero()
  tokens = CreacionVocabulario(lecturaFichero[0])
  tokens.sort()
  ficheroEscritura = open('vocabulario.txt', 'w')
  ficheroEscritura.write('Número de tokens: ' + str(len(tokens)) + '\n')
  for token in tokens:
    ficheroEscritura.write(token + '\n')
  ficheroEscritura.close()
  

if __name__ == "__main__":
  main()
  