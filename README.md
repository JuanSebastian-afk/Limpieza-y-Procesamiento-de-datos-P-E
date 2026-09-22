# Limpieza-y-Procesamiento-de-datos-P-E


## Análisis de Inconsistencias, Errores y Limpieza de Datos

Al realizar el diagnóstico del conjunto de datos "Consolidado agrícola por municipios de los cultivos permanentes del Valle del Cauca", se buscaron y corrijieron las siguientes inconsistencias y errores de digitación:

1.  **Incoherencia en Tipos de Datos de la Fuente:**
- La variable 'rendimiento_toneladas' proviene registrada en la plataforma como tipo Texto (string) en lugar de tipo Cuantitativo Continuo (float). Esto se debe a la presencia de comas (',') como separadores decimales y caracteres no numéricos en algunos registros.
- Las variables 'id_municipio' e 'id_cultivo' se encuentran almacenadas como tipo entero (int64), pero conceptualmente corresponden a códigos identificadores cualitativos nominales.

2. **Errores de Formato de Texto y Tipográficos:**
- Variaciones de capitalización (mezcla de mayúsculas y minúsculas) y presencia de espacios en blanco al inicio o al final de las cadenas de texto en variables cualitativas ('tipo_cultivo', 'municipio', 'cultivo' y 'ciclo').
- Inconsistencia en acentuaciones y caracteres especiales entre registros del mismo municipio o cultivo.

3. **Inconsistencias Lógicas y Valores Nulos/Atípicos:**
- Presencia de valores nulos o vacíos en variables operativas.
- Registros con 'hectareas_cosechadas' mayores a las 'hectareas_sembradas' o con 'hectareas_cosechadas' igual a cero pero con 'produccion_toneladas' positiva (lo cual genera indefinición matemática en la variable rendimiento).
- Filas duplicadas correspondientes al mismo municipio, cultivo y año.

**Procedimiento de Limpieza y Preprocesamiento:**
1. Normalización de Cadenas de Texto: Se transformaron todas las variables cualitativas a letras minúsculas, eliminando espacios iniciales/finales sobrantes y estandarizando caracteres especiales.
2. Corrección de Tipo de Dato: Se convirtió la columna 'rendimiento_toneladas' a formato numérico float64 previa sustitución de comas decimales por puntos.
3. Tratamiento de Nulos y Duplicados: Se eliminaron los registros completamente duplicados y se imputaron o descartaron las observaciones inconsistentes (donde las hectáreas cosechadas superaban las sembradas o donde la producción generaba división por cero).
4. Recálculo de Variable Derivada: Se recalculó de manera homogénea el rendimiento mediante la relación entre las toneladas producidas y las hectáreas cosechadas.
