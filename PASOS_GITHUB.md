# 📋 Pasos para Subir a GitHub - Súper Fácil

## 🎯 Paso 1: Crear Repositorio en GitHub

1. **Ve a**: https://github.com
2. **Inicia sesión** con tu cuenta (o crea una si no tienes)
3. **Click en el botón verde**: "New" o "New repository"
4. **Nombre del repositorio**: `nuncamerin-pasteleria`
5. **Descripción**: "Sistema de gestión de costos para pastelería Nuncamerin"
6. **Público o Privado**: Elige lo que prefieras
7. **NO marques**: "Add a README file" (ya tienes uno)
8. **Click**: "Create repository"

## 🚀 Paso 2: Conectar tu Código Local con GitHub

GitHub te mostrará una página con comandos. Copia y pega estos comandos en tu terminal:

```bash
git remote add origin https://github.com/TU_USUARIO/nuncamerin-pasteleria.git
git branch -M main
git push -u origin main
```

**Reemplaza `TU_USUARIO`** con tu nombre de usuario de GitHub.

## ✅ Paso 3: Verificar que se Subió

1. **Refresca** la página de tu repositorio en GitHub
2. **Deberías ver** todos tus archivos:
   - `app.py`
   - `requirements.txt`
   - `templates/`
   - `README_NUNCAMERIN.md`
   - etc.

## 🎉 ¡Listo para Desplegar!

Una vez que tu código esté en GitHub, puedes desplegarlo en:

### Railway (Recomendado)
1. **Ve a**: https://railway.app
2. **Regístrate** con tu cuenta de GitHub
3. **"New Project"** → "Deploy from GitHub repo"
4. **Selecciona**: `nuncamerin-pasteleria`
5. **Espera 3 minutos** → ¡Tu app estará online!

### Render (Alternativa)
1. **Ve a**: https://render.com
2. **Regístrate** con GitHub
3. **"New"** → "Web Service"
4. **Conecta** tu repositorio
5. **Deploy** automático

## 🆘 Si Tienes Problemas

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/TU_USUARIO/nuncamerin-pasteleria.git
```

### Error: "Permission denied"
- Verifica que estés logueado en GitHub
- Usa tu nombre de usuario correcto
- Puede que necesites configurar SSH (opcional)

### Error: "Repository not found"
- Verifica que el nombre del repositorio sea exacto
- Asegúrate de que el repositorio sea público o tengas acceso

## 💡 Comandos Útiles

```bash
# Ver el estado de Git
git status

# Ver los archivos que se van a subir
git log --oneline

# Ver la URL del repositorio remoto
git remote -v
```

---

**🧁 ¡En unos minutos tendrás tu sistema Nuncamerin disponible en internet!**

*Recuerda: Una vez en GitHub, el despliegue en Railway o Render es automático.*