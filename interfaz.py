import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from funcional import obtener_palabras, contar_frecuencia, palabras_frecuentes, resumen_basico
from logico import buscar_patron, cumple_regla_vocal, evaluar_calidad_texto
from utils import graficar_frecuencia, guardar_resultado
import json

def iniciar_interfaz():
    def analizar_texto():
        texto = entrada.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Advertencia", "Por favor ingrese un texto.")
            return
        
        palabras = obtener_palabras(texto)
        frecuencias = contar_frecuencia(palabras)
        top = palabras_frecuentes(frecuencias)
        resumen = resumen_basico(texto, top)
        
        palabra_buscar = patron_entry.get().strip()
        aparece = buscar_patron(palabras, palabra_buscar) if palabra_buscar else "No ingresada"
        vocales = cumple_regla_vocal(palabras)
        
        evaluacion_calidad = evaluar_calidad_texto(texto, palabras)
        
        salida.delete("1.0", tk.END)
        salida.insert(tk.END, "=== ANÁLISIS DE TEXTO ===\n\n")
        salida.insert(tk.END, f"Total de palabras: {len(palabras)}\n")
        salida.insert(tk.END, f"Palabras únicas: {len(frecuencias)}\n")
        salida.insert(tk.END, f"Diversidad léxica: {len(frecuencias)/len(palabras):.2%}\n\n")
        
        salida.insert(tk.END, "=== FRECUENCIAS ===\n")
        salida.insert(tk.END, f"{frecuencias}\n\n")
        
        salida.insert(tk.END, "=== TOP 10 PALABRAS ===\n")
        for i, (palabra, freq) in enumerate(top, 1):
            salida.insert(tk.END, f"{i}. {palabra}: {freq}\n")
        
        salida.insert(tk.END, f"\n=== BÚSQUEDA DE PATRÓN ===\n")
        salida.insert(tk.END, f"Palabra buscada: '{palabra_buscar}'\n")
        salida.insert(tk.END, f"¿Aparece? -> {aparece}\n")
        
        salida.insert(tk.END, f"\n=== REGLAS LÓGICAS ===\n")
        salida.insert(tk.END, f"¿Palabras que empiezan con vocal? -> {vocales}\n")
        
        salida.insert(tk.END, f"\n=== EVALUACIÓN DE CALIDAD ===\n")
        for regla, resultado in evaluacion_calidad.items():
            if regla != "puntuacion_calidad":
                estado = "✓" if resultado else "✗"
                salida.insert(tk.END, f"{estado} {regla}: {resultado}\n")
        
        salida.insert(tk.END, f"\nPuntuación de calidad: {evaluacion_calidad['puntuacion_calidad']:.2%}\n")
        salida.insert(tk.END, f"Calidad general: {evaluacion_calidad['calidad']}\n")
        
        salida.insert(tk.END, "\n=== RESUMEN BÁSICO ===\n")
        for r in resumen:
            salida.insert(tk.END, f"• {r}\n")

        # Guardar resultados
        guardar_resultado({
            "total_palabras": len(palabras),
            "palabras_unicas": len(frecuencias),
            "frecuencia": frecuencias,
            "palabras_top": top,
            "patron": palabra_buscar,
            "aparece": aparece,
            "tiene_vocales": vocales,
            "evaluacion_calidad": evaluacion_calidad,
            "resumen": resumen
        })

    def mostrar_grafico():
        texto = entrada.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Advertencia", "Ingrese un texto primero.")
            return
        palabras = obtener_palabras(texto)
        frecuencias = contar_frecuencia(palabras)
        graficar_frecuencia(frecuencias)

    def cargar_csv():
        archivo = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if archivo:
            try:
                import pandas as pd
                df = pd.read_csv(archivo)
                
                # Asumir que la primera columna contiene texto
                columna_texto = df.columns[0]
                textos = df[columna_texto].fillna("").astype(str)
                texto_combinado = " ".join(textos)
                
                entrada.delete("1.0", tk.END)
                entrada.insert(tk.END, texto_combinado[:5000])  # Primeros 5000 caracteres
                
                messagebox.showinfo("Éxito", f"CSV cargado. Se mostraron los primeros 5000 caracteres.\nTotal: {len(texto_combinado)} caracteres")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar CSV: {str(e)}")

    def limpiar_interfaz():
        entrada.delete("1.0", tk.END)
        salida.delete("1.0", tk.END)
        patron_entry.delete(0, tk.END)

    root = tk.Tk()
    root.title("Analizador de Texto Multiparadigma - v2.0")
    root.geometry("1000x750")
    root.configure(bg="#f0f0f0")

    # Marco superior para instrucciones
    marco_instrucciones = tk.Frame(root, bg="#1e3a8a")
    marco_instrucciones.pack(fill=tk.X, padx=0, pady=0)
    
    tk.Label(
        marco_instrucciones, 
        text="ANALIZADOR DE TEXTO INTELIGENTE - Programación Multiparadigma",
        font=("Segoe UI", 14, "bold"),
        bg="#1e3a8a",
        fg="white"
    ).pack(pady=8)

    # Marco principal
    marco_principal = tk.Frame(root, bg="#f0f0f0")
    marco_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Sección izquierda (entrada)
    tk.Label(marco_principal, text="Ingrese el texto a analizar:", font=("Segoe UI", 11, "bold"), bg="#f0f0f0").pack(anchor=tk.W)
    entrada = tk.Text(marco_principal, height=10, width=70, font=("Courier", 9), wrap=tk.WORD)
    entrada.pack(fill=tk.BOTH, expand=True, pady=5)

    # Marco de búsqueda
    marco_busqueda = tk.Frame(marco_principal, bg="#f0f0f0")
    marco_busqueda.pack(fill=tk.X, pady=5)
    
    tk.Label(marco_busqueda, text="Buscar palabra clave:", font=("Segoe UI", 10), bg="#f0f0f0").pack(side=tk.LEFT)
    patron_entry = tk.Entry(marco_busqueda, width=30, font=("Segoe UI", 10))
    patron_entry.pack(side=tk.LEFT, padx=5)

    # Marco de botones
    marco_botones = tk.Frame(marco_principal, bg="#f0f0f0")
    marco_botones.pack(fill=tk.X, pady=10)
    
    tk.Button(
        marco_botones, 
        text="Analizar Texto", 
        command=analizar_texto, 
        bg="#1e3a8a", 
        fg="white",
        font=("Segoe UI", 10, "bold"),
        padx=15,
        pady=8
    ).pack(side=tk.LEFT, padx=5)
    
    tk.Button(
        marco_botones, 
        text="Mostrar Gráfico", 
        command=mostrar_grafico, 
        bg="#0369a1", 
        fg="white",
        font=("Segoe UI", 10, "bold"),
        padx=15,
        pady=8
    ).pack(side=tk.LEFT, padx=5)
    
    tk.Button(
        marco_botones, 
        text="Cargar CSV", 
        command=cargar_csv, 
        bg="#059669", 
        fg="white",
        font=("Segoe UI", 10, "bold"),
        padx=15,
        pady=8
    ).pack(side=tk.LEFT, padx=5)
    
    tk.Button(
        marco_botones, 
        text="Limpiar", 
        command=limpiar_interfaz, 
        bg="#dc2626", 
        fg="white",
        font=("Segoe UI", 10, "bold"),
        padx=15,
        pady=8
    ).pack(side=tk.LEFT, padx=5)

    # Sección de salida
    tk.Label(marco_principal, text="Resultados del análisis:", font=("Segoe UI", 11, "bold"), bg="#f0f0f0").pack(anchor=tk.W, pady=(10, 0))
    salida = tk.Text(marco_principal, height=15, width=90, font=("Courier", 9), wrap=tk.WORD, bg="white")
    salida.pack(fill=tk.BOTH, expand=True, pady=5)

    # Marco de información
    marco_info = tk.Frame(root, bg="#dbeafe")
    marco_info.pack(fill=tk.X, padx=0, pady=0)
    
    tk.Label(
        marco_info,
        text="Los resultados se guardan automáticamente en resultado.json | Soporta: Análisis Funcional, Reglas Lógicas, Estadísticas Avanzadas",
        font=("Segoe UI", 9),
        bg="#dbeafe",
        fg="#1e40af"
    ).pack(pady=5)

    root.mainloop()
