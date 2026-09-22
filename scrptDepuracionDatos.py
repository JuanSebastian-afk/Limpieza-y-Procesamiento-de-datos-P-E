import pandas as pd
import numpy as np

# 1. Cargar el conjunto de datos 
# df = pd.read_excel("Consolidado_Agricola.xlsx")
df = pd.read_csv("Consolidado_agrícola_por_municipios_de_los_cultivos_permanentes_del_Valle_del_Cauca_20260922")

print("--- 1. DIAGNÓSTICO INICIAL ---")
print(f"Número total de filas iniciales: {len(df)}")
print(f"Número total de columnas: {len(df.columns)}")
print("\nTipos de datos detectados por Pandas:")
print(df.dtypes)

print("\n--- 2. CONTEO DE VALORES FALTANTES (NULOS) ---")
nulos = df.isnull().sum()
porcentaje_nulos = (nulos / len(df)) * 100
tabla_nulos = pd.DataFrame({'Nulos': nulos, 'Porcentaje (%)': porcentaje_nulos})
print(tabla_nulos[tabla_nulos['Nulos'] > 0])

print("\n--- 3. DETECCIÓN DE DUPLICADOS ---")
duplicados = df.duplicated().sum()
print(f"Filas duplicadas encontradas: {duplicados}")

# =========================================================
# PROCESO DE LIMPIEZA Y PREPROCESAMIENTO
# =========================================================

df_clean = df.copy()

# A. Normalización de nombres de columnas
df_clean.columns = df_clean.columns.str.strip().str.lower().str.replace(' ', '_')

# B. Eliminar filas duplicadas
if duplicados > 0:
    df_clean = df_clean.drop_duplicates()
    print(f"\n[OK] Se eliminaron {duplicados} filas duplicadas.")

# C. Estandarización de variables cualitativas (texto)
cols_texto = ['tipo_cultivo', 'municipio', 'cultivo', 'ciclo']
for col in cols_texto:
    if col in df_clean.columns:
        df_clean[col] = df_clean[col].astype(str).str.strip().str.lower()

# D. Conversión y corrección de 'rendimiento_toneladas' (que viene como texto en datos.gov.co)
col_rend = [c for c in df_clean.columns if 'rendimiento' in c][0]
if df_clean[col_rend].dtype == 'object':
    # Reemplazar comas por puntos y convertir a numérico
    df_clean[col_rend] = df_clean[col_rend].astype(str).str.replace(',', '.')
    df_clean[col_rend] = pd.to_numeric(df_clean[col_rend], errors='coerce')
    print(f"[OK] Variable '{col_rend}' convertida con éxito a tipo numérico (float64).")

# E. Validación de Inconsistencias Lógicas Agrícolas
# 1. Hectáreas cosechadas no pueden ser mayores a las sembradas
incoherencia_hectareas = df_clean['hectareas_cosechadas'] > df_clean['hectareas_sembradas']
print(f"\nInconsistencias donde Cosechadas > Sembradas: {incoherencia_hectareas.sum()}")

# 2. Corregir/Filtrar registros con inconsistencias críticas
# Se descartan registros donde las hectáreas cosechadas superen a las sembradas por errores de digitación
df_clean = df_clean[~incoherencia_hectareas]

# F. Recálculo verificado del rendimiento (Producción / Hectáreas cosechadas)
# Para evitar divisiones por cero en hectáreas cosechadas = 0:
df_clean['rendimiento_calculado'] = np.where(
    df_clean['hectareas_cosechadas'] > 0,
    df_clean['produccion_toneladas'] / df_clean['hectareas_cosechadas'],
    0
)

# G. Tratar valores vacíos/nulos restantes
df_clean = df_clean.dropna()

print("\n--- RESUMEN FINAL DE LA LIMPIEZA ---")
print(f"Filas resultantes en la base limpia: {len(df_clean)}")
print(f"Filas depuradas/eliminadas en total: {len(df) - len(df_clean)}")

# Exportar dataset limpio
df_clean.to_csv("datos_agricolas_limpios.csv", index=False)
print("\n[ÉXITO] Archivo 'datos_agricolas_limpios.csv' guardado correctamente.")