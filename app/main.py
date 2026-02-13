import signal
import sys
import logging
from app.config import settings
from app.collector.listener import NetFlowListener

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def handle_sigterm(signum, frame):
    logger.info("Received termination signal. Exiting.")
    sys.exit(0)

def main():
    signal.signal(signal.SIGTERM, handle_sigterm)
    signal.signal(signal.SIGINT, handle_sigterm)
    
    logger.info("Starting NetFlow Observer Service...")
    
    try:
        listener = NetFlowListener(settings.COLLECTOR_HOST, settings.COLLECTOR_PORT)
        listener.start()
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
