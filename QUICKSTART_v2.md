# 🚀 SISTEMA MEJORADO v2.0 - GUÍA RÁPIDA

## 📝 Solo 3 pasos para enviar certificados a un nuevo curso

### PASO 1: Editar `config.py`

Abre el archivo `config.py` y modifica SOLO estas 3 líneas:

```python
PREFIX = "imbtain5sprod09251"              # Tu prefijo único del curso
COURSE_NAME_ES = "5s aplicado a Producción"    # Nombre en español
COURSE_NAME_EN = "5s in Production"            # Nombre en inglés
```

**Ejemplo:**
```python
PREFIX = "imbtain5sprod09251"
COURSE_NAME_ES = "5s aplicado a Producción"
COURSE_NAME_EN = "5s in Production"
```

### PASO 2: Preparar archivo Excel

El archivo `certificados.xlsx` debe tener estas columnas:

| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| NOMBRE ALUMNO | Nombre del estudiante | Juan Pérez |
| ID | ID único del certificado | imbtain5sprod09251ar32366535 |
| WEB | URL de verificación | https://imbinstitute.com/verify/... |
| NIVEL | Master, Advanced o Fundamental | Master |
| PDF | Nombre del PDF (opcional) | Certificado-imbtain5sprod09251ar32366535.pdf |
| EMAIL | Email del estudiante | juan@example.com |
| FECHA | Fecha (cualquier formato) | 2025-11-07 |
| **PAGO** | **TRUE/FALSE** | **TRUE** |

⚠️ **MUY IMPORTANTE**: La columna `PAGO` controla quién recibe certificado
- `TRUE` = Enviar certificado ✅
- `FALSE` = NO enviar certificado ❌

### PASO 3: Ejecutar el script

Abre PowerShell en la carpeta del proyecto y ejecuta:

```powershell
python automatization_v2.py
```

**Resultado esperado:**
```
============================================================
📧 IMB INSTITUTE - CERTIFICATE DISTRIBUTION SYSTEM v2.0
============================================================

📌 CONFIGURATION:
   Course Prefix: imbtain5sprod09251
   Course Name (ES): 5s aplicado a Producción
   Course Name (EN): 5s in Production
   Mode: 📧 PRODUCTION

============================================================

🤖 Generando descripción con IA...
✅ Generated description: Certification validating competencies in lean manufacturing, continuous improvement, workplace organization, and operational efficiency in 5s in Production.

📊 Total de registros en Excel: 65
✅ Estudiantes con PAGO=TRUE: 63
❌ Estudiantes con PAGO=FALSE (serán ignorados): 2

🚀 Procesando 63 estudiante(s)...

[1/63] Procesando: Carlos Mendez
✅ Certificado enviado | Alumno: Carlos Mendez | Email: carlos@example.com

... (continúa con todos los estudiantes)

============================================================
📊 RESUMEN FINAL
============================================================
✅ Enviados correctamente: 63
❌ Errores: 0
📧 Total procesados: 63
📁 Registro guardado en: envio_certificados.log
============================================================
```

## 🧪 Modo Prueba

Antes de enviar a TODOS, prueba con un solo email:

1. Abre `config.py` y cambia:
```python
TEST_MODE = True  # Solo envía al TEST_EMAIL
TEST_EMAIL = "tu-email@example.com"
```

2. Ejecuta:
```powershell
python automatization_v2.py
```

3. Si todo va bien, cambia:
```python
TEST_MODE = False  # Ahora envía a todos
```

4. Ejecuta de nuevo:
```powershell
python automatization_v2.py
```

## 🤖 Generación Automática de Descripciones (OPCIONAL)

Si quieres descripciones automáticas generadas con IA (ChatGPT):

1. Instala la librería:
```powershell
pip install openai
```

2. En `config.py`, agrega tu API key:
```python
OPENAI_API_KEY = "sk-tu-api-key-aqui"
```

3. Obtén tu API key gratis en: https://platform.openai.com/api-keys

