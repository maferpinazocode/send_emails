# 🎓 SISTEMA CERTIFICADOS v2.0 - GUÍA VISUAL

## 🚀 ¿Cómo enviar certificados a un NUEVO CURSO?

### SOLO 3 PASOS - MENOS DE 2 MINUTOS ⏱️

---

## PASO 1️⃣: Editar `config.py`

Abre el archivo `config.py` y busca estas líneas:

```python
PREFIX = "imbtain5sprod09251"
COURSE_NAME_ES = "5s aplicado a Producción"
COURSE_NAME_EN = "5s in Production"
```

**CAMBIA SOLAMENTE ESTOS 3 VALORES:**

| Campo | Qué poner | Ejemplo |
|-------|-----------|---------|
| PREFIX | Código único del curso | `imbtain5sprod09251` |
| COURSE_NAME_ES | Nombre del curso en ESPAÑOL | `5s aplicado a Producción` |
| COURSE_NAME_EN | Nombre del curso en INGLÉS | `5s in Production` |

### Ejemplo de modificación:

**ANTES:**
```python
PREFIX = "imbtain5sprod09251"
COURSE_NAME_ES = "5s aplicado a Producción"
COURSE_NAME_EN = "5s in Production"
```

**DESPUÉS** (para otro curso):
```python
PREFIX = "imbtainlogist12345"
COURSE_NAME_ES = "Logística Integral"
COURSE_NAME_EN = "Integral Logistics"
```

---

## PASO 2️⃣: Preparar el archivo Excel

**Abre `certificados.xlsx` y asegúrate que tenga estas columnas:**

```
┌─────────────────┬──────────────────┬──────────┬─────────┬────────┬──────────────────────┬────────┬────────┐
│ NOMBRE ALUMNO   │ ID               │ WEB      │ NIVEL   │ PDF    │ EMAIL                │ FECHA  │ PAGO   │
├─────────────────┼──────────────────┼──────────┼─────────┼────────┼──────────────────────┼────────┼────────┤
│ Carlos Mendez   │ imbtain5s...001  │ https... │ Master  │ (auto) │ carlos@example.com   │ 2025.. │ TRUE   │
│ Maria Garcia    │ imbtain5s...002  │ https... │ Advanced│ (auto) │ maria@example.com    │ 2025.. │ TRUE   │
│ Juan Pérez      │ imbtain5s...003  │ https... │ Fundamental │ (auto) │ juan@example.com  │ 2025.. │ FALSE  │
└─────────────────┴──────────────────┴──────────┴─────────┴────────┴──────────────────────┴────────┴────────┘
```

### ⚠️ IMPORTANTE: Columna PAGO

La columna `PAGO` controla TODO:

| PAGO = TRUE | PAGO = FALSE |
|---|---|
| ✅ Estudiante recibe certificado | ❌ Estudiante NO recibe certificado |
| ✅ Se envía email | ❌ Se ignora completamente |
| ✅ Se registra en log | ❌ NO se procesa |

**Ejemplo:**
- 65 estudiantes en Excel
- 63 tienen PAGO=TRUE → **Se envían 63 certificados** ✅
- 2 tienen PAGO=FALSE → **Se ignoran** ❌
- **Resultado: 63 enviados, 0 errores**

---

## PASO 3️⃣: Ejecutar

Abre PowerShell en la carpeta del proyecto y copia/pega:

```powershell
python automatization_v2.py
```

### Resultado esperado:

```
============================================================
📧 IMB INSTITUTE - CERTIFICATE DISTRIBUTION SYSTEM v2.0
============================================================

📌 CONFIGURATION:
   Course Prefix: imbtain5sprod09251
   Course Name (ES): 5s aplicado a Producción
   Course Name (EN): 5s in Production
   Mode: 📧 PRODUCTION

🤖 Generando descripción con IA...
✅ Generated description: Certification validating competencies in lean manufacturing,
   continuous improvement, workplace organization, and operational efficiency...

📊 Total de registros en Excel: 65
✅ Estudiantes con PAGO=TRUE: 63
❌ Estudiantes con PAGO=FALSE (serán ignorados): 2

🚀 Procesando 63 estudiante(s)...

[1/63] Procesando: Carlos Mendez
✅ Certificado enviado | Alumno: Carlos Mendez | Email: carlos@example.com

[2/63] Procesando: Maria Garcia
✅ Certificado enviado | Alumno: Maria Garcia | Email: maria@example.com

... (continúa automáticamente)

============================================================
📊 RESUMEN FINAL
============================================================
✅ Enviados correctamente: 63
❌ Errores: 0
📧 Total procesados: 63
📁 Registro guardado en: envio_certificados.log
============================================================
```

