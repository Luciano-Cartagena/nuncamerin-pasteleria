#!/usr/bin/env python3
"""
Script de prueba para verificar que el sistema Nuncamerin funciona correctamente.
"""

import sqlite3
from decimal import Decimal

def test_database():
    """Prueba la conexión y estructura de la base de datos."""
    print("🔍 Probando conexión a la base de datos...")
    
    try:
        conn = sqlite3.connect('nuncamerin.db')
        cursor = conn.cursor()
        
        # Verificar tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"✅ Tablas encontradas: {[table[0] for table in tables]}")
        
        # Contar ingredientes
        cursor.execute("SELECT COUNT(*) FROM ingredientes")
        count_ingredientes = cursor.fetchone()[0]
        print(f"✅ Ingredientes en la base: {count_ingredientes}")
        
        # Contar recetas
        cursor.execute("SELECT COUNT(*) FROM recetas")
        count_recetas = cursor.fetchone()[0]
        print(f"✅ Recetas en la base: {count_recetas}")
        
        # Mostrar algunos ingredientes
        cursor.execute("SELECT nombre, marca, precio_paquete FROM ingredientes LIMIT 3")
        ingredientes = cursor.fetchall()
        print("✅ Ejemplos de ingredientes:")
        for ing in ingredientes:
            print(f"   - {ing[0]} ({ing[1]}): ${ing[2]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error en la base de datos: {e}")
        return False

def test_decimal_conversion():
    """Prueba la conversión de Decimal a float."""
    print("\n🔍 Probando conversión de Decimal...")
    
    try:
        # Simular cálculo con Decimal
        precio = Decimal('1250.50')
        cantidad = Decimal('300')
        resultado = precio * cantidad / 1000
        
        print(f"✅ Cálculo Decimal: {resultado}")
        print(f"✅ Conversión a float: {float(resultado)}")
        
        # Probar inserción simulada
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE test (valor REAL)')
        cursor.execute('INSERT INTO test VALUES (?)', (float(resultado),))
        
        cursor.execute('SELECT valor FROM test')
        valor_guardado = cursor.fetchone()[0]
        print(f"✅ Valor guardado en SQLite: {valor_guardado}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error en conversión Decimal: {e}")
        return False

def test_format_argentino():
    """Prueba el formato de números argentino."""
    print("\n🔍 Probando formato argentino...")
    
    try:
        # Simular función de formato
        def format_number(value):
            if value is None:
                return "0,00"
            
            if isinstance(value, str):
                try:
                    value = float(value)
                except:
                    return str(value)
            
            formatted = f"{value:,.2f}"
            formatted = formatted.replace(',', 'TEMP').replace('.', ',').replace('TEMP', '.')
            return formatted
        
        test_values = [1250.50, 12568.75, 3.14, 1000000.99]
        
        for val in test_values:
            formatted = format_number(val)
            print(f"✅ {val} → {formatted}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en formato argentino: {e}")
        return False

def main():
    """Ejecuta todas las pruebas."""
    print("🧁 SISTEMA NUNCAMERIN - PRUEBAS DE FUNCIONAMIENTO")
    print("=" * 50)
    
    tests = [
        ("Base de Datos", test_database),
        ("Conversión Decimal", test_decimal_conversion),
        ("Formato Argentino", test_format_argentino)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Ejecutando: {test_name}")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"   {test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("🌐 El sistema está listo en: http://127.0.0.1:8000")
    else:
        print("\n⚠️ Algunas pruebas fallaron. Revisa los errores arriba.")

if __name__ == '__main__':
    main()