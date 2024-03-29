import json
import os
from typing import Final, List

from dotenv import load_dotenv

load_dotenv()

TOKEN: Final[str] = os.getenv('TELEGRAM')
ADMINS: Final[List[int]] = json.loads(os.getenv('ADMINS'))
GROUP: Final[int] = int(os.getenv('GROUP'))

BLACKLIST = (
    "or[kc]",
    "hohol",
    "hurensohn",
    "arschloch",
    "fick(en|t)",
    "nazi",
    "ludwigshafen ",
    "rashist",
    "putler",
)
