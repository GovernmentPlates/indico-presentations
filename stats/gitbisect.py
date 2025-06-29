#!/usr/bin/env python3
import sys
from pathlib import Path

lang = sys.argv[1]

if Path(f'/home/tomas/dev/indico/indico/translations/{lang}').exists():
    sys.exit(1)
else:
    sys.exit(0)