Sin API key configurada, el sistema usa descripciones genéricas automáticamente.

## 📁 Estructura de Archivos

```
work/
├── config.py                    ← EDITAR AQUÍ para cada curso
├── automatization_v2.py         ← Script principal
├── ai_helper.py                 ← Generador de IA (opcional)
├── certificados.xlsx            ← Tu archivo de estudiantes
├── HTMLs/                       ← Templates generadas automáticamente
│   ├── Certificado-master.html
│   ├── Certificado-advanced.html
│   └── Certificado-fundamental.html
├── PDFs/                        ← Certificados (Certificado-{ID}.pdf)
├── badges/                      ← Insignias por nivel
│   ├── certified-master.png
│   ├── certified-advanced.png
│   └── certified-fundamental.png
├── qrs/                         ← QR codes (estructura lista)
└── envio_certificados.log       ← Log de envíos
```

## 🔑 Configuración de Credenciales

En `config.py`, asegúrate de tener credenciales correctas:

```python
SMTP_SERVER = "mail.imbinstitute.com"
SMTP_PORT = 465
SENDER_EMAIL = "certificados@imbinstitute.com"
SENDER_PASSWORD = "tu-contraseña"
SENDER_NAME = "IMB Institute"
```

## 📊 Archivo de Log

Cada ejecución se registra en `envio_certificados.log`:

```
[2025-11-07 10:15:32] ✅ Certificado enviado | Alumno: Carlos Mendez | Email: carlos@example.com | Estado: ÉXITO
[2025-11-07 10:15:35] ✅ Certificado enviado | Alumno: Maria Garcia | Email: maria@example.com | Estado: ÉXITO
[2025-11-07 10:15:38] ❌ Email vacío | Alumno: Juan Pérez | Email: | Estado: SKIPPED
[2025-11-07 10:15:41] ✅ Certificado enviado | Alumno: Ana Rodriguez | Email: ana@example.com | Estado: ÉXITO
```

## ❓ Solución de Problemas

**P: ¿Qué pasa si el PDF no existe?**
R: Se registra como error en el log, pero el email se sigue enviando con la insignia.

**P: ¿Se respetan los estudiantes con PAGO=FALSE?**
R: SÍ, se saltan automáticamente y no reciben email.

**P: ¿Cómo agrego nuevos niveles de certificación?**
R: Agrega nuevas imágenes PNG a `badges/` con el nombre `certified-{nivel}.png` (ej: certified-gold.png)

**P: ¿Se pueden enviar en modo prueba primero?**
R: SÍ, usa `TEST_MODE = True` y edita `TEST_EMAIL`.

## 🎓 Ejemplo de Uso Completo

**Escenario**: Enviar 65 certificados del curso "5s in Production"

1. En `config.py`:
```python
PREFIX = "imbtain5sprod09251"
COURSE_NAME_ES = "5s aplicado a Producción"
COURSE_NAME_EN = "5s in Production"
TEST_MODE = False  # Modo producción
```

2. Excel tiene 65 registros:
   - 63 con PAGO=TRUE ✅ (recibirán certificado)
   - 2 con PAGO=FALSE ❌ (serán ignorados)

3. Ejecutar:
```powershell
python automatization_v2.py
```

4. Resultado: 63 certificados enviados exitosamente, 0 errores

## ✅ Versión Antigua vs Nueva

| Característica | v1.0 | v2.0 |
|---|---|---|
| Configuración rápida | ⚠️ Editar múltiples líneas | ✅ Solo 3 líneas en config.py |
| Descripciones automáticas | ❌ Manual | ✅ Con IA (opcional) |
| Filtro PAGO | ❌ No | ✅ Sí |
| Templates automáticas | ❌ No | ✅ Genera si no existen |
| Modo prueba | ✅ Sí | ✅ Sí |
| Logging | ✅ Sí | ✅ Mejorado |

---

**¿Preguntas?** Revisa el log file (`envio_certificados.log`) para detalles de cada envío.
