# =========================================================
# 📧 Envío de certificados IMB Institute - v2.0
# Versión mejorada con:
# - Configuración simple en config.py
# - Generación automática de descripciones con IA
# - Filtro por PAGO (FALSE/TRUE)
# - Generación automática de templates
# =========================================================

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import pandas as pd
from datetime import datetime
import time

# Import from config
from config import (
    PREFIX,
    COURSE_NAME_ES,
    COURSE_NAME_EN,
    SMTP_SERVER,
    SMTP_PORT,
    SENDER_EMAIL,
    SENDER_PASSWORD,
    SENDER_NAME,
    TEST_MODE,
    TEST_EMAIL,
    LOG_FILE,
    EXCEL_FILE,
)

# Try to import AI helper (optional)
try:
    from ai_helper import generate_certificate_description, generate_html_templates
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("⚠️  Warning: OpenAI not available. Using generic descriptions.")

# ===================== SETUP =====================

PDF_FOLDER = "PDFs"
HTML_FOLDER = "HTMLs"
BADGE_FOLDER = "badges"

BADGES = {
    "Master": os.path.join(BADGE_FOLDER, "certified-master.png"),
    "Advanced": os.path.join(BADGE_FOLDER, "certified-advanced.png"),
    "Fundamental": os.path.join(BADGE_FOLDER, "certified-fundamental.png")
}

# ===================== FUNCTIONS =====================


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
    
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(linea + "\n")
    except Exception as e:
        print(f"   ⚠️  Error escribiendo log: {e}")
    
    print(linea)


def generate_html_template(level, course_name_es, course_name_en, description):
    """Genera una plantilla HTML dinamicamente"""
    base = f"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta charset="UTF-8">
    <title>Certified {{{{NIVEL}}}} - IMB Institute</title>
<meta HTTP-EQUIV="Content-Type" content="text/html; charset=iso-8859-1" />
</head>

<body>

