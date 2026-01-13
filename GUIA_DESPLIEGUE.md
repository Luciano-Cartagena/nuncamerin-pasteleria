# 🚀 Guía de Despliegue - Sistema Nuncamerin

## 🌟 Opciones de Despliegue Gratuito

### 1. **Railway** (Más Recomendado) 🚂

#### ✅ Ventajas:
- **Completamente gratis** para proyectos pequeños
- **Dominio gratis** incluido (ej: `nuncamerin-pasteleria.up.railway.app`)
- **Base de datos SQLite persistente**
- **Despliegue automático** desde GitHub
- **Muy fácil de configurar**

#### 📋 Pasos para Railway:

1. **Crear cuenta en Railway**
   - Ve a: https://railway.app
   - Regístrate con GitHub (gratis)

2. **Subir tu código a GitHub**
   - Crea un repositorio en GitHub
   - Sube todos los archivos de tu proyecto

3. **Conectar Railway con GitHub**
   - En Railway: "New Project" → "Deploy from GitHub repo"
   - Selecciona tu repositorio
   - Railway detectará automáticamente que es una app Flask

4. **Configurar variables de entorno** (opcional)
   - `FLASK_ENV=production`
   - `SECRET_KEY` (Railway lo genera automáticamente)

5. **¡Listo!** 
   - Railway te dará una URL como: `https://nuncamerin-pasteleria.up.railway.app`

---

### 2. **Render** 🎨

#### ✅ Ventajas:
- **Plan gratuito generoso**
- **Dominio gratis** (ej: `nuncamerin-pasteleria.onrender.com`)
- **SSL automático**
- **Fácil configuración**

#### 📋 Pasos para Render:

1. **Crear cuenta en Render**
   - Ve a: https://render.com
   - Regístrate con GitHub

2. **Crear Web Service**
   - "New" → "Web Service"
   - Conecta tu repositorio de GitHub
   - Configuración automática detectada

3. **Configurar**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

4. **Variables de entorno**
   - `FLASK_ENV=production`

---

### 3. **PythonAnywhere** 🐍

#### ✅ Ventajas:
- **Especializado en Python**
- **Plan gratuito disponible**
- **Fácil para principiantes**

#### 📋 Pasos para PythonAnywhere:

1. **Crear cuenta**
   - Ve a: https://www.pythonanywhere.com
   - Plan "Beginner" (gratis)

2. **Subir archivos**
   - Usa el file manager o Git
   - Sube todos los archivos del proyecto

3. **Configurar Web App**
   - "Web" → "Add a new web app"
   - Selecciona Flask
   - Configura el path a tu `app.py`

---

## 📁 Archivos Necesarios para Despliegue

Tu proyecto ya tiene todos los archivos necesarios:

```
nuncamerin/
├── app.py                 # Aplicación principal
├── requirements.txt       # Dependencias Python
├── Procfile              # Para Railway/Render
├── railway.json          # Configuración Railway
├── render.yaml           # Configuración Render
├── runtime.txt           # Versión de Python
├── templates/            # Plantillas HTML
├── nuncamerin.db         # Base de datos (se crea automáticamente)
└── README_NUNCAMERIN.md  # Documentación
```

## 🔧 Preparación Final

### 1. **Crear repositorio en GitHub**

```bash
# En tu carpeta del proyecto
git init
git add .
git commit -m "Sistema Nuncamerin - Primera versión"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/nuncamerin-pasteleria.git
git push -u origin main
```

### 2. **Verificar archivos importantes**

✅ `requirements.txt` - Dependencias
✅ `Procfile` - Comando de inicio
✅ `app.py` - Configurado para producción
✅ `railway.json` - Configuración Railway
✅ `render.yaml` - Configuración Render

## 🌐 Dominios Personalizados (Opcional)

### Dominios Gratis:
- **Freenom**: .tk, .ml, .ga, .cf (gratis por 1 año)
- **Dot.tk**: Dominios .tk gratuitos

### Configurar Dominio Personalizado:
1. **Railway**: Settings → Domains → Add Custom Domain
2. **Render**: Settings → Custom Domains
3. **Configurar DNS**: Apuntar a la IP/CNAME del servicio

## 💡 Recomendación Final

**Para Nuncamerin, recomiendo Railway porque:**

1. ✅ **Más fácil de usar**
2. ✅ **Mejor para SQLite** (base de datos persistente)
3. ✅ **Dominio gratis inmediato**
4. ✅ **Despliegue automático** cuando actualizas el código
5. ✅ **Plan gratuito generoso**

## 🚀 Pasos Rápidos para Railway

1. **Sube tu código a GitHub**
2. **Ve a railway.app y regístrate**
3. **"New Project" → "Deploy from GitHub repo"**
4. **Selecciona tu repositorio**
5. **¡Espera 2-3 minutos y tendrás tu URL!**

---

## 🆘 Solución de Problemas

### Error: "Application failed to start"
- Verifica que `requirements.txt` tenga Flask y gunicorn
- Asegúrate de que `app.py` esté en la raíz del proyecto

### Error: "Database not found"
- La base de datos se crea automáticamente al iniciar
- Verifica que `init_db()` se ejecute en `if __name__ == '__main__'`

### Error: "Port binding"
- Asegúrate de usar `port = int(os.environ.get('PORT', 8000))`
- Y `host='0.0.0.0'` en `app.run()`

---

**🧁 ¡Tu sistema Nuncamerin estará disponible 24/7 en internet!**

*Con cualquiera de estas opciones tendrás tu pastelería online gratis.*