import logging
import requests
from colorama import init, Fore, Style
from logging.handlers import RotatingFileHandler

# Inicializar colorama
init()

# ================== CONFIGURACIÓN ==================
TELEGRAM_BOT_TOKEN = "7782114763:AAG95EeBfC6Wd7rSEa88cidvMCTX9lkBQUE"
TELEGRAM_CHAT_ID = "-1002513850512"  # Grupo de Telegram

# ================== HANDLER PARA TELEGRAM ==================
class TelegramHandler(logging.Handler):
    def emit(self, record):
        msg = self.format(record)
        if len(msg) > 4000:
            msg = msg[:4000] + "..."

        url = f"https://api.telegram.org/bot {TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': f"🚨 LOG: {msg}",
            'parse_mode': 'HTML'
        }
        try:
            response = requests.post(url, data=data, timeout=10)
            if response.status_code != 200:
                print(f"Error Telegram: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error al enviar a Telegram: {e}")

# ================== FORMATO COLOREADO ==================
class ColoredFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT
    }

    def format(self, record):
        message = super().format(record)
        color = self.COLORS.get(record.levelno, Fore.WHITE)
        return f"{color}{message}{Style.RESET_ALL}"

# ================== CONFIGURACIÓN DEL LOGGER ==================
def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Formato con detalles
    detailed_format = '%(asctime)s | %(filename)s:%(lineno)d | %(funcName)s | %(levelname)s | %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'

    # Formato coloreado para consola
    console_formatter = ColoredFormatter(detailed_format, datefmt=date_format)

    # Formato plano para archivo y Telegram
    plain_formatter = logging.Formatter(detailed_format, datefmt=date_format)

    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    # Handler para archivo (rotación)
    file_handler = RotatingFileHandler(
        'app.log',
        maxBytes=1_000_000,  # 1MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(plain_formatter)

    # Handler para Telegram
    telegram_handler = TelegramHandler()
    telegram_handler.setLevel(logging.WARNING)
    telegram_handler.setFormatter(plain_formatter)

    # Limpiar handlers previos
    logger.handlers.clear()

    # Añadir handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(telegram_handler)

    return logger

# ================== EJECUCIÓN ==================
if __name__ == "__main__":
    logger = setup_logger()

    logger.info("Iniciando aplicación...")
    logger.warning("¡Prueba de Telegram!")  # Este se envía a Telegram

    try:
        1 / 0  # Forzar error
    except Exception as e:
        logger.exception("Ocurrió una excepción")

    logger.info("Pruebas completadas")