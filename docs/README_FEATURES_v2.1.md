# 🎯 Fuzzy Logic Movie Recommendation System v2.1
## Complete Feature Guide & Update Log

**Autor:** Andrés Torres Ceja  
**ID:** 148252CF  
**Curso:** Soft Computing - Universidad de Guanajuato  
**Última Actualización:** Octubre 5, 2025

---

## 🆕 NUEVAS CARACTERÍSTICAS v2.1

### ✨ Funcionalidades Agregadas

#### 1. **Generación de Datasets** (`--generate-data`)
```bash
python main.py --generate-data 100
```

**Qué hace:**
- Genera N películas de muestra (10-1000 películas)
- Exporta automáticamente en **3 formatos**:
  - `sample_movies.csv` - Para Excel, análisis
  - `sample_movies.json` - Para APIs, web apps
  - `sample_movies.xlsx` - Con estadísticas y distribución de géneros en hojas separadas
- Crea carpeta `generated_data/dataset_TIMESTAMP/`
- Incluye README.txt con resumen completo
- Muestra top 5 géneros más comunes

**Salida incluye:**
- Total de películas generadas
- Rating promedio y desviación estándar
- Rango de ratings (min-max)
- Distribución de géneros (top 10)
- Año de lanzamiento más común
- Estadísticas completas en Excel

#### 2. **Agregar Películas Personalizadas** (Menú: Opción 7)
```bash
# Modo interactivo > Opción 7
python main.py
```

**Funcionalidad:**
- Formulario interactivo para agregar películas custom
- Campos requeridos y opcionales:
  - **Título** (requerido)
  - Géneros (comma-separated)
  - Actores principales (comma-separated)
  - Rating promedio (1-10, validado)
  - Año de lanzamiento (validado)
  - Director
- Validación automática de datos
- Guarda en `data/custom_movies.csv`
- Integra inmediatamente al dataset actual
- Re-inicializa el motor con los nuevos datos

**Ejemplo de uso:**
```
Movie Title: The Matrix
Genres: Action, Sci-Fi
Main Actors: Keanu Reeves, Laurence Fishburne
Average Rating: 8.7
Release Year: 1999
Director: Wachowski Brothers
```

#### 3. **Exportación de Datasets** (Menú: Opción 8 / `--export`)
```bash
# Comando directo
python main.py --export csv
python main.py --export json
python main.py --export excel
python main.py --export all

# O desde menú interactivo
python main.py  # Opción 8
```

**Opciones:**
1. **CSV** - Compatible con Excel, Python pandas
2. **JSON** - Para APIs, JavaScript, web apps
3. **Excel** - Con 2 hojas:
   - Hoja 1: Datos completos de películas
   - Hoja 2: Estadísticas del dataset
4. **All** - Los 3 formatos simultáneamente

**La exportación incluye:**
- Timestamp en nombre de carpeta
- Todos los metadatos originales
- Estadísticas agregadas (Excel)
- Fecha y hora de exportación

#### 4. **Historial de Recomendaciones** (Menú: Opción 9)
```bash
# Ver historial desde menú
python main.py  # Opción 9
```

**Características:**
- Guarda automáticamente cada recomendación
- Almacena en `data/recommendation_history.json`
- Incluye:
  - Timestamp (fecha/hora exacta)
  - Inputs (rating, popularity, genre_match)
  - Output (recommendation score)
  - Película recomendada (si aplica)
- Muestra últimas 10 recomendaciones en tabla
- Exportación completa a JSON
- Límite: 100 recomendaciones (circular)

**Tabla de historial:**
```
+---+------------+--------+------------+-------+-------+----------+
| # | Date/Time  | Rating | Popularity | Genre | Score | Movie    |
+---+------------+--------+------------+-------+-------+----------+
| 1 | 10/05 15:30| 8.5    | 75.0       | 85.0  | 78.5  | Matrix   |
+---+------------+--------+------------+-------+-------+----------+
```

#### 5. **Gestión de Datasets** (Menú: Opción 11)
```bash
# Modo interactivo > Opción 11
python main.py
```

**Opciones del gestor:**
1. **Cargar CSV custom** - Importar tu propio dataset
2. **Ver datasets disponibles** - Lista todos los CSV en data/ y generated_data/
3. **Recargar dataset actual** - Reinicializar
4. **Ver info del dataset** - Estadísticas, memoria, duplicados

**Listado de datasets muestra:**
- Tipo (data / generated)
- Nombre de archivo
- Tamaño en KB
- Fecha de modificación
- Número total encontrado

**Información de dataset:**
```
Total Movies:       103
Columns:            title, genres, rating, year, actors...
Memory Usage:       125.3 KB
Average Rating:     8.76
Rating Std Dev:     0.89
Duplicates:         0
```

