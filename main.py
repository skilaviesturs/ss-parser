import time
from logger import logger
from parser_main import run_parser
from config import PARSE_INTERVAL_MINUTES

def main():
    while True:
        logger.info("[main] Running parser...")
        start_time = time.time()

        try:
            run_parser()
        except Exception as e:
            logger.error(f"[runner] Parser crashed: {str(e)}")

        duration = round(time.time() - start_time, 2)
        logger.info(f"[main] Parser finished in {duration} seconds.")
        logger.info(f"[main] Sleeping for {PARSE_INTERVAL_MINUTES} minutes...")
        time.sleep(PARSE_INTERVAL_MINUTES * 60)

if __name__ == "__main__":
    main()