<table width="100%" border="0" cellspacing="0" cellpadding="0">
  <tr>
    <td align="center" valign="top" style="background-color:#F2F2F2;"><br><br>
      <table width="592" border="0" cellspacing="0" cellpadding="0" align="center" style="font-family:Arial, Helvetica, sans-serif">
           <tr>
              <td width="600" height="80" align="center" bgcolor="#252425">
              <img src="https://imbinstitute.com/wp-content/uploads/2025/05/logo_simple_imb.png" height="50" alt=""/>
              </td>
           </tr>
           <tr style="color:#1d1d1d">
             <td>
               <table width="600px" height="300px" cellpadding="0" cellspacing="0" bgcolor="#252425">
                       <tr>
                         <td height="3"></td>
                       </tr>
                       <tr>
                         <td height="300" colspan="3" bgcolor="ffffff">
                          <img src="https://imbinstitute.com/mailer/imagen-alumnos-certificados-mailing.jpg" width="600" height="300" border="0">
                         </td>
                       </tr>
                 </table>
               <table width="600px" height="329" cellpadding="2" cellspacing="2" bgcolor="ffffff" style="font-size:14px; color:#1d1d1d; line-height:180%">
                      <tr>
                         <td width="30" rowspan="7">
                         </td>
                          <td height="15"></td>
                        <td width="30" rowspan="7" >
                        </td>
                 </tr>
                      <tr>
                         <td height="60" align="lef" style="font-size:26px; color:#252425; line-height:120%">
                           <b><br />
                           ¡Hola, {{{{PRIMER_NOMBRE}}}}! 👑</b><br /><br />
                        </td>
                 </tr>
                      <tr>
                        <td valign="top">
                          Recibe un cordial saludo y a la vez felicitarte por haber culminado exitosamente el módulo <b>{course_name_es},</b> demostrando tu compromiso y esfuerzo. Estamos seguros de que los conocimientos adquiridos serán de gran valor en tu desarrollo profesional.✨<br />
                          <br />
                        
                        <b>Te enviamos tu certificado como documento adjunto.</b><br />
                        ✅ Certified {{{{NIVEL}}}} in {course_name_en} (PDF)<br><br />
							
                         </td>
                      </tr>
						<tr style="color:#1d1d1d">
                        <td valign="top" style="font-size:12px; color:#1d1d1d"><hr>
							Additionally, we attach your certification badge and the manual to configure it on your LinkedIn (https://imbinstitute.com/linkedin/Manual-para-certificaciones-en-linkedin-IMB.pdf). Here are the contents you need to add to its configuration.<br />
							
                        &bull; <b>Name:</b> {{{{NIVEL}}}} in {course_name_en}.<br>
						&bull; <b>Credential ID:</b> {{{{ID}}}}<br />
						&bull; <b>Credential URL:</b> {{{{WEB}}}}<br>
                        &bull; <b>Title:</b> Certified {{{{NIVEL}}}} in {course_name_en}.<br />
                        &bull; <b>Description:</b> {description}<hr><br />
							</td>
                      </tr>
				   <tr>
                        <td>
							
							Agradecemos la confianza depositada en nuestra institución y esperamos que esta certificación sea un impulso valioso en tu desarrollo profesional.<br>
							
							
							💪¡Que el éxito te acompañe en cada nuevo desafío!<br><br>
                         </td>
                      </tr>
				   <tr>
                        <td valign="top">
							Atentamente<br><b>Departamento Académico.</b><br><br>
                         </td>
                      </tr>
               </table>
                 <table width="600px" height="3" cellpadding="2" cellspacing="2" bgcolor="#252425">
                 </table>
                 <table width="600px" height="100" cellpadding="0" cellspacing="0" bgcolor="#f2f2f2">
                      <tr>
                         <td width="10">
                         </td>
                          <td height="15"></td>
                        <td width="7" >
                        </td>
                   </tr>
                      <tr>
                        <td width="30"></td>
                         <td align="center" style="color:#706F6F; font-family:Tahoma, Geneva, sans-serif; font-size:12px; line-height:150%">
                        <b>IMB Institute SAC</b><br />
                          Urb. Alto de la Luna G-16, J. Luis Bustamante y R. - Arequipa, Perú / Tel&eacute;f: +51 919 077 226<br />
                <a href="http://www.imbinstitute.com" target="_blank"  style="color:#706F6F; text-decoration:none;">www.imbinstitute.com</a>
                        </td>
                         <td width="30">
                         </td>
                      </tr>
                      <tr>
                        <td width="10">
                        </td>
                        <td height="15">
                        </td>
                        <td width="7">
                        </td>
                      </tr>
                 </table>
                 
                 
           </tr>
        </table>
     <br>
    <br></td>
  </tr>
</table>
</body>
</html>"""
    
    return base


def get_html_template(level):
    """Carga la plantilla HTML según el nivel"""
    filename = f"Certificado-{level.lower()}.html"
    path = os.path.join(HTML_FOLDER, filename)
    if not os.path.exists(path):
        # Si no existe, generar una nueva
        print(f"⚠️  Template not found at {path}. Generating new template...")
        description = "Certification validating professional competencies and expertise."
        html = generate_html_template(level, COURSE_NAME_ES, COURSE_NAME_EN, description)
        os.makedirs(HTML_FOLDER, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        return html
    
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def build_certificate_path(pdf_name):
    """Construye la ruta del certificado PDF"""
    if not pdf_name.lower().startswith("certificado-"):
        pdf_name = f"Certificado-{pdf_name}"
    
    if not pdf_name.lower().endswith(".pdf"):
        pdf_name = pdf_name + ".pdf"
    
    return os.path.join(PDF_FOLDER, pdf_name)


def send_email(student, html_body, pdf_path, badge_path):
    """Envía un correo con certificado + insignia"""
    
    recipient = TEST_EMAIL if TEST_MODE else student["EMAIL"]
    
    msg = MIMEMultipart()
    subject = f"🎓 Tu certificado: {COURSE_NAME_ES}"
    msg["Subject"] = subject
    msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    msg["To"] = recipient
    
    # Personalizar el HTML
    html_body = html_body.replace("{{PRIMER_NOMBRE}}", student.get("NOMBRE ALUMNO", "Estudiante").split()[0])
    html_body = html_body.replace("{{NIVEL}}", student.get("NIVEL", ""))
    html_body = html_body.replace("{{ID}}", student.get("ID", ""))
    html_body = html_body.replace("{{WEB}}", student.get("WEB", ""))
    
    msg.attach(MIMEText(html_body, "html"))
    
    # Adjuntar PDF
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(pdf_path)}")
        msg.attach(part)
    else:
        log_envio(f"❌ PDF no encontrado: {pdf_path}", student.get("NOMBRE ALUMNO", ""), 
                 student.get("EMAIL", ""), "ERROR")
    
    # Adjuntar badge
    if badge_path and os.path.exists(badge_path):
        with open(badge_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(badge_path)}")
        msg.attach(part)
    
    # Enviar
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        
        log_envio(f"✅ Certificado enviado", student.get("NOMBRE ALUMNO", ""), 
                 recipient, "ÉXITO")
        return True
    
    except Exception as e:
        log_envio(f"❌ Error al enviar", student.get("NOMBRE ALUMNO", ""), 
                 recipient, f"ERROR: {str(e)}")
        return False


def normalize_column_names(df):
    """Normaliza los nombres de las columnas del DataFrame"""
    column_mapping = {
        "NOMBRE ALUMNO": ["NOMBRE ALUMNO", "Nombre Alumno", "nombre alumno", "NOMBRE"],
        "ID": ["ID", "id", "ID_CERTIFICADO"],
        "WEB": ["WEB", "web", "URL"],
        "NIVEL": ["NIVEL", "nivel", "LEVEL"],
        "PDF": ["PDF", "pdf"],
        "EMAIL": ["EMAIL", "email", "E-MAIL", "CORREO"],
        "FECHA": ["FECHA", "fecha"],
        "PAGO": ["PAGO", "pago", "PAYMENT"],
    }
    
    for standard_name, alternatives in column_mapping.items():
        for col in df.columns:
            if col in alternatives and col != standard_name:
                df = df.rename(columns={col: standard_name})
                break
    
    return df


def main():
    """Función principal"""
    
    print("\n" + "="*60)
    print("📧 IMB INSTITUTE - CERTIFICATE DISTRIBUTION SYSTEM v2.0")
    print("="*60)
    print(f"\n📌 CONFIGURATION:")
    print(f"   Course Prefix: {PREFIX}")
    print(f"   Course Name (ES): {COURSE_NAME_ES}")
    print(f"   Course Name (EN): {COURSE_NAME_EN}")
    print(f"   Mode: {'🧪 TEST (to {})'.format(TEST_EMAIL) if TEST_MODE else '📧 PRODUCTION'}")
    print("="*60 + "\n")
    
    # Generar descripción con IA si está disponible
    if AI_AVAILABLE:
        print("🤖 Generando descripción con IA...")
        description = generate_certificate_description(COURSE_NAME_EN)
    else:
        description = f"Certification validating competencies in {COURSE_NAME_EN}."
        print(f"📝 Using generic description: {description}")
    
    print("\n")
    
    # Leer Excel
    try:
        df = pd.read_excel(EXCEL_FILE)
    except FileNotFoundError:
        print(f"❌ Error: No se encontró {EXCEL_FILE}")
        log_envio(f"❌ Error: Archivo {EXCEL_FILE} no encontrado")
        return
    
    # Normalizar columnas
    df = normalize_column_names(df)
    
    # Filtrar por PAGO = TRUE (solo enviar a estudiantes que pagaron)
    print(f"📊 Total de registros en Excel: {len(df)}")
    
    # Asegurarse de que la columna PAGO existe
    if "PAGO" not in df.columns:
        print("⚠️  Columna 'PAGO' no encontrada. Enviando a todos los estudiantes.")
        df_to_send = df
    else:
        # Convertir PAGO a booleano (maneja TRUE, False, "True", etc.)
        df["PAGO"] = df["PAGO"].astype(str).str.lower().isin(["true", "1", "sí", "si", "yes"])
        df_to_send = df[df["PAGO"] == True]
        print(f"✅ Estudiantes con PAGO=TRUE: {len(df_to_send)}")
        print(f"❌ Estudiantes con PAGO=FALSE (serán ignorados): {len(df) - len(df_to_send)}")
    
    if len(df_to_send) == 0:
        print("⚠️  No hay estudiantes para procesar.")
        return
    
    print(f"\n🚀 Procesando {len(df_to_send)} estudiante(s)...\n")
    
    sent = 0
    errors = 0
    
    # Procesar cada estudiante
    for idx, (_, student) in enumerate(df_to_send.iterrows(), 1):
        print(f"\n[{idx}/{len(df_to_send)}] Procesando: {student.get('NOMBRE ALUMNO', 'N/A')}")
        
        # Validar datos obligatorios
        if pd.isna(student.get("EMAIL")) or not student.get("EMAIL"):
            log_envio(f"⚠️  Email vacío", str(student.get("NOMBRE ALUMNO", "")), "", "SKIPPED")
            errors += 1
            continue
        
        if pd.isna(student.get("NIVEL")) or not student.get("NIVEL"):
            log_envio(f"⚠️  Nivel vacío", str(student.get("NOMBRE ALUMNO", "")), 
                     str(student.get("EMAIL", "")), "SKIPPED")
            errors += 1
            continue
        
        # Obtener nivel y validar
        nivel = str(student.get("NIVEL", "")).strip().capitalize()
        if nivel not in BADGES:
            log_envio(f"⚠️  Nivel inválido: {nivel}", str(student.get("NOMBRE ALUMNO", "")), 
                     str(student.get("EMAIL", "")), "ERROR")
            errors += 1
            continue
        
        # Construir rutas de PDF y badge
        pdf_name = student.get("PDF") if not pd.isna(student.get("PDF")) else student.get("ID")
        pdf_path = build_certificate_path(str(pdf_name))
        badge_path = BADGES[nivel]
        
        # Cargar template HTML
        try:
            html_body = get_html_template(nivel)
        except Exception as e:
            log_envio(f"❌ Error cargando template: {e}", str(student.get("NOMBRE ALUMNO", "")), 
                     str(student.get("EMAIL", "")), "ERROR")
            errors += 1
            continue
        
        # Enviar email
        if send_email(student, html_body, pdf_path, badge_path):
            sent += 1
        else:
            errors += 1
        
        # Delay para no sobrecargar el servidor
        time.sleep(2)
    
    # Resumen final
    print("\n" + "="*60)
    print("📊 RESUMEN FINAL")
    print("="*60)
    print(f"✅ Enviados correctamente: {sent}")
    print(f"❌ Errores: {errors}")
    print(f"📧 Total procesados: {sent + errors}")
    print(f"📁 Registro guardado en: {LOG_FILE}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