#### 6. **Batch Testing Suite** (`--batch-test`)
```bash
python main.py --batch-test
```

**Tests ejecutados:**

**A. Test de Performance:**
- 4 casos de prueba con diferentes inputs
- Mide tiempo de ejecución (ms)
- Calcula: promedio, mínimo, máximo, desviación estándar
- Valida throughput del sistema

**B. Test de Precisión:**
- Valida que inputs bajos → scores bajos
- Valida que inputs altos → scores altos
- Valida que inputs medios → scores medios
- Rangos esperados vs. reales

**C. Test de Robustez:**
- Valores mínimos (1.0, 0.0, 0.0)
- Valores máximos (10.0, 100.0, 100.0)
- Valores decimales (5.5, 55.5, 55.5)
- Extremos mixtos (1.0, 100.0, 0.0)

**Resultados en tablas:**
```
Performance Results:
  Average Time: 0.25 ms
  Min Time:     0.00 ms
  Max Time:     1.00 ms
  Std Dev:      0.43 ms

Accuracy Results:
  [OK] Low inputs → Low scores (27.4 ∈ [0, 40])
  [OK] High inputs → High scores (93.2 ∈ [70, 100])
  [OK] Medium inputs → Medium scores (40.0 ∈ [35, 65])

Robustness Results:
  [OK] All edge cases handled correctly
```

---

## 📋 MENÚ INTERACTIVO COMPLETO

```
MAIN MENU:
1.  Generate Movie Recommendations
2.  Visualize Fuzzy Logic System
3.  Analyze User Preferences
4.  View System Dashboard
5.  Explore Movie Database
6.  Test Fuzzy Inference
7.  Add Custom Movie                    ← NUEVO
8.  Export Current Dataset              ← NUEVO
9.  View Recommendation History         ← NUEVO
10. Generate Sample Dataset             ← NUEVO
11. Manage Datasets                     ← NUEVO
12. Exit
```

---

## 🚀 MODOS DE USO ACTUALIZADOS

### Modo 1: Interactivo (Predeterminado)
```bash
python main.py
```
Acceso a todas las 12 opciones del menú

### Modo 2: Demostración
```bash
python main.py --demo
```
Demo automático + visualizaciones

### Modo 3: Solo Visualizaciones
```bash
python main.py --visualize
```
Genera todas las gráficas

### Modo 4: Generación de Datos ⭐ NUEVO
```bash
python main.py --generate-data 100
```
Crea 100 películas en CSV/JSON/Excel

### Modo 5: Batch Testing ⭐ NUEVO
```bash
python main.py --batch-test
```
Ejecuta suite completa de pruebas

### Modo 6: Exportación Directa ⭐ NUEVO
```bash
python main.py --export csv
python main.py --export json
python main.py --export excel
python main.py --export all
```
Exporta dataset actual

---

## 📁 ESTRUCTURA DE CARPETAS ACTUALIZADA

```
E1_Fzz_AndresTorresCeja_148252CF/
│
├── main.py                         # ✨ v2.1 con nuevas funcionalidades
├── main_old.py                     # 📦 Backup v1.0
├── README_MODERN_UI.md             # 📖 Documentación UI v2.0
├── README_FEATURES_v2.1.md         # 📖 Esta documentación
│
├── src/
│   ├── fuzzy_logic/                # Sistema de lógica difusa
│   ├── recommender/                # Motor de recomendaciones
│   ├── ui/                         # Interfaz moderna
│   │   ├── interface.py            # UIManager
│   │   └── visualizer.py           # FuzzyVisualizer
│   └── utils/
│       └── data_loader.py
│
├── data/                           # ⭐ NUEVO: Datos persistentes
│   ├── custom_movies.csv           # Películas agregadas manualmente
│   ├── recommendation_history.json # Historial de recomendaciones
│   └── export_TIMESTAMP/           # Exportaciones
│
├── generated_data/                 # ⭐ NUEVO: Datasets generados
│   └── dataset_TIMESTAMP/
│       ├── sample_movies.csv
│       ├── sample_movies.json
│       ├── sample_movies.xlsx      # Con hojas de estadísticas
│       └── README.txt
│
├── visualizations/                 # Gráficas generadas
│   ├── membership_functions.png
│   ├── fuzzy_inference.png
│   ├── dashboard.png
│   └── data_statistics.png
│
└── docs/
    ├── ARCHITECTURE.md
    └── IMRAD.md
```

---

## 🔄 FLUJOS DE TRABAJO TÍPICOS

