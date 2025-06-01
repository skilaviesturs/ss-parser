import logging
import os
from dotenv import load_dotenv

# Ielādē .env tikai ārpus Docker
def is_running_in_docker():
    try:
        if os.path.exists('/.dockerenv'):
            return True
        with open('/proc/1/cgroup', 'rt') as f:
            return 'docker' in f.read() or 'kubepods' in f.read()
    except Exception:
        return False

if not is_running_in_docker():
    load_dotenv(override=True)

# Nolasa un apstrādā LOGLEVEL vērtību
loglevel_raw = os.getenv("LOGLEVEL", "info")
levels = [lvl.strip().lower() for lvl in loglevel_raw.split(",") if lvl.strip()]

# Nosaka aktīvo log līmeni
active_level = logging.DEBUG if "debug" in levels else logging.INFO

# Konfigurē root logger
logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    level=active_level,
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)
logger.info(f"[logger] Log level set to: {'DEBUG' if active_level == logging.DEBUG else 'INFO'}")
