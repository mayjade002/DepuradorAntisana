import pandas as pd
import os
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

# Lista de archivos CSV
archivos = [
    "P42-Antisana_Ramón_Huañuna_Precipitación-Mensual.csv",
    "P43-Antisana_Limboasi_Precipitación-Mensual.csv",
    "P55-Antisana_Diguchi_Precipitación-Mensual.csv",
    "H44-Antisana_DJ_Diguchi_Nivel_de_agua-Mensual.csv",
    "H55-Río_Antisana_AC_Nivel_de_agua-Mensual.csv"
]

ruta_entrada = "."
ruta_salida = "./archivos_limpios"
os.makedirs(ruta_salida, exist_ok=True)

# Para almacenar mensajes detallados
mensajes = []

def agregar_mensaje(texto):
    print(texto)
    mensajes.append(texto)

def depurar_archivo(nombre_archivo):
    ruta_completa = os.path.join(ruta_entrada, nombre_archivo)
    agregar_mensaje(f"\n📂 Procesando archivo: {nombre_archivo}")

    if not os.path.isfile(ruta_completa):
        agregar_mensaje(f"⚠️  Archivo no encontrado: {nombre_archivo}")
        return

    try:
        df = pd.read_csv(ruta_completa, encoding="utf-8")
        filas, columnas = df.shape
        agregar_mensaje(f"📊 Archivo cargado con {filas} filas y {columnas} columnas.")

        total_valores_antes = df.size
        columnas_numericas = df.columns[1:]
        agregar_mensaje(f"🔍 Columnas a convertir en numéricas: {list(columnas_numericas)}")

        for col in columnas_numericas:
            valores_antes = df[col].notna().sum()
            df[col] = pd.to_numeric(df[col], errors='coerce')
            valores_despues = df[col].notna().sum()
            convertidos = valores_antes - valores_despues
            agregar_mensaje(f"🔄 Columna '{col}': {convertidos} valores convertidos a NaN")

        total_valores_despues = df.size
        total_nulos = df.isna().sum().sum()

        nombre_salida = os.path.join(ruta_salida, nombre_archivo)
        df.to_csv(nombre_salida, index=False)
        agregar_mensaje(f"💾 Archivo limpio guardado en: {nombre_salida}")
        agregar_mensaje(f"✅ Total de valores antes: {total_valores_antes}, después: {total_valores_despues}, nulos: {total_nulos}")

    except Exception as e:
        agregar_mensaje(f"❌ Error al procesar {nombre_archivo}: {e}")

# Procesar todos los archivos
for archivo in archivos:
    depurar_archivo(archivo)

# Mostrar los mensajes en una ventana
def mostrar_log():
    ventana = tk.Tk()
    ventana.title("🧹 Detalle del Proceso de Depuración")
    ventana.geometry("1000x600")
    ventana.configure(bg="#f9f9f9")

    canvas = tk.Canvas(ventana, bg="#f9f9f9")
    scrollbar = tk.Scrollbar(ventana, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#f9f9f9")

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    titulo = tk.Label(scroll_frame, text="📊 Resumen detallado de la depuración", font=("Segoe UI", 16, "bold"), bg="#f9f9f9", fg="#333")
    titulo.pack(pady=(10, 10))

    archivo_actual = None
    bloque = []

    for mensaje in mensajes:
        if mensaje.startswith("\n📂 Procesando archivo:"):
            if bloque:
                mostrar_bloque(scroll_frame, archivo_actual, bloque)
                bloque = []
            archivo_actual = mensaje.replace("\n📂 Procesando archivo: ", "")
        else:
            bloque.append(mensaje)

    if archivo_actual and bloque:
        mostrar_bloque(scroll_frame, archivo_actual, bloque)

    tk.Button(scroll_frame, text="Cerrar", command=ventana.destroy, font=("Segoe UI", 10), bg="#4CAF50", fg="white", padx=15, pady=5).pack(pady=10)

    ventana.mainloop()


def mostrar_bloque(frame, nombre, datos):
    marco = tk.LabelFrame(frame, text=f"📁 {nombre}", font=("Segoe UI", 10, "bold"), padx=10, pady=5, bg="#ffffff", fg="#222")
    marco.pack(fill="x", padx=20, pady=10)

    for linea in datos:
        lbl = tk.Label(marco, text="• " + linea, anchor="w", justify="left", font=("Consolas", 9), bg="#ffffff", fg="#000000")
        lbl.pack(fill="x", anchor="w")
mostrar_log()