### Flujo 1: Investigación - Generar Datos de Prueba
```bash
# 1. Generar dataset de prueba grande
python main.py --generate-data 200

# 2. Ejecutar batch tests
python main.py --batch-test

# 3. Generar visualizaciones
python main.py --visualize

# 4. Exportar resultados
python main.py --export all
```

### Flujo 2: Uso Académico - Presentación
```bash
# 1. Generar datos
python main.py --generate-data 50

# 2. Demo automático
python main.py --demo

# 3. Los archivos están listos en:
#    - visualizations/*.png (para slides)
#    - generated_data/*.xlsx (para análisis)
```

### Flujo 3: Desarrollo - Dataset Custom
```bash
# 1. Modo interactivo
python main.py

# 2. Opción 7: Agregar películas custom
#    - Agregar The Matrix
#    - Agregar Inception
#    - Agregar Interstellar

# 3. Opción 8: Exportar dataset con películas custom

# 4. Opción 1: Generar recomendaciones

# 5. Opción 9: Ver historial
```

### Flujo 4: Testing - Validación del Sistema
```bash
# 1. Batch testing completo
python main.py --batch-test

# 2. Tests manuales interactivos
python main.py
# > Opción 6: Test Fuzzy Inference
#   - Probar valores extremos
#   - Probar valores normales
#   - Generar visualizaciones

# 3. Ver historial de pruebas
# > Opción 9: View Recommendation History
```

---

## 🎓 CASOS DE USO ACADÉMICOS

### Caso 1: Proyecto Final
**Objetivo:** Presentar sistema completo con análisis

```bash
# Paso 1: Generar dataset grande
python main.py --generate-data 500

# Paso 2: Ejecutar demo
python main.py --demo

# Paso 3: Batch testing
python main.py --batch-test

# Paso 4: Recolectar archivos para reporte
# - generated_data/dataset_*/sample_movies.xlsx
# - visualizations/*.png
# - docs/ARCHITECTURE.md
```

**Entregables:**
- ✅ Dataset de 500 películas (Excel con estadísticas)
- ✅ 4 visualizaciones profesionales (PNG 300 DPI)
- ✅ Resultados de batch testing (performance, accuracy, robustness)
- ✅ Documentación completa

### Caso 2: Experimentación
**Objetivo:** Probar diferentes configuraciones

```bash
# Experimento 1: Dataset pequeño
python main.py --generate-data 50
python main.py --batch-test

# Experimento 2: Dataset mediano
python main.py --generate-data 100
python main.py --batch-test

# Experimento 3: Dataset grande
python main.py --generate-data 500
python main.py --batch-test

# Comparar resultados de performance
```

### Caso 3: Validación Manual
**Objetivo:** Agregar películas conocidas y validar recomendaciones

```bash
python main.py
# > Opción 7: Agregar películas conocidas
#   - Matrix (Action/Sci-Fi, 8.7)
#   - Godfather (Drama/Crime, 9.2)
#   - Inception (Sci-Fi/Thriller, 8.8)

# > Opción 1: Generar recomendaciones
#   Preferencia: Action, Sci-Fi
#   Min rating: 8.0

# > Validar que recomiende Matrix e Inception

# > Opción 9: Ver historial
```

---

## 🛠️ DETALLES TÉCNICOS

### Persistencia de Datos

**recommendation_history.json:**
```json
[
  {
    "timestamp": "2025-10-05T15:30:45.123456",
    "inputs": {
      "user_rating": 8.5,
      "actor_popularity": 75.0,
      "genre_match": 85.0
    },
    "output": 78.45,
    "movie": "The Matrix"
  }
]
```

**custom_movies.csv:**
```csv
movie_id,title,genres,main_actors,director,average_rating,release_year,custom_added,added_timestamp
custom_1728159045,The Matrix,Action|Sci-Fi,Keanu Reeves|Laurence Fishburne,Wachowski Brothers,8.7,1999,true,2025-10-05T15:30:45
```

### Validaciones Implementadas

**Add Custom Movie:**
- Title: No vacío
- Rating: 1.0-10.0 (forzado)
- Year: Integer válido
- Géneros: Opcional, formato libre

**Generate Data:**
- Num movies: 10-1000 (límite de seguridad)
- Validación de espacio en disco
- Manejo de errores en Excel export

**Load Custom Dataset:**
- Columnas requeridas: `title`, `average_rating`
- Validación de tipos de datos
- Manejo de valores faltantes

### Performance

**Benchmarks (en sistema de prueba):**
- Generación de 100 películas: ~2 segundos
- Export CSV: ~0.1 segundos
- Export JSON: ~0.2 segundos
- Export Excel: ~0.5 segundos
- Inferencia fuzzy: ~0.25 ms promedio
- Batch testing completo: ~3 segundos

