import time
import os
from logger import logger
from parser_main import run_parser
from config import PARSE_INTERVAL_MINUTES

def main():
    while True:
        logger.info("[main] Running parser...")
        run_parser()
        logger.info(f"[main] Sleeping for {PARSE_INTERVAL_MINUTES} minutes...")
        time.sleep(PARSE_INTERVAL_MINUTES * 60)

if __name__ == "__main__":
    main()