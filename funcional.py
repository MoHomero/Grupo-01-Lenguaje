from functools import reduce
import re
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import pandas as pd

# Descargar datos NLTK (solo la primera vez)
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('stopwords', quiet=True)

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('spanish'))

# 🔹 Limpieza y normalización del texto
def limpiar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r'[^\w\sáéíóúñ]', '', texto)
    return texto

# 🔹 Tokenización + lematización + eliminación de stopwords
def obtener_palabras(texto):
    texto = limpiar_texto(texto)
    palabras = texto.split()
    return [lemmatizer.lemmatize(p) for p in palabras if p not in stop_words]

# 🔹 Contar frecuencia de palabras
def contar_frecuencia(palabras):
    return reduce(lambda acc, p: {**acc, p: acc.get(p, 0) + 1}, palabras, {})

# 🔹 Palabras más frecuentes
def palabras_frecuentes(frecuencias, limite=10):
    return sorted(frecuencias.items(), key=lambda x: x[1], reverse=True)[:limite]

# 🔹 Generar resumen básico (frases relevantes)
def resumen_basico(texto, top_palabras):
    oraciones = re.split(r'[.!?]', texto)
    relevantes = [o.strip() for o in oraciones if any(tp[0] in o.lower() for tp in top_palabras)]
    return [r for r in relevantes if r]

# 🔹 Obtener n-gramas
def obtener_n_gramas(palabras, n=2):
    n_gramas = [tuple(palabras[i:i+n]) for i in range(len(palabras) - n + 1)]
    return reduce(lambda acc, ng: {**acc, ng: acc.get(ng, 0) + 1}, n_gramas, {})

# 🔹 Calcular densidad de palabras clave
def calcular_densidad_palabra(texto, palabra):
    palabras = obtener_palabras(texto)
    if not palabras:
        return 0.0
    ocurrencias = sum(1 for p in palabras if p == palabra.lower())
    return ocurrencias / len(palabras)

# 🔹 Índice de Flesch-Kincaid
def indice_flesch_kincaid(palabras, oraciones):
    if not palabras or not oraciones:
        return 0.0
    
    # Contar sílabas aproximado
    silabas = sum(contar_silabas(p) for p in palabras)
    
    # Fórmula: 0.39 * (palabras/oraciones) + 11.8 * (sílabas/palabras) - 15.59
    resultado = (0.39 * (len(palabras) / len(oraciones)) + 
                 11.8 * (silabas / len(palabras)) - 15.59)
    
    return max(0, min(100, resultado))

def contar_silabas(palabra):
    palabra = palabra.lower()
    vocales = "aeiouáéíóú"
    silabas = 0
    anterior_vocal = False
    
    for letra in palabra:
        es_vocal = letra in vocales
        if es_vocal and not anterior_vocal:
            silabas += 1
        anterior_vocal = es_vocal
    
    return max(1, silabas)
