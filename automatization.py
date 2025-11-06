# =========================================================
# 📧 Envío de certificados IMB Institute
# Versión adaptada que SÍ funciona
# =========================================================

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import pandas as pd
from datetime import datetime

# ===================== CONFIGURACIÓN =====================

# Datos de acceso (configuración que funciona)
SENDER_EMAIL = "certification@imbinstitute.com"
PASSWORD = "@imbinstitute.com"
SMTP_SERVER = "mail.imbinstitute.com"
SMTP_PORT = 465

# Archivos
EXCEL_FILE = "certificados.xlsx"
PDF_FOLDER = "PDFs"
HTML_FOLDER = "HTMLs"
BADGE_FOLDER = "badges"  # Carpeta con las insignias
LOG_FILE = "envio_certificados.log"  # Archivo de registro

# Nombre del módulo/curso (texto que queremos mostrar en el asunto)
MODULE_NAME = "Inteligencia Artificial y Automatización para la Gestión del Talento"

BADGES = {
    "Master": os.path.join(BADGE_FOLDER, "certified-master.png"),
    "Advanced": os.path.join(BADGE_FOLDER, "certified-advanced.png"),
    "Fundamental": os.path.join(BADGE_FOLDER, "certified-fundamental.png")
}

# ⚠️ Modo prueba: solo envía la fila 2 del Excel
TEST_MODE = False  # ✅ CAMBIAR A False PARA ENVIAR A TODOS
TEST_EMAIL = "fernandagrant18@gmail.com"

# =========================================================


