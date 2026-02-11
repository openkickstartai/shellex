"""Safety checks for shell commands."""
import re
from enum import Enum
from typing import List


class SafetyLevel(Enum):
    SAFE = "safe"
    NORMAL = "normal"
    DANGEROUS = "dangerous"


DANGEROUS_PATTERNS: List[str] = [
    r"\brm\s+(-[a-zA-Z]*[rR][a-zA-Z]*f|-[a-zA-Z]*f[a-zA-Z]*[rR])[a-zA-Z]*\s",
    r"\brm\s+--recursive\s+--force",
    r"\brm\s+--force\s+--recursive",
    r"\bdd\s+",
    r"\bmkfs\b",
    r"\b>\s*/dev/",
    r"\bchmod\s+-R\s+777",
    r":(){ :|:& };:",
    r"\bshutdown\b",
    r"\breboot\b",
]

WARNING_PATTERNS: List[str] = [
    r"\brm\b",
    r"\bmv\b.*\/",
    r"\bsudo\b",
    r"\bkill\b",
    r"\bpkill\b",
]


def check_safety(command: str) -> SafetyLevel:
    """Check if a command is potentially dangerous."""
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, command):
            return SafetyLevel.DANGEROUS
    for pattern in WARNING_PATTERNS:
        if re.search(pattern, command):
            return SafetyLevel.NORMAL
    return SafetyLevel.SAFE