---

## 📊 FORMATO DE EXPORTACIONES

### CSV Export
```csv
movie_id,title,genres,main_actors,director,average_rating,release_year
1,Movie Title,Action|Drama,Actor1|Actor2,Director Name,8.5,2020
```

### JSON Export
```json
[
  {
    "movie_id": "1",
    "title": "Movie Title",
    "genres": "Action|Drama",
    "main_actors": "Actor1|Actor2",
    "director": "Director Name",
    "average_rating": 8.5,
    "release_year": 2020
  }
]
```

### Excel Export (2 hojas)

**Hoja 1: Movies**
- Todas las columnas del dataset
- Formato tabla con filtros

**Hoja 2: Statistics**
```
Metric              | Value
--------------------|------------------
Total Movies        | 100
Average Rating      | 8.76
Rating Std Dev      | 0.89
Min Rating          | 6.50
Max Rating          | 9.80
Unique Genres       | 18
Most Common Genre   | Drama
Generated           | 2025-10-05 15:30:45
```

---

## 🔍 PREGUNTAS FRECUENTES (FAQ)

### Q1: ¿Dónde se guardan las películas custom?
**A:** En `data/custom_movies.csv` y se integran al dataset actual en memoria.

### Q2: ¿El historial tiene límite?
**A:** Sí, 100 recomendaciones. Cuando se excede, elimina las más antiguas (circular).

### Q3: ¿Puedo usar mis propias películas desde CSV?
**A:** Sí, Opción 11 > "Load custom CSV dataset". Requiere columnas: `title`, `average_rating`.

### Q4: ¿Las visualizaciones se regeneran cada vez?
**A:** Sí, se sobreescriben en `visualizations/`. Para conservar, cópialas a otra carpeta.

### Q5: ¿Qué formato es mejor para Excel?
**A:** El `.xlsx` incluye estadísticas en hojas separadas. Para CSV usa `--export csv`.

### Q6: ¿Puedo generar más de 1000 películas?
**A:** No, el límite es 1000 por seguridad. Para más, genera múltiples veces.

### Q7: ¿El batch testing modifica el dataset?
**A:** No, solo lee datos. Es seguro ejecutarlo múltiples veces.

### Q8: ¿Cómo exporto solo mi historial?
**A:** Opción 9 > "View Recommendation History" > Responder 'y' a export.

---

## ✅ CHECKLIST DE FUNCIONALIDADES

### Características v2.1
- [x] Generación de datasets (`--generate-data`)
- [x] Exportación múltiples formatos (CSV, JSON, Excel)
- [x] Agregar películas personalizadas
- [x] Historial de recomendaciones persistente
- [x] Gestión de datasets (cargar/listar/info)
- [x] Batch testing suite completo
- [x] Exportación desde línea de comandos
- [x] README.txt en datasets generados
- [x] Estadísticas en Excel (hojas múltiples)
- [x] Validación de datos de entrada

### Características v2.0 (previas)
- [x] Interfaz UI limpia (sin emojis)
- [x] Visualizaciones matplotlib/seaborn
- [x] Funciones de membresía gráficas
- [x] Dashboard del sistema
- [x] Modo demo automático
- [x] Compatibilidad Windows

---

## 🎯 PRÓXIMAS MEJORAS SUGERIDAS

1. **Base de datos SQL**
   - SQLite para persistencia
   - Búsquedas más rápidas
   - Relaciones entre tablas

2. **API REST**
   - Flask/FastAPI endpoints
   - Acceso remoto
   - Integración web

3. **Web Interface**
   - Dashboard HTML/CSS/JS
   - Gráficas interactivas (Plotly)
   - Upload de CSV

4. **Machine Learning**
   - Entrenamiento del sistema fuzzy
   - Ajuste automático de membresías
   - Collaborative filtering

5. **Más Exportaciones**
   - PDF con gráficas
   - LaTeX tables
   - Markdown reports

---

## 📞 SOPORTE Y CONTRIBUCIÓN

**Proyecto:** E1_Fzz_AndresTorresCeja_148252CF  
**Curso:** Soft Computing  
**Universidad:** Universidad de Guanajuato  
**Versión:** 2.1.0  
**Fecha:** Octubre 5, 2025

Para más información:
- `README_MODERN_UI.md` - Documentación UI v2.0
- `docs/ARCHITECTURE.md` - Arquitectura del sistema
- `docs/IMRAD.md` - Documento de investigación

---

**¡Sistema de Recomendación con Lógica Difusa - Versión Feature-Complete!**  
*12 Opciones Interactivas • 6 Modos CLI • Persistencia de Datos • Testing Automatizado*