def log_envio(mensaje, nombre_alumno="", email="", estado=""):
    """Escribe un registro en el archivo de log"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{timestamp}] {mensaje}"
    if nombre_alumno:
        linea += f" | Alumno: {nombre_alumno}"
    if email:
        linea += f" | Email: {email}"
    if estado:
        linea += f" | Estado: {estado}"
    
    # Escribir en archivo de log
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(linea + "\n")
    except Exception as e:
        print(f"   ⚠️ Error escribiendo log: {e}")
    
    # También mostrar en pantalla
    print(linea)


def get_html_template(level):
    """Carga la plantilla HTML según el nivel"""
    filename = f"Certificado-{level.lower()}.html"
    path = os.path.join(HTML_FOLDER, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"⚠️ No se encontró la plantilla: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def build_certificate_path(pdf_name):
    """Construye la ruta del certificado PDF con el formato correcto: Certificado-{ID}.pdf"""
    # Si el nombre no contiene "Certificado-", agregarlo
    if not pdf_name.lower().startswith("certificado-"):
        pdf_name = f"Certificado-{pdf_name}"
    
    # Agregar extensión .pdf si no la tiene
    if not pdf_name.lower().endswith(".pdf"):
        pdf_name = pdf_name + ".pdf"
    
    return os.path.join(PDF_FOLDER, pdf_name)


def send_email(student, html_body, pdf_path, badge_path):
    """Envía un correo con certificado + insignia"""

    # Determinar destinatario (modo prueba o real)
    recipient = TEST_EMAIL if TEST_MODE else student["EMAIL"]

    # Crear mensaje básico
    msg = MIMEMultipart()
    # Usar el nombre del módulo para el asunto. Si MODULE_NAME está vacío, usar el nivel como fallback.
    subject_module = MODULE_NAME if MODULE_NAME else student.get('NIVEL', '')
    msg['Subject'] = f"🎖️ ¡Logro Conseguido! Certificado en {subject_module}"
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient

    # Personalizar HTML con los datos del alumno (solo la plantilla personalizada)
    html_personalizado = html_body.replace("{{NOMBRE_ALUMNO}}", student['NOMBRE ALUMNO'])
    html_personalizado = html_personalizado.replace("{{NIVEL}}", student['NIVEL'])
    html_personalizado = html_personalizado.replace("{{ID}}", str(student['ID']))
    html_personalizado = html_personalizado.replace("{{WEB}}", str(student['WEB']))
    primer_nombre = student['NOMBRE ALUMNO'].split()[0]
    html_personalizado = html_personalizado.replace("{{PRIMER_NOMBRE}}", primer_nombre)
    msg.attach(MIMEText(html_personalizado, "html"))

    # Adjuntar certificado PDF
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(pdf_path)}")
        msg.attach(part)
        print(f"   ✅ PDF adjuntado: {os.path.basename(pdf_path)}")
    else:
        print(f"   ⚠️ PDF no encontrado: {pdf_path}")
        return False

    # Adjuntar insignia
    if badge_path and os.path.exists(badge_path):
        with open(badge_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(badge_path)}")
        msg.attach(part)
        print(f"   ✅ Badge adjuntado: {os.path.basename(badge_path)}")
    else:
        print(f"   ⚠️ Badge no encontrado: {badge_path}")

    # Enviar correo
    try:
        print(f"   🔌 Conectando al servidor...")
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            server.login(SENDER_EMAIL, PASSWORD)
            server.send_message(msg)
        print(f"   ✅ Correo enviado a {recipient}")
        log_envio(f"✅ ENVIADO", nombre_alumno=student['NOMBRE ALUMNO'], email=recipient, estado="Éxito")
        return True
    except Exception as e:
        print(f"   ❌ Error enviando correo: {e}")
        log_envio(f"❌ ERROR", nombre_alumno=student['NOMBRE ALUMNO'], email=recipient, estado=str(e))
        return False


def main():
    """Función principal"""
    
    print("=" * 60)
    print("📧 SISTEMA DE ENVÍO DE CERTIFICADOS - IMB INSTITUTE")
    print("=" * 60)
    
    # Verificar modo
    if TEST_MODE:
        print(f"⚠️  MODO PRUEBA ACTIVADO")
        print(f"   Todos los correos se enviarán a: {TEST_EMAIL}")
        print(f"   Para enviar a los alumnos reales, cambiar TEST_MODE = False")
    else:
        print(f"✅ MODO PRODUCCIÓN")
        print(f"   Los correos se enviarán a los emails de los alumnos")
    
    print("=" * 60)
    
    # Leer Excel
    try:
        df = pd.read_excel(EXCEL_FILE)
        # Normalizar y mapear columnas comunes para tolerar variaciones del Excel
        original_cols = list(df.columns)
        cols_stripped = [str(c).strip() for c in original_cols]
        df.columns = cols_stripped

        # Mapeo de alias a nombres esperados
        alias_map = {
            'NOMBRE ALUMNO': ['NOMBRE ALUMNO', 'NOMBRE', 'Nombre', 'NOMBRE_ALUMNO', 'NOMBREALUMNO'],
            'EMAIL': ['EMAIL', 'Email', 'email'],
            'NIVEL': ['NIVEL', 'Nivel', 'nivel'],
            'PDF': ['PDF', 'Pdf', 'pdf'],
            'ID': ['ID', 'Id', 'id'],
            'WEB': ['WEB', 'Web', 'web']
        }

        rename_map = {}
        for canonical, candidates in alias_map.items():
            for cand in candidates:
                if cand in df.columns:
                    rename_map[cand] = canonical
                    break

        if rename_map:
            df = df.rename(columns=rename_map)

        print(f"\n📊 {len(df)} registros encontrados en {EXCEL_FILE}")
        print(f"   Columnas detectadas: {list(df.columns)}")
    except Exception as e:
        print(f"❌ Error leyendo Excel: {e}")
        return
    
    # Procesar alumnos
    success_count = 0
    error_count = 0
    
    # Si está en modo prueba, procesar solo la fila 2
    if TEST_MODE:
        print(f"\n🧪 Modo prueba: enviando solo la fila 2 del Excel...\n")
        # Enviar fila 2 (índice 1)
        if len(df) >= 2:
            rows = [df.iloc[1]]
        else:
            print("   ⚠️ El Excel tiene menos de 2 filas. Usando la primera.")
            rows = [df.iloc[0]]
    else:
        rows = [row for _, row in df.iterrows()]

    # Código que ya no se usa (eliminado para simplificar)
    if False:  # Desactivado
        pass

    print(f"\n🚀 Procesando {len(rows)} fila(s)...\n")
    
    for idx, row in enumerate(rows, 1):
        print(f"\n{'='*60}")
        print(f"📧 Procesando {idx}/{len(rows)}")
        print(f"{'='*60}")
        
        # Extraer datos del alumno
        student = {
            "NOMBRE ALUMNO": row["NOMBRE ALUMNO"],
            "EMAIL": row["EMAIL"],
            "NIVEL": row["NIVEL"],
            "PDF": row["PDF"],
            "ID": row["ID"],
            "WEB": row["WEB"]
        }
        
        print(f"👤 Alumno: {student['NOMBRE ALUMNO']}")
        print(f"📧 Email: {student['EMAIL']}")
        print(f"🎓 Nivel: {student['NIVEL']}")
        print(f"📄 PDF: {student['PDF']}")
        print(f"🆔 ID: {student['ID']}")
        print(f"🌐 URL: {student['WEB']}")
        
        # Validar nivel
        nivel = str(student["NIVEL"]).strip()
        if nivel not in ["Master", "Advanced", "Fundamental"]:
            print(f"⏭️  Nivel no válido ({nivel}), saltando...")
            error_count += 1
            continue
        
        # Obtener plantilla HTML
        try:
            html_body = get_html_template(nivel)
        except FileNotFoundError as e:
            print(f"   ❌ {e}")
            error_count += 1
            continue
        
        # Construir rutas
        # Si la columna PDF está vacía o es NaN, usar el ID como nombre del PDF (fallback)
        pdf_value = student.get("PDF")
        try:
            # Pandas puede traer NaN como float
            if pd.isna(pdf_value) or str(pdf_value).strip().lower() == "nan" or str(pdf_value).strip() == "":
                pdf_value = str(student.get("ID"))
        except Exception:
            # En caso de cualquier error, usar el ID
            pdf_value = str(student.get("ID"))

        pdf_path = build_certificate_path(pdf_value)
        badge_path = BADGES.get(nivel)
        
        # Enviar correo
        if send_email(student, html_body, pdf_path, badge_path):
            success_count += 1
        else:
            error_count += 1
        
        # Pausa entre envíos (solo en modo producción)
        if not TEST_MODE and idx < len(rows):
            import time
            print("   ⏳ Esperando 2 segundos...")
            time.sleep(2)
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN FINAL")
    print("=" * 60)
    print(f"✅ Enviados correctamente: {success_count}")
    print(f"❌ Errores: {error_count}")
    print(f"📧 Total procesados: {success_count + error_count}")
    print(f"📁 Registro guardado en: {LOG_FILE}")
    
    # Guardar resumen en log
    log_envio("\n" + "=" * 60)
    log_envio("📊 RESUMEN FINAL DEL ENVÍO")
    log_envio("=" * 60)
    log_envio(f"✅ Enviados correctamente: {success_count}")
    log_envio(f"❌ Errores: {error_count}")
    log_envio(f"📧 Total procesados: {success_count + error_count}")
    log_envio("=" * 60)
    
    if TEST_MODE:
        print("\n⚠️  Recuerda: estás en MODO PRUEBA")
        print("   Para enviar a todos los alumnos, cambiar TEST_MODE = False")


# Ejecutar
if __name__ == "__main__":
    main()