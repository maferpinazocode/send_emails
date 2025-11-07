"""
Configuration file for Certificate Automation System
Simple setup: Fill in these values and run automatization.py
"""

# ==================== QUICK CONFIG ====================
# Only modify these 3 values to deploy a new course!

PREFIX = "imbtain5sprod09251"  # Course ID prefix (e.g., imbtain5sprod09251)
COURSE_NAME_ES = "5s aplicado a Producción"  # Course name in Spanish
COURSE_NAME_EN = "5s in Production"  # Course name in English

# ⚠️  IMPORTANT: Ensure credentials below are correct before running!

# ==================== EMAIL CONFIGURATION ====================
SMTP_SERVER = "mail.imbinstitute.com"
SMTP_PORT = 465
SENDER_EMAIL = "certificados@imbinstitute.com"
SENDER_PASSWORD = "your-password-here"
SENDER_NAME = "IMB Institute"

# ==================== APPLICATION SETTINGS ====================
TEST_MODE = False  # True = send to TEST_EMAIL only, False = send to all students
TEST_EMAIL = "fernandagrant18@gmail.com"
LOG_FILE = "envio_certificados.log"
EXCEL_FILE = "certificados.xlsx"

# ==================== AI CONFIGURATION ====================
# OpenAI API key for auto-generating descriptions
OPENAI_API_KEY = "sk-your-api-key-here"  # Get from https://platform.openai.com/api-keys

# ==================== DO NOT MODIFY BELOW ====================
# These are derived from the above settings

MODULE_NAME = COURSE_NAME_ES
COURSE_NAME_ENGLISH = COURSE_NAME_EN

__all__ = [
    'PREFIX',
    'COURSE_NAME_ES',
    'COURSE_NAME_EN',
    'SMTP_SERVER',
    'SMTP_PORT',
    'SENDER_EMAIL',
    'SENDER_PASSWORD',
    'SENDER_NAME',
    'TEST_MODE',
    'TEST_EMAIL',
    'LOG_FILE',
    'EXCEL_FILE',
    'OPENAI_API_KEY',
    'MODULE_NAME',
    'COURSE_NAME_ENGLISH',
]
