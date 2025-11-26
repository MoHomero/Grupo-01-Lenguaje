import json
import matplotlib.pyplot as plt

# 🔹 Guardar resultados en JSON
def guardar_resultado(resultados, archivo="resultado.json"):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=4)
    print(f"✅ Resultados guardados en {archivo}")

# 🔹 Gráfico de frecuencia de palabras
def graficar_frecuencia(frecuencias):
    palabras = list(frecuencias.keys())[:10]
    valores = list(frecuencias.values())[:10]
    plt.figure(figsize=(8, 4))
    plt.bar(palabras, valores)
    plt.title("Palabras más frecuentes")
    plt.xlabel("Palabras")
    plt.ylabel("Frecuencia")
    plt.show()
