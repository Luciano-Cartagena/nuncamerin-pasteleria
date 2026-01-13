import sqlite3
from decimal import Decimal

def cargar_datos_ejemplo():
    """Carga datos de ejemplo en la base de datos."""
    conn = sqlite3.connect('pasteleria.db')
    cursor = conn.cursor()
    
    print("Cargando ingredientes de ejemplo...")
    
    # Ingredientes básicos
    ingredientes = [
        ('Harina 0000', 180.00, 'kg'),
        ('Harina Leudante', 200.00, 'kg'),
        ('Azúcar Común', 150.00, 'kg'),
        ('Azúcar Impalpable', 280.00, 'kg'),
        ('Leche Entera', 120.00, 'l'),
        ('Crema de Leche', 350.00, 'l'),
        ('Manteca', 450.00, 'kg'),
        ('Queso Crema', 800.00, 'kg'),
        ('Huevo', 30.00, 'unidad'),
        ('Vainilla', 15.00, 'ml'),
        ('Polvo de Hornear', 8.00, 'g'),
        ('Sal', 2.00, 'g'),
        ('Chocolate Semi-amargo', 1200.00, 'kg'),
        ('Cacao en Polvo', 800.00, 'kg'),
        ('Dulce de Leche', 600.00, 'kg'),
    ]
    
    for nombre, precio, unidad in ingredientes:
        try:
            cursor.execute(
                'INSERT INTO ingredientes (nombre, precio_base, unidad_base) VALUES (?, ?, ?)',
                (nombre, precio, unidad)
            )
            print(f"  ✓ {nombre}")
        except sqlite3.IntegrityError:
            print(f"  - {nombre} (ya existe)")
    
    print("\nCreando recetas de ejemplo...")
    
    # Recetas
    recetas = [
        ('Torta de Vainilla', 'Torta clásica de vainilla esponjosa', 60.00),
        ('Brownie de Chocolate', 'Brownie húmedo con chocolate semi-amargo', 70.00),
        ('Cheesecake Clásico', 'Cheesecake cremoso con base de galletas', 80.00),
    ]
    
    for nombre, descripcion, margen in recetas:
        try:
            cursor.execute(
                'INSERT INTO recetas (nombre, descripcion, margen_ganancia) VALUES (?, ?, ?)',
                (nombre, descripcion, margen)
            )
            print(f"  ✓ {nombre}")
        except sqlite3.IntegrityError:
            print(f"  - {nombre} (ya existe)")
    
    # Ingredientes para Torta de Vainilla
    cursor.execute('SELECT id FROM recetas WHERE nombre = ?', ('Torta de Vainilla',))
    torta_id = cursor.fetchone()
    
    if torta_id:
        torta_id = torta_id[0]
        ingredientes_torta = [
            ('Harina 0000', 300, 'g'),
            ('Azúcar Común', 250, 'g'),
            ('Huevo', 3, 'unidad'),
            ('Manteca', 150, 'g'),
            ('Leche Entera', 200, 'ml'),
            ('Polvo de Hornear', 10, 'g'),
            ('Vainilla', 5, 'ml'),
            ('Sal', 2, 'g'),
        ]
        
        for nombre_ing, cantidad, unidad in ingredientes_torta:
            cursor.execute('SELECT id FROM ingredientes WHERE nombre = ?', (nombre_ing,))
            ing_id = cursor.fetchone()
            if ing_id:
                try:
                    cursor.execute(
                        'INSERT INTO ingrediente_receta (receta_id, ingrediente_id, cantidad, unidad) VALUES (?, ?, ?, ?)',
                        (torta_id, ing_id[0], cantidad, unidad)
                    )
                except sqlite3.IntegrityError:
                    pass  # Ya existe
    
    conn.commit()
    conn.close()
    
    print("\n✅ Datos de ejemplo cargados exitosamente!")
    print("🌐 Ejecuta: python app.py")
    print("📱 Luego abre: http://127.0.0.1:8000")

if __name__ == '__main__':
    cargar_datos_ejemplo()