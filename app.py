import os
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from decimal import Decimal

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'nuncamerin-pasteleria-2026')

# Configuración de la base de datos
DATABASE = 'nuncamerin.db'

def init_db():
    """Inicializa la base de datos con las tablas necesarias."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Tabla de ingredientes mejorada
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ingredientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            marca TEXT,
            precio_paquete DECIMAL(10,2) NOT NULL,
            peso_paquete DECIMAL(10,3) NOT NULL,
            unidad_paquete TEXT NOT NULL,
            precio_por_gramo DECIMAL(10,4) GENERATED ALWAYS AS (
                CASE 
                    WHEN unidad_paquete = 'kg' THEN precio_paquete / (peso_paquete * 1000)
                    WHEN unidad_paquete = 'g' THEN precio_paquete / peso_paquete
                    WHEN unidad_paquete = 'l' THEN precio_paquete / (peso_paquete * 1000)
                    WHEN unidad_paquete = 'ml' THEN precio_paquete / peso_paquete
                    ELSE precio_paquete / peso_paquete
                END
            ) STORED,
            fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(nombre, marca)
        )
    ''')
    
    # Tabla de recetas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recetas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            descripcion TEXT,
            margen_ganancia DECIMAL(5,2) DEFAULT 50.00,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de ingredientes por receta mejorada
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ingrediente_receta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            receta_id INTEGER NOT NULL,
            ingrediente_id INTEGER NOT NULL,
            cantidad_usada DECIMAL(10,3) NOT NULL,
            unidad_usada TEXT NOT NULL DEFAULT 'g',
            costo_calculado DECIMAL(10,4),
            FOREIGN KEY (receta_id) REFERENCES recetas (id),
            FOREIGN KEY (ingrediente_id) REFERENCES ingredientes (id),
            UNIQUE(receta_id, ingrediente_id)
        )
    ''')
    
    conn.commit()
    
    # Cargar datos de ejemplo si no existen
    cursor.execute("SELECT COUNT(*) FROM ingredientes")
    if cursor.fetchone()[0] == 0:
        cargar_datos_iniciales(cursor)
        conn.commit()
    
    conn.close()

def cargar_datos_iniciales(cursor):
    """Carga datos iniciales para Nuncamerin."""
    # Ingredientes básicos
    ingredientes = [
        ('Harina 0000', 'Morixe', 850.00, 1.0, 'kg'),
        ('Azúcar Común', 'Ledesma', 650.00, 1.0, 'kg'),
        ('Huevos', 'Granja del Sol', 1800.00, 12, 'unidad'),
        ('Manteca', 'Sancor', 1200.00, 500, 'g'),
        ('Leche Entera', 'La Serenísima', 380.00, 1.0, 'l'),
        ('Chocolate Semi-amargo', 'Águila', 2400.00, 200, 'g'),
        ('Esencia de Vainilla', 'Alicante', 850.00, 60, 'ml'),
        ('Polvo de Hornear', 'Royal', 320.00, 100, 'g'),
    ]
    
    for nombre, marca, precio_paquete, peso_paquete, unidad_paquete in ingredientes:
        try:
            cursor.execute(
                'INSERT INTO ingredientes (nombre, marca, precio_paquete, peso_paquete, unidad_paquete) VALUES (?, ?, ?, ?, ?)',
                (nombre, marca, precio_paquete, peso_paquete, unidad_paquete)
            )
        except sqlite3.IntegrityError:
            pass  # Ya existe
    
    # Receta de ejemplo
    try:
        cursor.execute(
            'INSERT INTO recetas (nombre, descripcion, margen_ganancia) VALUES (?, ?, ?)',
            ('Torta de Vainilla Clásica', 'Torta esponjosa de vainilla con crema', 200.00)
        )
    except sqlite3.IntegrityError:
        pass  # Ya existe

def get_db_connection():
    """Obtiene una conexión a la base de datos."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def calcular_costo_ingrediente(ingrediente_id, cantidad_usada, unidad_usada='g'):
    """Calcula el costo de usar una cantidad específica de un ingrediente."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT precio_paquete, peso_paquete, unidad_paquete
        FROM ingredientes 
        WHERE id = ?
    ''', (ingrediente_id,))
    
    ingrediente = cursor.fetchone()
    conn.close()
    
    if not ingrediente:
        return Decimal('0.00')
    
    precio_paquete = Decimal(str(ingrediente['precio_paquete']))
    peso_paquete = Decimal(str(ingrediente['peso_paquete']))
    cantidad_usada = Decimal(str(cantidad_usada))
    
    # Si el ingrediente se compra por unidades (como huevos)
    if ingrediente['unidad_paquete'] == 'unidad':
        if unidad_usada == 'unidad':
            # Usar unidades directamente
            precio_por_unidad = precio_paquete / peso_paquete
            costo_total = precio_por_unidad * cantidad_usada
        else:
            # Si se usa en gramos pero se compra por unidad, asumir peso promedio
            # Por ejemplo: 1 huevo = 60g aproximadamente
            peso_por_unidad = Decimal('60')  # gramos por huevo (configurable)
            if ingrediente_id:  # Podríamos hacer esto más específico por ingrediente
                cursor = conn.cursor()
                # Aquí podrías agregar una tabla de conversiones específicas
            
            precio_por_unidad = precio_paquete / peso_paquete
            precio_por_gramo = precio_por_unidad / peso_por_unidad
            
            # Convertir cantidad usada a gramos
            if unidad_usada == 'kg':
                cantidad_usada_gramos = cantidad_usada * 1000
            elif unidad_usada == 'l':
                cantidad_usada_gramos = cantidad_usada * 1000
            elif unidad_usada == 'ml':
                cantidad_usada_gramos = cantidad_usada
            else:  # gramos
                cantidad_usada_gramos = cantidad_usada
            
            costo_total = precio_por_gramo * cantidad_usada_gramos
        
        return costo_total
    
    # Para ingredientes por peso/volumen (lógica original)
    # Convertir peso del paquete a gramos
    if ingrediente['unidad_paquete'] == 'kg':
        peso_paquete_gramos = peso_paquete * 1000
    elif ingrediente['unidad_paquete'] == 'l':
        peso_paquete_gramos = peso_paquete * 1000  # Asumimos densidad 1
    elif ingrediente['unidad_paquete'] == 'ml':
        peso_paquete_gramos = peso_paquete
    else:  # gramos
        peso_paquete_gramos = peso_paquete
    
    # Convertir cantidad usada a gramos
    if unidad_usada == 'kg':
        cantidad_usada_gramos = cantidad_usada * 1000
    elif unidad_usada == 'l':
        cantidad_usada_gramos = cantidad_usada * 1000
    elif unidad_usada == 'ml':
        cantidad_usada_gramos = cantidad_usada
    elif unidad_usada == 'unidad':
        # Si se usa por unidad pero se compra por peso, usar peso promedio
        cantidad_usada_gramos = cantidad_usada * 60  # 60g por unidad promedio
    else:  # gramos
        cantidad_usada_gramos = cantidad_usada
    
    # Calcular precio por gramo y costo total
    precio_por_gramo = precio_paquete / peso_paquete_gramos
    costo_total = precio_por_gramo * cantidad_usada_gramos
    
    return costo_total

def calcular_costo_receta(receta_id):
    """Calcula el costo total de una receta."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT ir.ingrediente_id, ir.cantidad_usada, ir.unidad_usada
        FROM ingrediente_receta ir
        WHERE ir.receta_id = ?
    ''', (receta_id,))
    
    ingredientes = cursor.fetchall()
    conn.close()
    
    costo_total = Decimal('0.00')
    
    for ing in ingredientes:
        costo_ingrediente = calcular_costo_ingrediente(
            ing['ingrediente_id'], 
            ing['cantidad_usada'], 
            ing['unidad_usada']
        )
        costo_total += costo_ingrediente
    
    return costo_total

@app.route('/test')
def test():
    """Página de prueba."""
    return render_template('test.html')

@app.route('/')
def index():
    """Página principal."""
    return render_template('index.html')

@app.route('/ingredientes')
def ingredientes():
    """Lista de ingredientes."""
    conn = get_db_connection()
    ingredientes = conn.execute('''
        SELECT *, 
               CASE 
                   WHEN unidad_paquete = 'unidad' THEN precio_paquete / peso_paquete
                   WHEN unidad_paquete = 'kg' THEN precio_paquete / (peso_paquete * 1000)
                   WHEN unidad_paquete = 'g' THEN precio_paquete / peso_paquete
                   WHEN unidad_paquete = 'l' THEN precio_paquete / (peso_paquete * 1000)
                   WHEN unidad_paquete = 'ml' THEN precio_paquete / peso_paquete
                   ELSE precio_paquete / peso_paquete
               END as precio_por_gramo_calc,
               CASE 
                   WHEN unidad_paquete = 'unidad' THEN 'unidad'
                   ELSE 'g'
               END as unidad_precio
        FROM ingredientes 
        ORDER BY nombre, marca
    ''').fetchall()
    conn.close()
    return render_template('ingredientes.html', ingredientes=ingredientes)

@app.route('/ingredientes/nuevo', methods=['GET', 'POST'])
def nuevo_ingrediente():
    """Crear nuevo ingrediente."""
    if request.method == 'POST':
        nombre = request.form['nombre']
        marca = request.form['marca']
        precio_paquete = request.form['precio_paquete']
        peso_paquete = request.form['peso_paquete']
        unidad_paquete = request.form['unidad_paquete']
        
        try:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO ingredientes (nombre, marca, precio_paquete, peso_paquete, unidad_paquete) VALUES (?, ?, ?, ?, ?)',
                (nombre, marca, precio_paquete, peso_paquete, unidad_paquete)
            )
            conn.commit()
            conn.close()
            flash(f'Ingrediente {nombre} ({marca}) creado exitosamente!', 'success')
            return redirect(url_for('ingredientes'))
        except sqlite3.IntegrityError:
            flash('Ya existe un ingrediente con ese nombre y marca.', 'error')
    
    return render_template('nuevo_ingrediente.html')

@app.route('/recetas')
def recetas():
    """Lista de recetas con costos calculados."""
    conn = get_db_connection()
    recetas = conn.execute('SELECT * FROM recetas ORDER BY nombre').fetchall()
    conn.close()
    
    recetas_con_costos = []
    for receta in recetas:
        costo_total = calcular_costo_receta(receta['id'])
        margen = Decimal(str(receta['margen_ganancia']))
        precio_sugerido = costo_total * (1 + margen / 100)
        
        recetas_con_costos.append({
            'id': receta['id'],
            'nombre': receta['nombre'],
            'descripcion': receta['descripcion'],
            'margen_ganancia': margen,
            'costo_total': costo_total,
            'precio_sugerido': precio_sugerido
        })
    
    return render_template('recetas.html', recetas=recetas_con_costos)

@app.route('/recetas/nueva', methods=['GET', 'POST'])
def nueva_receta():
    """Crear nueva receta."""
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        margen_ganancia = request.form['margen_ganancia']
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO recetas (nombre, descripcion, margen_ganancia) VALUES (?, ?, ?)',
                (nombre, descripcion, margen_ganancia)
            )
            receta_id = cursor.lastrowid
            conn.commit()
            conn.close()
            flash('Receta creada exitosamente!', 'success')
            return redirect(url_for('editar_receta', id=receta_id))
        except sqlite3.IntegrityError:
            flash('Ya existe una receta con ese nombre.', 'error')
    
    return render_template('nueva_receta.html')

@app.route('/recetas/<int:id>/editar', methods=['GET', 'POST'])
def editar_receta(id):
    """Editar receta y sus ingredientes."""
    conn = get_db_connection()
    receta = conn.execute('SELECT * FROM recetas WHERE id = ?', (id,)).fetchone()
    
    if not receta:
        flash('Receta no encontrada.', 'error')
        return redirect(url_for('recetas'))
    
    if request.method == 'POST':
        # Verificar si es una actualización de datos de la receta
        if 'actualizar_receta' in request.form:
            nombre = request.form['nombre']
            descripcion = request.form['descripcion']
            
            try:
                conn.execute(
                    'UPDATE recetas SET nombre = ?, descripcion = ?, fecha_modificacion = CURRENT_TIMESTAMP WHERE id = ?',
                    (nombre, descripcion, id)
                )
                conn.commit()
                flash(f'Receta "{nombre}" actualizada exitosamente!', 'success')
                # Recargar los datos de la receta
                receta = conn.execute('SELECT * FROM recetas WHERE id = ?', (id,)).fetchone()
            except sqlite3.IntegrityError:
                flash('Ya existe una receta con ese nombre.', 'error')
        
        # Verificar si es agregar ingrediente a la receta
        elif 'ingrediente_id' in request.form:
            ingrediente_id = request.form['ingrediente_id']
            cantidad_usada = request.form['cantidad_usada']
            unidad_usada = request.form['unidad_usada']
            
            costo_calculado = calcular_costo_ingrediente(ingrediente_id, cantidad_usada, unidad_usada)
            
            try:
                conn.execute(
                    'INSERT INTO ingrediente_receta (receta_id, ingrediente_id, cantidad_usada, unidad_usada, costo_calculado) VALUES (?, ?, ?, ?, ?)',
                    (id, ingrediente_id, float(cantidad_usada), unidad_usada, float(costo_calculado))
                )
                conn.commit()
                flash('Ingrediente agregado a la receta!', 'success')
            except sqlite3.IntegrityError:
                flash('Este ingrediente ya está en la receta.', 'error')
    
    # Obtener ingredientes de la receta
    ingredientes_receta = conn.execute('''
        SELECT ir.*, i.nombre as ingrediente_nombre, i.marca, i.precio_paquete, i.peso_paquete, i.unidad_paquete
        FROM ingrediente_receta ir
        JOIN ingredientes i ON ir.ingrediente_id = i.id
        WHERE ir.receta_id = ?
    ''', (id,)).fetchall()
    
    # Obtener todos los ingredientes disponibles
    todos_ingredientes = conn.execute('SELECT * FROM ingredientes ORDER BY nombre, marca').fetchall()
    
    conn.close()
    
    costo_total = calcular_costo_receta(id)
    margen = Decimal(str(receta['margen_ganancia']))
    precio_sugerido = costo_total * (1 + margen / 100)
    
    return render_template('editar_receta.html', 
                         receta=receta, 
                         ingredientes_receta=ingredientes_receta,
                         todos_ingredientes=todos_ingredientes,
                         costo_total=costo_total,
                         precio_sugerido=precio_sugerido)

@app.route('/ingredientes/<int:id>/editar', methods=['GET', 'POST'])
def editar_ingrediente(id):
    """Editar ingrediente existente."""
    conn = get_db_connection()
    ingrediente = conn.execute('SELECT * FROM ingredientes WHERE id = ?', (id,)).fetchone()
    
    if not ingrediente:
        flash('Ingrediente no encontrado.', 'error')
        return redirect(url_for('ingredientes'))
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        marca = request.form['marca']
        precio_paquete = request.form['precio_paquete']
        peso_paquete = request.form['peso_paquete']
        unidad_paquete = request.form['unidad_paquete']
        
        try:
            conn.execute(
                'UPDATE ingredientes SET nombre = ?, marca = ?, precio_paquete = ?, peso_paquete = ?, unidad_paquete = ?, fecha_actualizacion = CURRENT_TIMESTAMP WHERE id = ?',
                (nombre, marca, precio_paquete, peso_paquete, unidad_paquete, id)
            )
            conn.commit()
            conn.close()
            flash(f'Ingrediente {nombre} actualizado exitosamente!', 'success')
            return redirect(url_for('ingredientes'))
        except sqlite3.IntegrityError:
            flash('Ya existe un ingrediente con ese nombre y marca.', 'error')
    
    conn.close()
    return render_template('editar_ingrediente.html', ingrediente=ingrediente)

def format_number(value):
    """Formatea números con punto para miles y coma para decimales."""
    if value is None:
        return "0,00"
    
    # Convertir a float si es necesario
    if isinstance(value, str):
        try:
            value = float(value)
        except:
            return str(value)
    
    # Formatear con punto para miles y coma para decimales
    formatted = f"{value:,.2f}"
    # Cambiar coma por punto para miles y punto por coma para decimales
    formatted = formatted.replace(',', 'TEMP').replace('.', ',').replace('TEMP', '.')
    return formatted

def format_number_4_decimals(value):
    """Formatea números con 4 decimales."""
    if value is None:
        return "0,0000"
    
    if isinstance(value, str):
        try:
            value = float(value)
        except:
            return str(value)
    
    formatted = f"{value:,.4f}"
    formatted = formatted.replace(',', 'TEMP').replace('.', ',').replace('TEMP', '.')
    return formatted

# Agregar filtros personalizados para las plantillas
@app.template_filter('format_price')
def format_price_filter(value):
    return format_number(value)

@app.template_filter('format_price_per_gram')
def format_price_per_gram_filter(value):
    return format_number_4_decimals(value)

@app.route('/recetas/<int:id>/cambiar_margen', methods=['POST'])
def cambiar_margen(id):
    """Cambiar el margen de ganancia de una receta."""
    nuevo_margen = request.form['nuevo_margen']
    
    try:
        nuevo_margen_decimal = Decimal(str(nuevo_margen))
        if nuevo_margen_decimal < 0:
            flash('El margen de ganancia no puede ser negativo.', 'error')
            return redirect(url_for('editar_receta', id=id))
        
        conn = get_db_connection()
        conn.execute(
            'UPDATE recetas SET margen_ganancia = ?, fecha_modificacion = CURRENT_TIMESTAMP WHERE id = ?',
            (float(nuevo_margen_decimal), id)
        )
        conn.commit()
        conn.close()
        
        flash(f'Margen de ganancia actualizado a {nuevo_margen}%', 'success')
    except (ValueError, TypeError):
        flash('Margen de ganancia inválido.', 'error')
    
    return redirect(url_for('editar_receta', id=id))

@app.route('/ingredientes/<int:id>/eliminar', methods=['POST'])
def eliminar_ingrediente_receta(id):
    """Eliminar ingrediente de una receta."""
    receta_id = request.form['receta_id']
    
    conn = get_db_connection()
    conn.execute('DELETE FROM ingrediente_receta WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    flash('Ingrediente eliminado de la receta.', 'success')
    return redirect(url_for('editar_receta', id=receta_id))

@app.route('/recetas/<int:id>/eliminar', methods=['POST'])
def eliminar_receta(id):
    """Eliminar receta completa."""
    conn = get_db_connection()
    
    # Obtener nombre de la receta antes de eliminarla
    receta = conn.execute('SELECT nombre FROM recetas WHERE id = ?', (id,)).fetchone()
    
    if receta:
        # Eliminar ingredientes de la receta primero
        conn.execute('DELETE FROM ingrediente_receta WHERE receta_id = ?', (id,))
        # Eliminar la receta
        conn.execute('DELETE FROM recetas WHERE id = ?', (id,))
        conn.commit()
        flash(f'Receta "{receta["nombre"]}" eliminada exitosamente.', 'success')
    else:
        flash('Receta no encontrada.', 'error')
    
    conn.close()
    return redirect(url_for('recetas'))

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)