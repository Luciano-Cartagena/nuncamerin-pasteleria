import sqlite3
from decimal import Decimal

def cargar_datos_nuncamerin():
    """Carga datos de ejemplo para la pastelería Nuncamerin."""
    conn = sqlite3.connect('nuncamerin.db')
    cursor = conn.cursor()
    
    print("🧁 Cargando ingredientes para Nuncamerin...")
    
    # Ingredientes con marca, precio de paquete y peso de paquete
    ingredientes = [
        # Harinas
        ('Harina 0000', 'Morixe', 850.00, 1.0, 'kg'),
        ('Harina Leudante', 'Blancaflor', 920.00, 1.0, 'kg'),
        
        # Azúcares
        ('Azúcar Común', 'Ledesma', 650.00, 1.0, 'kg'),
        ('Azúcar Impalpable', 'Ledesma', 1200.00, 500, 'g'),
        
        # Lácteos
        ('Leche Entera', 'La Serenísima', 380.00, 1.0, 'l'),
        ('Crema de Leche', 'La Serenísima', 450.00, 500, 'ml'),
        ('Manteca', 'Sancor', 1200.00, 500, 'g'),
        ('Queso Crema', 'Philadelphia', 2800.00, 300, 'g'),
        
        # Huevos y otros
        ('Huevos', 'Granja del Sol', 1800.00, 12, 'unidad'),
        ('Esencia de Vainilla', 'Alicante', 850.00, 60, 'ml'),
        ('Polvo de Hornear', 'Royal', 320.00, 100, 'g'),
        ('Sal Fina', 'Celusal', 180.00, 500, 'g'),
        
        # Chocolates
        ('Chocolate Semi-amargo', 'Águila', 2400.00, 200, 'g'),
        ('Cacao en Polvo', 'Nesquik', 1800.00, 400, 'g'),
        ('Chocolate Blanco', 'Milka', 1200.00, 100, 'g'),
        
        # Dulces y rellenos
        ('Dulce de Leche', 'La Serenísima', 980.00, 400, 'g'),
        ('Mermelada de Frutilla', 'Arcor', 650.00, 454, 'g'),
        ('Crema Pastelera en Polvo', 'Exquisita', 420.00, 100, 'g'),
        
        # Frutas (por unidad)
        ('Limones', 'Verdulería', 500.00, 6, 'unidad'),
        ('Naranjas', 'Verdulería', 800.00, 8, 'unidad'),
        
        # Decoración
        ('Azúcar Glas', 'Ledesma', 850.00, 250, 'g'),
        ('Colorante Rojo', 'Alicante', 320.00, 30, 'ml'),
        ('Colorante Azul', 'Alicante', 320.00, 30, 'ml'),
    ]
    
    for nombre, marca, precio_paquete, peso_paquete, unidad_paquete in ingredientes:
        try:
            cursor.execute(
                'INSERT INTO ingredientes (nombre, marca, precio_paquete, peso_paquete, unidad_paquete) VALUES (?, ?, ?, ?, ?)',
                (nombre, marca, precio_paquete, peso_paquete, unidad_paquete)
            )
            print(f"  ✅ {nombre} ({marca})")
        except sqlite3.IntegrityError:
            print(f"  ⚠️ {nombre} ({marca}) - ya existe")
    
    print("\n🍰 Creando recetas de ejemplo...")
    
    # Recetas típicas de pastelería
    recetas = [
        ('Torta de Vainilla Clásica', 'Torta esponjosa de vainilla con crema', 200.00),
        ('Brownie de Chocolate', 'Brownie húmedo con chocolate semi-amargo', 250.00),
        ('Cheesecake de Frutilla', 'Cheesecake cremoso con mermelada', 300.00),
        ('Lemon Pie', 'Tarta de limón con merengue', 280.00),
        ('Muffins de Chocolate', 'Muffins individuales con chips de chocolate', 200.00),
    ]
    
    for nombre, descripcion, margen in recetas:
        try:
            cursor.execute(
                'INSERT INTO recetas (nombre, descripcion, margen_ganancia) VALUES (?, ?, ?)',
                (nombre, descripcion, margen)
            )
            print(f"  ✅ {nombre}")
        except sqlite3.IntegrityError:
            print(f"  ⚠️ {nombre} - ya existe")
    
    print("\n🥄 Agregando ingredientes a las recetas...")
    
    # Ingredientes para Torta de Vainilla Clásica
    cursor.execute('SELECT id FROM recetas WHERE nombre = ?', ('Torta de Vainilla Clásica',))
    torta_result = cursor.fetchone()
    
    if torta_result:
        torta_id = torta_result[0]
        ingredientes_torta = [
            ('Harina 0000', 300, 'g'),
            ('Azúcar Común', 250, 'g'),
            ('Huevos', 3, 'unidad'),
            ('Manteca', 150, 'g'),
            ('Leche Entera', 200, 'ml'),
            ('Polvo de Hornear', 10, 'g'),
            ('Esencia de Vainilla', 5, 'ml'),
            ('Sal Fina', 2, 'g'),
        ]
        
        for nombre_ing, cantidad, unidad in ingredientes_torta:
            cursor.execute('SELECT id FROM ingredientes WHERE nombre = ?', (nombre_ing,))
            ing_result = cursor.fetchone()
            if ing_result:
                try:
                    cursor.execute(
                        'INSERT INTO ingrediente_receta (receta_id, ingrediente_id, cantidad_usada, unidad_usada) VALUES (?, ?, ?, ?)',
                        (torta_id, ing_result[0], cantidad, unidad)
                    )
                    print(f"    ✅ {nombre_ing}: {cantidad}{unidad}")
                except sqlite3.IntegrityError:
                    print(f"    ⚠️ {nombre_ing} - ya agregado")
    
    # Ingredientes para Brownie de Chocolate
    cursor.execute('SELECT id FROM recetas WHERE nombre = ?', ('Brownie de Chocolate',))
    brownie_result = cursor.fetchone()
    
    if brownie_result:
        brownie_id = brownie_result[0]
        ingredientes_brownie = [
            ('Chocolate Semi-amargo', 200, 'g'),
            ('Manteca', 150, 'g'),
            ('Azúcar Común', 200, 'g'),
            ('Huevos', 2, 'unidad'),
            ('Harina 0000', 100, 'g'),
            ('Cacao en Polvo', 30, 'g'),
            ('Esencia de Vainilla', 3, 'ml'),
            ('Sal Fina', 1, 'g'),
        ]
        
        for nombre_ing, cantidad, unidad in ingredientes_brownie:
            cursor.execute('SELECT id FROM ingredientes WHERE nombre = ?', (nombre_ing,))
            ing_result = cursor.fetchone()
            if ing_result:
                try:
                    cursor.execute(
                        'INSERT INTO ingrediente_receta (receta_id, ingrediente_id, cantidad_usada, unidad_usada) VALUES (?, ?, ?, ?)',
                        (brownie_id, ing_result[0], cantidad, unidad)
                    )
                    print(f"    ✅ {nombre_ing}: {cantidad}{unidad}")
                except sqlite3.IntegrityError:
                    print(f"    ⚠️ {nombre_ing} - ya agregado")
    
    conn.commit()
    conn.close()
    
    print("\n🎉 ¡Datos de ejemplo cargados exitosamente para Nuncamerin!")
    print("🌐 Tu sistema está listo en: http://127.0.0.1:8000")
    print("💡 Ahora puedes:")
    print("   • Ver y editar ingredientes")
    print("   • Crear nuevas recetas")
    print("   • Calcular costos y márgenes de ganancia")
    print("   • Cambiar márgenes según tu preferencia (generalmente 200% = 3x el costo)")

if __name__ == '__main__':
    cargar_datos_nuncamerin()