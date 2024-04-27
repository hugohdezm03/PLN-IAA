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
from nltk.stem import PorterStemmer


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

def CreacionCorpusSeparados():
  lecturaFichero = LecturaFichero()

  safe = []
  phishing = []

  for i in range(len(lecturaFichero[1])):
    if lecturaFichero[1][i] == 'Safe Email':
      safe.append([str(i), lecturaFichero[0][i], lecturaFichero[1][i]])
    else:
      phishing.append([str(i), lecturaFichero[0][i], lecturaFichero[1][i]])
  ficheroEscrituraSafe = open('corpusS.txt', 'w')
  ficheroEscrituraPhishing = open('corpusP.txt', 'w')

  ficheroEscrituraSafe.write('Number;EmailText;EmailType;\n')
  ficheroEscrituraPhishing.write('Number;EmailText;EmailType;\n')

  for [numero, correo, tipo] in safe:
    ficheroEscrituraSafe.write(numero + ';' + correo + ';' + tipo + ';\n')
  for [numero, correo, tipo] in phishing:
    ficheroEscrituraPhishing.write(numero + ';' + correo + ';' + tipo + ';\n')
  ficheroEscrituraSafe.close()
  ficheroEscrituraPhishing.close()

def CreacionVocabulario(textoLeido, eliminarRepetidos = True):
  separador = ' '
  cadenaTexto = separador.join(textoLeido)
  minusculas = cadenaTexto.lower()
  translate_table = dict((ord(char), ' ') for char in string.punctuation)
  sinPuntuacion = minusculas.translate(translate_table)
  tokens = word_tokenize(sinPuntuacion)
  stop_words = set(stopwords.words('english'))

  # remove duplicates
  if eliminarRepetidos:
    tokens = list(set(tokens))
  
  # noImprimible = re.compile(r'[^\x20-\x7E]+')
  # link = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
  # etiquetaHTML = re.compile(r'<[^>]+>')

  vocabulario = []
  for word in tokens:
    if word.isalpha():
      if word in stop_words:
        continue
      vocabulario.append(word)
    else:
      if emoji.is_emoji(word):
        transformedToken = emoji.demojize(word)
        vocabulario.append(transformedToken)
        continue
      if word.isnumeric():
        vocabulario.append('<numero' + str(len(word)) + '>')
      else:
        vocabulario.append('<alfanumerico' + str(len(word)) + '>')

  # stemming
  stemmer = PorterStemmer()
  vocabulario = [stemmer.stem(t) for t in vocabulario]

  # remove duplicates
  if eliminarRepetidos:
    vocabulario = list(set(vocabulario))
    vocabulario.append('<UNK>')
  
  return vocabulario

  # # stemming
  # stemmer = PorterStemmer()
  # tokens = [stemmer.stem(t) for t in tokens]

  # if eliminarRepetidos:
  #   # remove duplicates
  #   tokens = list(set(tokens))
  
  # return tokens


def generarModeloLenguaje(vocabulario, nombreCorpus = 'corpus-safe.csv', minimoContador = 1):
  corpusLeido = LecturaFichero(nombreCorpus)
  corpusProcesado = CreacionVocabulario(corpusLeido[0], False)
  corpusProcesado.sort()
  informacion = []

  print(len(vocabulario))

  mapaPalabras = {}
  for palabra in corpusProcesado:
    if palabra in mapaPalabras:
      mapaPalabras[palabra] += 1
    else:
      mapaPalabras[palabra] = 1
  
  for token in vocabulario:
    if token in mapaPalabras:
      informacion.append([token, mapaPalabras[token]])
    else:
      informacion.append([token, 0])

  nombreFicheroEscritura = nombreCorpus.split('.')[0] + '-modeloLenguaje.txt'
  ficheroEscritura = open(nombreFicheroEscritura, 'w')

  for [token, contadorPalabra] in informacion:
    ficheroEscritura.write(token + ' ' + str(contadorPalabra) + '\n')
  ficheroEscritura.close()

  
def main():
  print('0 - Generar vocabulario')
  print('1 - Separar corpus en safe y phishing')
  print('2 - Generar modelos de lenguaje')
  print('3 - Clasificar correos')
  print('4 - Salir')

  opcion = input('Opción introducida: ')
  if opcion == '0':
    print('Analizando vocabulario')
    lecturaFichero = LecturaFichero()
    tokens = CreacionVocabulario(lecturaFichero[0])
    tokens.sort()
    # ficheroEscritura = open('vocabulario.txt', 'w')
    ficheroEscritura = open('vocabulario.txt', 'w')
    ficheroEscritura.write('Número de palabras: ' + str(len(tokens)) + '\n')
    for token in tokens:
      ficheroEscritura.write(token + '\n')
    ficheroEscritura.close()
  elif opcion == '1':
    print('Separando corpus en safe y phishing')
    CreacionCorpusSeparados()
  elif opcion == '2':
    print('Generando modelos de lenguaje')
    archivoVocabulario = open('vocabulario_prueba.txt')
    vocabulario = archivoVocabulario.read()
    vocabulario = vocabulario.split('\n')[1:]
    # generarModeloLenguaje(vocabulario, 'prueba.csv')
    generarModeloLenguaje(vocabulario, 'corpus-safe.csv')
    generarModeloLenguaje(vocabulario, 'corpus-phishing.csv')
  elif opcion == '3':
    print('Clasificando correos')
  elif opcion == '4':
    print('Saliendo del programa')
  

if __name__ == "__main__":
  main()