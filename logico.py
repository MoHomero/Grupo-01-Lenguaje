"""
Módulo de Lógica: Implementa paradigma lógico con reglas e inferencias
Utiliza predicados y búsqueda de patrones para análisis de texto
"""

# 🔹 Buscar palabra clave
def buscar_patron(palabras, patron):
    return patron.lower() in palabras

# 🔹 Regla lógica: palabras que comienzan con vocal
def cumple_regla_vocal(palabras):
    return any(p[0].lower() in 'aeiou' for p in palabras)

# Regla: Palabras que comienzan con consonante
def cumple_regla_consonante(palabras):
    """
    Verifica si hay palabras que comienzan con consonante
    
    Args:
        palabras (list): Lista de palabras
    
    Returns:
        bool: True si al menos una palabra comienza con consonante
    """
    consonantes = "bcdfghjklmnñpqrstvwxyz"
    return any(p[0].lower() in consonantes for p in palabras if p)

# Regla: Longitud mínima de palabras
def cumple_regla_longitud_minima(palabras, minimo=3):
    """
    Verifica si hay palabras con longitud mínima especificada
    
    Args:
        palabras (list): Lista de palabras
        minimo (int): Longitud mínima requerida
    
    Returns:
        bool: True si existen palabras con longitud >= minimo
    """
    return any(len(p) >= minimo for p in palabras)

# Regla: Densidad de palabra clave
def cumple_regla_densidad_palabra(palabras, palabra_clave, minimo_densidad=0.01):
    """
    Verifica si una palabra clave aparece con cierta densidad
    
    Args:
        palabras (list): Lista de palabras
        palabra_clave (str): Palabra a buscar
        minimo_densidad (float): Densidad mínima requerida (0-1)
    
    Returns:
        bool: True si densidad >= minimo_densidad
    """
    if not palabras:
        return False
    
    ocurrencias = sum(1 for p in palabras if p == palabra_clave.lower())
    densidad = ocurrencias / len(palabras)
    return densidad >= minimo_densidad

# Regla: Repetición de palabras
def cumple_regla_repeticion(palabras, max_repeticiones=5):
    """
    Verifica si hay palabras muy repetidas (potencial plagio)
    
    Args:
        palabras (list): Lista de palabras
        max_repeticiones (int): Máximo de repeticiones permitidas
    
    Returns:
        bool: True si alguna palabra se repite más de max_repeticiones
    """
    from collections import Counter
    contador = Counter(palabras)
    return any(freq > max_repeticiones for freq in contador.values())

# Regla: Palabras en rango de frecuencia
def cumple_regla_rango_frecuencia(frecuencias, minimo=2, maximo=50):
    """
    Verifica si hay palabras en un rango específico de frecuencia
    
    Args:
        frecuencias (dict): Diccionario palabra -> frecuencia
        minimo (int): Frecuencia mínima
        maximo (int): Frecuencia máxima
    
    Returns:
        bool: True si existen palabras en ese rango
    """
    return any(minimo <= freq <= maximo for freq in frecuencias.values())

# Regla: Cantidad mínima de palabras únicas
def cumple_regla_diversidad_minima(palabras, minimo_unicas=20):
    """
    Verifica si el texto tiene mínima diversidad léxica
    
    Args:
        palabras (list): Lista de palabras
        minimo_unicas (int): Cantidad mínima de palabras únicas
    
    Returns:
        bool: True si palabras únicas >= minimo_unicas
    """
    return len(set(palabras)) >= minimo_unicas

# Regla: Coherencia temática (múltiples palabras relacionadas)
def cumple_regla_coherencia_tematica(palabras, palabras_tema):
    """
    Verifica si el texto contiene múltiples palabras de un tema
    
    Args:
        palabras (list): Lista de palabras del texto
        palabras_tema (list): Palabras relacionadas al tema
    
    Returns:
        bool: True si al menos 3 palabras del tema están presentes
    """
    set_palabras = set(palabras)
    coincidencias = sum(1 for pt in palabras_tema if pt in set_palabras)
    return coincidencias >= 3

# Regla: Presencia de palabras específicas (como académicas)
def cumple_regla_lenguaje_academico(palabras):
    """
    Detects if text contains academic language markers
    
    Args:
        palabras (list): Lista de palabras
    
    Returns:
        bool: True si contiene palabras académicas
    """
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
    """
    Evalúa la calidad general del texto combinando múltiples reglas
    
    Args:
        texto (str): Texto original
        palabras (list): Palabras procesadas
    
    Returns:
        dict: Evaluación de cada regla
    """
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
