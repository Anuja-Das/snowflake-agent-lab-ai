import subprocess
import sys
from pathlib import Path


def main():
    req = Path("requirements.txt")
    req.write_text("snowflake-snowpark-python\n")
    try:
        result = subprocess.run(["snow", "snowpark", "deploy", "--replace"])
    finally:
        req.unlink(missing_ok=True)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
