# 🧁 Sistema de Gestión de Costos - Pastelería Nuncamerin

Sistema web completo para calcular costos de recetas y gestionar márgenes de ganancia en la pastelería Nuncamerin.

## ✨ Características Principales

### 📊 Gestión de Ingredientes
- **Información completa**: Nombre, marca, precio del paquete, peso/cantidad del paquete
- **Unidades flexibles**: Soporte para kg, g, litros, ml y unidades individuales (huevos, limones, etc.)
- **Cálculo automático**: Precio por gramo calculado automáticamente
- **Formato argentino**: Números con punto para miles y coma para decimales (ej: 12.568,50)
- **Edición fácil**: Modificar precios y datos de ingredientes existentes

### 🍰 Gestión de Recetas
- **Ingredientes por receta**: Agregar ingredientes con cantidades específicas
- **Cálculo automático de costos**: El sistema calcula el costo total de la receta
- **Análisis de ganancias**: Muestra cuánto te cuesta, cuánto vas a cobrar y cuánto vas a ganar
- **Márgenes configurables**: Cambiar el porcentaje de ganancia según tus necesidades

### 💰 Análisis Financiero Detallado
- **Costo de ingredientes**: Lo que realmente te cuesta hacer la receta
- **Precio de venta**: Lo que vas a cobrar al cliente
- **Ganancia neta**: Tu ganancia por unidad vendida
- **Multiplicador**: Cuántas veces cobras vs. lo que te cuesta (ej: 3.0x = cobras 3 veces el costo)
- **Interpretación visual**: Indicadores de si el margen es excelente, moderado o bajo

## 🚀 Cómo Usar el Sistema

### 1. Iniciar el Sistema
```bash
# Opción 1: Usar el archivo batch
ejecutar_nuncamerin.bat

# Opción 2: Comando manual
python app.py
```

### 2. Acceder al Sistema
Abrir en el navegador: `http://127.0.0.1:8000`

### 3. Flujo de Trabajo Recomendado

#### Paso 1: Cargar Ingredientes
1. Ir a "Ingredientes" → "Nuevo Ingrediente"
2. Completar:
   - **Nombre**: Ej. "Chocolate Semi-amargo"
   - **Marca**: Ej. "Águila"
   - **Precio del Paquete**: Lo que pagaste (ej. 2.400,00)
   - **Peso/Cantidad del Paquete**: Cuánto viene (ej. 200g)
   - **Unidad**: kg, g, l, ml, o unidad

#### Paso 2: Crear Recetas
1. Ir a "Recetas" → "Nueva Receta"
2. Completar nombre, descripción y margen inicial (ej. 200% = cobras 3 veces el costo)
3. Agregar ingredientes uno por uno con las cantidades que usas

#### Paso 3: Analizar Costos
- El sistema automáticamente calcula:
  - **Costo total** de ingredientes
  - **Precio sugerido** de venta
  - **Ganancia neta** por unidad
  - **Multiplicador** (cuántas veces cobras vs. costo)

#### Paso 4: Ajustar Márgenes
- Usar el botón "🔧 Cambiar Margen de Ganancia"
- Ejemplos comunes:
  - **200%** = Cobras 3 veces el costo (tu preferencia habitual)
  - **150%** = Cobras 2.5 veces el costo
  - **100%** = Cobras 2 veces el costo

## 📋 Ejemplos Prácticos

### Ejemplo: Torta de Chocolate
- **Costo de ingredientes**: $1.250,00
- **Margen**: 200% (cobras 3 veces el costo)
- **Precio de venta**: $3.750,00
- **Ganancia**: $2.500,00

### Ejemplo: Ingrediente por Unidad
- **Huevos**: Compras 12 unidades por $1.800
- **Precio por unidad**: $150,00
- **En receta usas**: 3 huevos = $450,00

## 🔧 Características Técnicas

### Formatos Argentinos
- **Miles**: 12.568 (con punto)
- **Decimales**: 12.568,50 (con coma)
- **Moneda**: $12.568,50

### Unidades Soportadas
- **Peso**: kg, g
- **Volumen**: l, ml  
- **Unidades**: Para huevos, limones, etc.

### Cálculos Automáticos
- Conversión automática entre unidades
- Precio por gramo para ingredientes por peso
- Precio por unidad para ingredientes individuales
- Recálculo automático al cambiar precios

## 💡 Consejos para Nuncamerin

### Gestión de Precios
- **Actualiza regularmente** los precios de ingredientes
- **Usa una balanza** para medir exactamente los gramos que usas
- **Considera costos adicionales** (gas, luz, tiempo) en tu margen

### Márgenes Recomendados
- **200-250%**: Para productos estándar (cobras 3-3.5 veces el costo)
- **150-200%**: Para productos competitivos
- **300%+**: Para productos premium o únicos

### Competencia
- **Compara precios** con otras pastelerías de la zona
- **Ajusta márgenes** según la demanda y competencia
- **Considera el valor agregado** de tus productos artesanales

## 📁 Archivos del Sistema

- `app.py`: Aplicación principal Flask
- `nuncamerin.db`: Base de datos SQLite
- `templates/`: Plantillas HTML del sistema
- `cargar_datos_nuncamerin.py`: Script para cargar datos de ejemplo
- `ejecutar_nuncamerin.bat`: Archivo para iniciar fácilmente

## 🆘 Solución de Problemas

### El sistema no inicia
1. Verificar que el entorno virtual esté activado
2. Ejecutar: `pip install flask`
3. Verificar que el puerto 8000 esté libre

### Los cálculos no se ven
1. Verificar que los ingredientes tengan precios válidos
2. Asegurarse de que las cantidades sean números positivos
3. Revisar que las unidades sean consistentes

### Problemas con números argentinos
- El sistema automáticamente formatea con punto para miles y coma para decimales
- Ingresar números normales (ej: 1250.50), el sistema los formatea automáticamente

---

**🧁 ¡Que tengas éxito con Nuncamerin!**

*Sistema desarrollado específicamente para las necesidades de tu pastelería, con cálculos precisos y formato argentino.*