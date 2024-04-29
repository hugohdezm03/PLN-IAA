##### Inteligencia Artificial Avanzada
##### Hugo Hernández Martín (alu0101481227)

import nltk
import string
import emoji
import math
import re

nltk.download('stopwords')
nltk.download('punkt')

from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Función que lee un fichero y devuelve el texto y el tipo de correo (safe o phishing)
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

# Función que crea dos corpus separados, uno para los correos seguros y otro para los correos de phishing
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

# Función que crea un vocabulario a partir de un texto leído
# Si el segundo parámetro es True, se eliminarán las palabras repetidas
# Si el segundo parámetro es False, se mantendrán las palabras repetidas (procesamiento de corpus)
def Procesado(textoLeido, eliminarRepetidos = True):
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
        # vocabulario.append(word)
      else:
        vocabulario.append('<alfanumerico' + str(len(word)) + '>')
        # vocabulario.append('<alfanumerico>')
        # vocabulario.append(word)

  # stemming
  stemmer = PorterStemmer()
  vocabulario = [stemmer.stem(t) for t in vocabulario]

  # remove duplicates
  if eliminarRepetidos:
    vocabulario = list(set(vocabulario))
  
  return vocabulario

# Función que genera un modelo de lenguaje a partir de un vocabulario y un corpus
def generarModeloLenguaje(vocabulario, sizeVocabulario, nombreCorpus, minimoContador = 1):
  print('Generando modelo de lenguaje para el corpus ' + nombreCorpus)
  corpusLeido = LecturaFichero(nombreCorpus)
  sizeCorpus = len(corpusLeido[0])
  corpusProcesado = Procesado(corpusLeido[0], False)
  # corpusProcesado.sort()

  informacion = []
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

  nombreFicheroEscritura = 'modelo_lenguaje_' + nombreCorpus.split('.')[0][-1] + '.txt'
  ficheroEscritura = open(nombreFicheroEscritura, 'w')

  ficheroEscritura.write('Numero de documentos (noticias) del corpus: ' + str(sizeCorpus) + '\n')
  ficheroEscritura.write('Número de palabras del corpus: ' + str(len(corpusProcesado)))

  for [token, contadorPalabra] in informacion:
    resultado = '\nPalabra: ' + token
    resultado += ' Frec: ' + str(contadorPalabra)
    resultado += ' LogProb: ' + str(math.log((contadorPalabra + 1) / (len(corpusProcesado) + sizeVocabulario)))
    ficheroEscritura.write(resultado)
  ficheroEscritura.close()

  
def main():
  print('0 - Generar vocabulario')
  print('1 - Separar corpus en safe y phishing')
  print('2 - Generar modelos de lenguaje')
  print('3 - Salir')

  opcion = input('Opción introducida: ')
  if opcion == '0':
    print('Analizando vocabulario')
    lecturaFichero = LecturaFichero()
    tokens = Procesado(lecturaFichero[0])
    tokens.append('<UNK>')
    tokens.sort()
    ficheroEscritura = open('vocabulario.txt', 'w')
    ficheroEscritura.write('Número de palabras: ' + str(len(tokens)))
    for token in tokens:
      ficheroEscritura.write('\n' + token)
    ficheroEscritura.close()
  elif opcion == '1':
    print('Separando corpus en safe y phishing')
    CreacionCorpusSeparados()
  elif opcion == '2':
    print('Generando modelos de lenguaje')
    archivoVocabulario = open('vocabulario.txt')
    vocabulario = archivoVocabulario.read()
    vocabulario = vocabulario.split('\n')
    sizeVocabulario = int(vocabulario[0].split(' ')[-1])
    vocabulario = vocabulario[1:]
    generarModeloLenguaje(vocabulario, sizeVocabulario, 'corpusS.txt')
    generarModeloLenguaje(vocabulario, sizeVocabulario, 'corpusP.txt')
  elif opcion == '3':
    print('Saliendo del programa')
  

if __name__ == "__main__":
  main()