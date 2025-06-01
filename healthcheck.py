import os
import sys

# piemērs: pārbauda, vai SQLite datubāze eksistē
if not os.path.exists("/data/ss_entries.db"):
    print("DB missing!")
    sys.exit(1)

print("Healthy.")