---

## 🧪 ANTES: HACER PRUEBA (RECOMENDADO)

Antes de enviar a 60+ estudiantes, **prueba con 1 solo email:**

### 1. Abre `config.py` y cambia:

```python
TEST_MODE = True  # ← Cambia esto a True
TEST_EMAIL = "tu-email-personal@gmail.com"  # ← Tu email
```

### 2. Ejecuta:

```powershell
python automatization_v2.py
```

Verás algo como:

```
Mode: 🧪 TEST (to tu-email-personal@gmail.com)
...
✅ Certificado enviado | Alumno: Carlos Mendez | Email: tu-email-personal@gmail.com
```

### 3. Si todo va bien en tu email, VUELVE A CAMBIAR:

```python
TEST_MODE = False  # ← Cambia a False para producción
```

### 4. Ejecuta de nuevo (ahora enviará a TODOS):

```powershell
python automatization_v2.py
```

---

## 🤖 BONUS: Descripciones Automáticas con IA (Opcional)

El sistema genera descripciones automáticamente basadas en el nombre del curso.

**Para usar IA de ChatGPT:**

### 1. Instala OpenAI:
```powershell
pip install openai
```

### 2. En `config.py`, agrega tu API key:
```python
OPENAI_API_KEY = "sk-tu-api-key-aqui"
```

### 3. Obtén tu API key GRATIS:
- Ve a: https://platform.openai.com/api-keys
- Copia tu clave
- Pégala en `config.py`

**Sin API key:** El sistema sigue funcionando con descripciones genéricas.

---

## 📚 FLUJO VISUAL COMPLETO

```
┌─────────────────────────┐
│  Edita config.py        │  ← 3 valores: PREFIX, ES, EN
│  con 3 líneas           │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Abre certificados.xlsx  │
│ Revisa columna PAGO     │  ← TRUE/FALSE
│ (TRUE=enviar)           │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ python automatization_v2.py │
│ en PowerShell           │
└────────────┬────────────┘
             │
             ▼
      ┌──────┴──────┐
      │             │
      ▼             ▼
   ✅ SUCCESS    ❌ ERROR
   (Revisa log)
```

---

## 🆘 PREGUNTAS COMUNES

### P: ¿Qué si NO tengo API key de OpenAI?
**R:** No hay problema. El sistema genera descripciones genéricas automáticamente.

### P: ¿Se respeta la columna PAGO?
**R:** SÍ, 100%. Los estudiantes con PAGO=FALSE se ignoran completamente.

### P: ¿Dónde veo los errores?
**R:** En el archivo `envio_certificados.log` (se actualiza automáticamente).

### P: ¿Cuánto tarda enviar 60+ certificados?
**R:** ~3-4 minutos (con delay de 2 segundos entre emails).

### P: ¿Se pueden cambiar los templates HTML?
**R:** SÍ, están en la carpeta `HTMLs/` y se personalizan automáticamente.

### P: ¿Qué pasa si el PDF no existe?
**R:** Se registra como error, pero el email se sigue enviando con la insignia.

---

## 📂 ARCHIVOS IMPORTANTES

```
📁 work/
├── config.py                    ← ✏️ EDITAR AQUÍ (3 líneas)
├── automatization_v2.py         ← Script principal (NO tocar)
├── certificados.xlsx            ← Tu Excel con estudiantes
├── HTMLs/                       ← Templates (se generan solos)
├── PDFs/                        ← Certificados (Certificado-{ID}.pdf)
├── badges/                      ← Insignias por nivel
└── envio_certificados.log       ← Log de envíos (revisar si hay errores)
```

---

## ✅ CHECKLIST ANTES DE ENVIAR

- [ ] Edité las 3 líneas en `config.py`
- [ ] Mi Excel tiene columna PAGO con TRUE/FALSE
- [ ] Probé primero con TEST_MODE = True
- [ ] Vi que el email llegó a mi inbox
- [ ] Cambié TEST_MODE = False
- [ ] Ejecuté el script
- [ ] Revisé el log para confirmar que todo salió bien

---

## 🎯 RESULTADO ESPERADO

**Antes:** 
- ⏱️ 30 minutos editando archivos
- 🔧 Cambiar múltiples líneas de código
- 😫 Confusión con configuraciones

**Después (con v2.0):**
- ⏱️ 2 minutos editando `config.py`
- 🚀 3 líneas, nada más
- 😊 Claro y automático

---

**¿Lista para enviar certificados? ¡Vamos!** 🎓
