import numpy as np
import pandas as pd
from funcional import contar_frecuencia, obtener_palabras

def obtener_estadisticas(frecuencias):
    valores = np.array(list(frecuencias.values()))
    
    if len(valores) == 0:
        return {}
    
    stats = {
        "total_palabras_unicas": len(frecuencias),
        "total_palabras": int(np.sum(valores)),
        "promedio": float(np.mean(valores)),
        "mediana": float(np.median(valores)),
        "desviacion_estandar": float(np.std(valores)),
        "varianza": float(np.var(valores)),
        "minimo": int(np.min(valores)),
        "maximo": int(np.max(valores)),
        "percentil_25": float(np.percentile(valores, 25)),
        "percentil_50": float(np.percentile(valores, 50)),
        "percentil_75": float(np.percentile(valores, 75)),
    }    
    return stats

def crear_dataframe_frecuencias(frecuencias):
    df = pd.DataFrame({
        "palabra": list(frecuencias.keys()),
        "frecuencia": list(frecuencias.values())
    })
    
    df = df.sort_values("frecuencia", ascending=False).reset_index(drop=True)
    df["frecuencia_relativa"] = df["frecuencia"] / df["frecuencia"].sum()
    df["frecuencia_acumulada"] = df["frecuencia"].cumsum()
    df["rango"] = range(1, len(df) + 1)
    
    return df
"""te toca a ti"""
def analizar_diversidad_lexical(texto):
    palabras = obtener_palabras(texto)
    palabras_unicas = len(set(palabras))
    total_palabras = len(palabras)
    
    # Type-Token Ratio
    ttr = palabras_unicas / total_palabras if total_palabras > 0 else 0
    
    # Índice de Shannon (entropía)
    frecuencias = contar_frecuencia(palabras)
    probabilidades = np.array(list(frecuencias.values())) / total_palabras
    entropía = -np.sum(probabilidades * np.log2(probabilidades + 1e-10))
    
    return {
        "total_palabras": total_palabras,
        "palabras_unicas": palabras_unicas,
        "type_token_ratio": float(ttr),
        "entropía_shannon": float(entropía),
    }

def comparar_textos(texto1, texto2):
    palabras1 = obtener_palabras(texto1)
    palabras2 = obtener_palabras(texto2)
    
    set1 = set(palabras1)
    set2 = set(palabras2)
    
    # Similitud de Jaccard
    interseccion = len(set1 & set2)
    union = len(set1 | set2)
    jaccard = interseccion / union if union > 0 else 0
    
    # Palabras en común
    palabras_comunes = list(set1 & set2)
    palabras_unicas_1 = list(set1 - set2)
    palabras_unicas_2 = list(set2 - set1)
    
    return {
        "similitud_jaccard": float(jaccard),
        "palabras_en_comun": len(palabras_comunes),
        "palabras_unicas_texto1": len(palabras_unicas_1),
        "palabras_unicas_texto2": len(palabras_unicas_2),
        "ejemplos_comunes": palabras_comunes[:10],
        "ejemplos_unicas_1": palabras_unicas_1[:10],
        "ejemplos_unicas_2": palabras_unicas_2[:10],
    }

def cargar_y_analizar_csv(archivo, columna_texto="texto"):
    df = pd.read_csv(archivo)
    
    if columna_texto not in df.columns:
        raise ValueError(f"Columna '{columna_texto}' no encontrada en CSV")
    
    textos = df[columna_texto].fillna("").astype(str)
    texto_combinado = " ".join(textos)
    
    palabras = obtener_palabras(texto_combinado)
    frecuencias = contar_frecuencia(palabras)
    
    return {
        "total_registros": len(df),
        "total_palabras": len(palabras),
        "palabras_unicas": len(frecuencias),
        "estadisticas": obtener_estadisticas(frecuencias),
        "diversidad_lexical": {
            "type_token_ratio": len(set(palabras)) / len(palabras) if palabras else 0
        }
    }
