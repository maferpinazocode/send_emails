# 🎓 Certificate Automation System - IMB Institute

Automated certificate distribution system that sends personalized emails with PDFs and badges to students across multiple courses.

## 📋 Features

- ✅ **Automated Email Sending**: Sends personalized certificates via SMTP
- ✅ **Multi-Course Support**: Switch between courses with simple configuration
- ✅ **Excel Integration**: Reads student data from Excel files
- ✅ **File Attachments**: Includes PDFs and badge images with each email
- ✅ **Certification Levels**: Supports Master, Advanced, and Fundamental levels
- ✅ **Bilingual Templates**: Spanish body text + English descriptions
- ✅ **Test Mode**: Safe testing with single test email before production
- ✅ **Logging System**: Tracks all sends with timestamps and status
- ✅ **Error Handling**: Comprehensive error reporting and recovery

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- pandas library
- SMTP server credentials (mail.imbinstitute.com:465)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/certificate-automation.git
cd certificate-automation
```

2. Install dependencies:
```bash
pip install pandas
```

3. Create `.env` file (use `.env.example` as template):
```bash
cp .env.example .env
```

4. Configure your email credentials in `automatization.py` (lines 16-20).

## 📁 Project Structure

```
certificate-automation/
├── automatization.py          # Main certificate distribution engine
├── certificados.xlsx          # Excel file with student data
├── HTMLs/                     # Email templates
│   ├── Certificado-master.html
│   ├── Certificado-advanced.html
│   └── Certificado-fundamental.html
├── PDFs/                      # Student certificates (Certificado-{ID}.pdf)
├── badges/                    # Badge images per level
│   ├── certified-master.png
│   ├── certified-advanced.png
│   └── certified-fundamental.png
├── qrs/                       # QR codes (structure ready)
└── envio_certificados.log     # Send log file
```

## ⚙️ Configuration

Edit `automatization.py` (lines 28-40):

```python
# Module/Course name in Spanish
MODULE_NAME = "Inteligencia Artificial y Automatización para la Gestión del Talento"

# Test mode: True = send to TEST_EMAIL only, False = send to all students
TEST_MODE = False

# Test email for safe testing
TEST_EMAIL = "your-test-email@example.com"

# Log file path
LOG_FILE = "envio_certificados.log"
```

### SMTP Configuration (lines 16-20)

```python
SMTP_SERVER = "mail.imbinstitute.com"
SMTP_PORT = 465
SENDER_EMAIL = "your-email@imbinstitute.com"
SENDER_PASSWORD = "your-password"
SENDER_NAME = "IMB Institute"
```

## 📊 Excel File Format

The `certificados.xlsx` file should contain columns:

| Column | Description |
|--------|-------------|
| NOMBRE ALUMNO | Student's first name |
| ID | Certificate ID (e.g., imbtainiarrhh09251) |
| WEB | URL for credential verification |
| NIVEL | Certification level: Master, Advanced, or Fundamental |
| PDF | PDF filename (optional, uses ID as fallback) |
| EMAIL | Student email address |
| FECHA | Date field |
| PAGO | Payment status |

## 🔄 Usage

### Test Mode (Send to Single Email)

1. Edit `automatization.py`:
```python
TEST_MODE = True
TEST_EMAIL = "your-test-email@example.com"
```

2. Run:
```bash
python automatization.py
```

### Production Mode (Send to All Students)

1. Edit `automatization.py`:
```python
TEST_MODE = False
```

2. Run:
```bash
python automatization.py
```

The script will:
- ✅ Load student data from Excel
- ✅ Validate certification levels
- ✅ Personalize email templates
- ✅ Attach PDFs and badges
- ✅ Send emails with 2-second delays
- ✅ Log all sends with timestamps and status

## 📝 How to Add a New Course

1. **Prepare files**:
   - Add student data to `certificados.xlsx` with new sheet or rows
   - Add PDFs to `PDFs/` folder named `Certificado-{ID}.pdf`
   - Ensure badge files exist: `badges/certified-master.png`, etc.

2. **Update configuration**:
   ```python
   MODULE_NAME = "Your Course Name in Spanish"
   ```

3. **Update HTML templates** (`HTMLs/` folder):
   - Replace course name in templates
   - Update English certificate title
   - Update LinkedIn description
   - Keep personalization placeholders: {{PRIMER_NOMBRE}}, {{NIVEL}}, {{ID}}, {{WEB}}

4. **Test & Deploy**:
   ```python
   TEST_MODE = True  # Test first
   ```
   Then switch to `TEST_MODE = False` for production

## 📧 Email Template System

Templates use personalization placeholders:

| Placeholder | Replaced With |
|---|---|
| {{PRIMER_NOMBRE}} | Student's first name |
| {{NIVEL}} | Certification level (Master/Advanced/Fundamental) |
| {{ID}} | Certificate ID |
| {{WEB}} | Verification URL |

Three templates for each level:
- `Certificado-master.html` - Master level
- `Certificado-advanced.html` - Advanced level  
- `Certificado-fundamental.html` - Fundamental level

## 📊 Deployment History

Successfully deployed to:
- ✅ Planeación Estratégica y Control de Proyectos (18 students)
- ✅ Planificación Financiera y Control Interno Corporativo (44 students)
- ✅ Gestión de Riesgos, Calidad y Partes Interesadas (18 students)
- ✅ Inteligencia Artificial y Automatización para la Gestión del Talento (65 students)

**Total Sent**: 145 certificates | **Success Rate**: 100%

## 📋 Logging

All sends are logged to `envio_certificados.log` with:
- Timestamp
- Student name
- Student email
- Certificate ID
- Status (✅ Success or ❌ Error)
- Error details (if any)

## 🔐 Security Notes

⚠️ **Important**: 
- Keep email credentials secure (.env file is in .gitignore)
- Never commit `.env` file with actual credentials
- Use environment variables in production

## 🔜 Planned Features

- Database integration (Neon PostgreSQL + Prisma ORM)
- Certificate tracking and audit logs
- Resend functionality for failed emails
- Bulk import from multiple Excel files
- QR code generation and inclusion

## 👨‍💼 Author

IMB Institute - Academic Department

## 📄 License

Internal use only - IMB Institute

---

**Last Updated**: November 6, 2025  
**Status**: Production Ready ✅
