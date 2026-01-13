# Sistema de Gestión de Costos para Pastelería

Sistema web desarrollado en Django para calcular automáticamente el costo real de recetas y sugerir precios de venta con margen de ganancia configurable.

## Características Principales

- **Gestión de Ingredientes**: Control de precios y unidades de medida
- **Gestión de Recetas**: Composición de productos con cálculo automático de costos
- **Cálculo Automático**: Conversión de unidades y cálculo preciso usando Decimal
- **Panel de Administración**: Interfaz intuitiva basada en Django Admin
- **Margen de Ganancia**: Configurable por receta para sugerir precio de venta

## Tecnologías Utilizadas

- **Backend**: Python 3.11+ con Django 4.2
- **Base de Datos**: SQLite (migrable a PostgreSQL)
- **Panel**: Django Admin personalizado
- **Cálculos**: Decimal para precisión monetaria

## Instalación

### 1. Instalar Python
Descargar Python 3.11+ desde [python.org](https://www.python.org/downloads/)

### 2. Crear entorno virtual
```bash
python -m venv venv
```

### 3. Activar entorno virtual
**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Ejecutar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear superusuario
```bash
python manage.py createsuperuser
```

### 7. Cargar datos de ejemplo (opcional)
```bash
python manage.py cargar_datos_ejemplo
```

### 8. Ejecutar servidor
```bash
python manage.py runserver
```

## Uso del Sistema

### Acceso al Panel
- URL: `http://127.0.0.1:8000/admin/`
- Usar las credenciales del superusuario creado

### Gestión de Ingredientes
1. Ir a "Ingredientes" en el panel
2. Agregar ingredientes con:
   - Nombre descriptivo
   - Precio base por unidad
   - Unidad de medida (gramos, kg, ml, litros, unidad)
3. El sistema actualiza automáticamente la fecha de modificación

### Gestión de Recetas
1. Ir a "Recetas" en el panel
2. Crear nueva receta con:
   - Nombre del producto
   - Descripción (opcional)
   - Margen de ganancia en porcentaje
3. Agregar ingredientes con cantidades específicas
4. El sistema calcula automáticamente:
   - Costo total de la receta
   - Precio sugerido de venta

### Funcionalidades del Cálculo

#### Conversión de Unidades
El sistema convierte automáticamente entre unidades:
- kg ↔ gramos
- litros ↔ mililitros
- Asume densidad 1 para líquidos (1ml = 1g)

#### Precisión Monetaria
- Usa `Decimal` en lugar de `float` para evitar errores de redondeo
- Mantiene precisión en todos los cálculos monetarios

#### Cálculo de Costos
```
Costo Ingrediente = Precio Base × Cantidad Usada
Costo Total = Suma de todos los ingredientes
Precio Sugerido = Costo Total × (1 + Margen/100)
```

## Estructura del Proyecto

```
pasteleria/
├── manage.py                 # Comando principal de Django
├── requirements.txt          # Dependencias
├── pasteleria/              # Configuración del proyecto
│   ├── settings.py          # Configuración principal
│   ├── urls.py              # URLs del proyecto
│   └── wsgi.py              # Configuración WSGI
└── costos/                  # Aplicación principal
    ├── models.py            # Modelos de datos
    ├── admin.py             # Configuración del admin
    ├── tests.py             # Tests unitarios
    └── management/commands/ # Comandos personalizados
```

## Modelos de Datos

### Ingrediente
- `nombre`: Nombre único del ingrediente
- `precio_base`: Precio por unidad base (Decimal)
- `unidad_base`: Unidad de medida (g, kg, ml, l, unidad)
- `fecha_actualizacion`: Timestamp automático

### Receta
- `nombre`: Nombre único del producto
- `descripcion`: Descripción opcional
- `margen_ganancia`: Porcentaje de ganancia (Decimal)
- `ingredientes`: Relación ManyToMany con Ingrediente

### IngredienteReceta (Tabla Intermedia)
- `receta`: FK a Receta
- `ingrediente`: FK a Ingrediente
- `cantidad`: Cantidad específica (Decimal)
- `unidad`: Unidad de medida para esta cantidad

## Decisiones Técnicas

### Uso de Decimal
- Evita errores de redondeo en cálculos monetarios
- Mantiene precisión en operaciones financieras
- Configurado en settings para formato argentino

### Conversión de Unidades
- Sistema unificado basado en gramos
- Conversiones automáticas entre unidades
- Flexibilidad para diferentes tipos de ingredientes

### Django Admin Personalizado
- Campos calculados de solo lectura
- Inlines para gestión intuitiva de ingredientes
- Formateo visual con colores para costos y precios
- Filtros y búsquedas optimizadas

### Validaciones
- Precios y cantidades deben ser positivos
- Nombres únicos para ingredientes y recetas
- Relaciones únicas ingrediente-receta

## Testing

Ejecutar tests:
```bash
python manage.py test
```

Los tests cubren:
- Conversión de unidades
- Cálculos de costos
- Cálculos de precios sugeridos
- Validaciones de modelos

## Escalabilidad Futura

El sistema está diseñado para futuras expansiones:

### API REST
- Estructura preparada para Django REST Framework
- Modelos con serialización en mente

### Frontend con Astro
- Backend independiente del frontend
- APIs preparadas para consumo externo

### Funcionalidades Adicionales
- Gestión de stock
- Historial de precios
- Reportes de rentabilidad
- Integración con MercadoPago
- Gestión de clientes y pedidos

## Soporte

Para problemas o consultas:
1. Revisar logs en consola
2. Verificar migraciones aplicadas
3. Comprobar datos de ejemplo cargados
4. Validar configuración de base de datos

## Licencia

Proyecto desarrollado para uso interno de pastelería.