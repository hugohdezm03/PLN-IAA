##### Inteligencia Artificial Avanzada
##### Hugo Hernández Martín (alu0101481227)

import nltk
import string
import emoji
import re

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


# def CreacionVocabulario(textoLeido):
#   separador = ' '
#   cadenaTexto = separador.join(textoLeido)
#   minusculas = cadenaTexto.lower()
#   translate_table = dict((ord(char), ' ') for char in string.punctuation)
#   sinPuntuacion = minusculas.translate(translate_table)
#   tokens = word_tokenize(sinPuntuacion)
#   stop_words = set(stopwords.words('english'))
#   # tokens = [word for word in tokens if (word not in stop_words and word.isalpha())]
#   # tokens = [word for word in tokens if (word not in stop_words)]

#   # patron = r"[^\x00-\x7F]" # Elimina los caracteres ASCII no imprimibles
#   caracteresNoImprimibles = set(chr(i) for i in range(0, 32))
#   caracteresNoImprimibles.add(chr(127))
#   for word in tokens:
#     if word not in stop_words:
#       # if not word.isprintable(): # Elimina los caracteres ASCII no imprimibles
#       #   tokens.remove(word)
#       if emoji.is_emoji(word): # Elimina los emojis
#         # print(word)
#         tokens.remove(word)
#         tokens.append(emoji.demojize(word))
      
#   return list(set(tokens))

def CreacionVocabulario(textoLeido):
  separador = ' '
  cadenaTexto = separador.join(textoLeido)
  minusculas = cadenaTexto.lower()
  translate_table = dict((ord(char), ' ') for char in string.punctuation)
  sinPuntuacion = minusculas.translate(translate_table)
  tokens = word_tokenize(sinPuntuacion)
  stop_words = set(stopwords.words('english'))

  # remove duplicates
  tokens = list(set(tokens))
  noImprimible = re.compile(r'[^\x20-\x7E]+')
  link = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
  etiquetaHTML = re.compile(r'<[^>]+>')
  numero = re.compile(r'\d+')

  for word in tokens:
    if word in stop_words:
      tokens.remove(word)
      continue
    if emoji.is_emoji(word):
      transformedToken = emoji.demojize(word)
      tokens.remove(word)
      tokens.append(transformedToken)
      print('Emoji: ' + word + ' -> ' + transformedToken)
      continue
    if noImprimible.search(word) or link.search(word) or etiquetaHTML.search(word):
      tokens.remove(word)
  return tokens
    

def main():
  print('Analizando vocabulario')
  lecturaFichero = LecturaFichero()
  tokens = CreacionVocabulario(lecturaFichero[0])
  tokens.sort()
  # ficheroEscritura = open('vocabulario.txt', 'w')
  ficheroEscritura = open('vocabulario_prueba_2.txt', 'w')
  ficheroEscritura.write('Número de tokens: ' + str(len(tokens)) + '\n')
  for token in tokens:
    ficheroEscritura.write(token + '\n')
  ficheroEscritura.close()
  

if __name__ == "__main__":
  main()
  