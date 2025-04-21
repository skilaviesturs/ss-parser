import time
import os
from parser_main import run_parser
from config import PARSE_INTERVAL_MINUTES

def main():
    while True:
        print("Running parser...")
        run_parser()
        print(f"Sleeping for {PARSE_INTERVAL_MINUTES} minutes...")
        time.sleep(PARSE_INTERVAL_MINUTES * 60)

if __name__ == "__main__":
    main()