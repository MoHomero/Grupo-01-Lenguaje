# 🔹 Buscar palabra clave
def buscar_patron(palabras, patron):
    return patron.lower() in palabras

# 🔹 Regla lógica: palabras que comienzan con vocal
def cumple_regla_vocal(palabras):
    return any(p[0].lower() in 'aeiou' for p in palabras)

# Regla: Palabras que comienzan con consonante
def cumple_regla_consonante(palabras):
    consonantes = "bcdfghjklmnñpqrstvwxyz"
    return any(p[0].lower() in consonantes for p in palabras if p)

# Regla: Longitud mínima de palabras
def cumple_regla_longitud_minima(palabras, minimo=3):
    return any(len(p) >= minimo for p in palabras)

# Regla: Densidad de palabra clave
def cumple_regla_densidad_palabra(palabras, palabra_clave, minimo_densidad=0.01):
    if not palabras:
        return False
    
    ocurrencias = sum(1 for p in palabras if p == palabra_clave.lower())
    densidad = ocurrencias / len(palabras)
    return densidad >= minimo_densidad

# Regla: Repetición de palabras
def cumple_regla_repeticion(palabras, max_repeticiones=5):
    from collections import Counter
    contador = Counter(palabras)
    return any(freq > max_repeticiones for freq in contador.values())

# Regla: Palabras en rango de frecuencia
def cumple_regla_rango_frecuencia(frecuencias, minimo=2, maximo=50):
    return any(minimo <= freq <= maximo for freq in frecuencias.values())

# Regla: Cantidad mínima de palabras únicas
def cumple_regla_diversidad_minima(palabras, minimo_unicas=20):
    return len(set(palabras)) >= minimo_unicas

# Regla: Coherencia temática (múltiples palabras relacionadas)
def cumple_regla_coherencia_tematica(palabras, palabras_tema):
    set_palabras = set(palabras)
    coincidencias = sum(1 for pt in palabras_tema if pt in set_palabras)
    return coincidencias >= 3

# Regla: Presencia de palabras específicas (como académicas)
def cumple_regla_lenguaje_academico(palabras):
    palabras_academicas = {
        'investigación', 'estudio', 'análisis', 'metodología',
        'conclusión', 'hipótesis', 'resultado', 'evidencia',
        'demostración', 'teoría', 'concepto', 'definición',
        'modelo', 'framework', 'enfoque', 'perspectiva'
    }
    set_palabras = set(palabras)
    return any(pa in set_palabras for pa in palabras_academicas)

# Motor de Inferencia: Combina múltiples reglas
def evaluar_calidad_texto(texto, palabras):

    from funcional import contar_frecuencia
    
    frecuencias = contar_frecuencia(palabras)
    
    evaluacion = {
        "tiene_vocales": cumple_regla_vocal(palabras),
        "tiene_consonantes": cumple_regla_consonante(palabras),
        "longitud_adecuada": cumple_regla_longitud_minima(palabras, 3),
        "diversidad_suficiente": cumple_regla_diversidad_minima(palabras, 20),
        "lenguaje_academico": cumple_regla_lenguaje_academico(palabras),
        "sin_excesiva_repeticion": not cumple_regla_repeticion(palabras, 10),
    }
    
    # Calcular puntuación
    puntuacion = sum(1 for v in evaluacion.values() if v) / len(evaluacion)
    evaluacion["puntuacion_calidad"] = puntuacion
    evaluacion["calidad"] = "Alta" if puntuacion >= 0.7 else "Media" if puntuacion >= 0.4 else "Baja"
    
    return evaluacion
