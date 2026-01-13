#!/usr/bin/env python3
"""
Script para probar que la aplicación está lista para despliegue.
"""

import os
import sys
import subprocess

def check_file_exists(filename, description):
    """Verifica si un archivo existe."""
    if os.path.exists(filename):
        print(f"✅ {description}: {filename}")
        return True
    else:
        print(f"❌ {description}: {filename} - NO ENCONTRADO")
        return False

def check_requirements():
    """Verifica que requirements.txt tenga las dependencias necesarias."""
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
            
        required = ['Flask', 'gunicorn']
        missing = []
        
        for req in required:
            if req.lower() not in content.lower():
                missing.append(req)
        
        if missing:
            print(f"❌ Faltan dependencias en requirements.txt: {', '.join(missing)}")
            return False
        else:
            print("✅ requirements.txt tiene todas las dependencias necesarias")
            return True
            
    except FileNotFoundError:
        print("❌ requirements.txt no encontrado")
        return False

def check_app_structure():
    """Verifica la estructura de la aplicación."""
    try:
        # Importar la app para verificar que no hay errores de sintaxis
        sys.path.insert(0, '.')
        from app import app
        print("✅ app.py se importa correctamente")
        
        # Verificar que tenga las rutas principales
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        essential_routes = ['/', '/ingredientes', '/recetas']
        
        missing_routes = []
        for route in essential_routes:
            if route not in routes:
                missing_routes.append(route)
        
        if missing_routes:
            print(f"❌ Faltan rutas esenciales: {', '.join(missing_routes)}")
            return False
        else:
            print("✅ Todas las rutas esenciales están presentes")
            return True
            
    except Exception as e:
        print(f"❌ Error al importar app.py: {e}")
        return False

def check_production_config():
    """Verifica configuración para producción."""
    try:
        with open('app.py', 'r') as f:
            content = f.read()
        
        checks = [
            ('os.environ.get(\'PORT\'', 'Configuración de puerto dinámico'),
            ('host=\'0.0.0.0\'', 'Host configurado para producción'),
            ('os.environ.get(\'SECRET_KEY\'', 'Secret key desde variable de entorno')
        ]
        
        all_good = True
        for check, description in checks:
            if check in content:
                print(f"✅ {description}")
            else:
                print(f"❌ {description} - NO CONFIGURADO")
                all_good = False
        
        return all_good
        
    except FileNotFoundError:
        print("❌ app.py no encontrado")
        return False

def main():
    """Ejecuta todas las verificaciones."""
    print("🚀 VERIFICACIÓN DE DESPLIEGUE - SISTEMA NUNCAMERIN")
    print("=" * 55)
    
    checks = [
        ("Archivos de configuración", lambda: all([
            check_file_exists('requirements.txt', 'Dependencias Python'),
            check_file_exists('Procfile', 'Configuración de proceso'),
            check_file_exists('app.py', 'Aplicación principal'),
            check_file_exists('railway.json', 'Configuración Railway'),
            check_file_exists('render.yaml', 'Configuración Render')
        ])),
        ("Dependencias", check_requirements),
        ("Estructura de la aplicación", check_app_structure),
        ("Configuración de producción", check_production_config)
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\n📋 Verificando: {check_name}")
        result = check_func()
        results.append((check_name, result))
    
    print("\n" + "=" * 55)
    print("📊 RESUMEN:")
    
    all_passed = True
    for check_name, result in results:
        status = "✅ LISTO" if result else "❌ NECESITA ATENCIÓN"
        print(f"   {check_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 55)
    if all_passed:
        print("🎉 ¡TU APLICACIÓN ESTÁ LISTA PARA DESPLIEGUE!")
        print("\n📋 Próximos pasos:")
        print("1. Sube tu código a GitHub")
        print("2. Ve a railway.app y crea una cuenta")
        print("3. Conecta tu repositorio de GitHub")
        print("4. ¡Disfruta tu app online!")
        print("\n🌐 Lee GUIA_DESPLIEGUE.md para instrucciones detalladas")
    else:
        print("⚠️  Hay algunos problemas que resolver antes del despliegue.")
        print("📖 Revisa los errores arriba y corrígelos.")

if __name__ == '__main__':
    main()