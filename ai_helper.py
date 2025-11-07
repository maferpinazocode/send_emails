"""
AI Helper Module - Generates certificate descriptions using OpenAI API
"""

import openai
import os
from config import OPENAI_API_KEY

# Initialize OpenAI
openai.api_key = OPENAI_API_KEY


def generate_certificate_description(course_title_en: str) -> str:
    """
    Generate a professional certificate description using AI.
    
    Args:
        course_title_en: Course title in English (e.g., "5s in Production")
    
    Returns:
        str: Professional certificate description for LinkedIn
    """
    
    if not OPENAI_API_KEY or OPENAI_API_KEY == "sk-your-api-key-here":
        print("⚠️  OpenAI API key not configured. Using generic description.")
        return generate_generic_description(course_title_en)
    
    try:
        prompt = f"""Generate a professional LinkedIn certificate description (1-2 sentences, max 150 words) for a certification titled: "{course_title_en}"

The description should:
- Be concise and professional
- List 3-4 key competencies gained
- Use commas to separate competencies
- Be suitable for LinkedIn credential
- Emphasize practical application and professional development

Format:
Certification validating competencies in [competency 1], [competency 2], [competency 3], and [competency 4] in {course_title_en}.

Only provide the description, no additional text."""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional certification writer for an educational institute."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )
        
        description = response.choices[0].message.content.strip()
        print(f"✅ Generated description: {description}")
        return description
        
    except Exception as e:
        print(f"❌ Error generating description with AI: {e}")
        return generate_generic_description(course_title_en)


def generate_generic_description(course_title_en: str) -> str:
    """
    Generate a generic description if API is not available.
    
    Args:
        course_title_en: Course title in English
    
    Returns:
        str: Generic professional description
    """
    return f"Certification validating competencies in {course_title_en} and professional practices."


def generate_html_templates(course_name_es: str, course_name_en: str, description: str) -> tuple:
    """
    Generate three HTML email templates (Master, Advanced, Fundamental).
    
    Args:
        course_name_es: Course name in Spanish
        course_name_en: Course name in English
        description: Certificate description
    
    Returns:
        tuple: (master_html, advanced_html, fundamental_html)
    """
    
    base_template = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta charset="UTF-8">
    <title>Certified {{NIVEL}} - IMB Institute</title>
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
                           ¡Hola, {{PRIMER_NOMBRE}}! 👑</b><br /><br />
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
    
    # All three templates are the same (level differentiation happens in email body)
    return (base_template, base_template, base_template)


if __name__ == "__main__":
    # Test the description generator
    test_description = generate_certificate_description("5s in Production")
    print(f"\nGenerated Description:\n{test_description}")
