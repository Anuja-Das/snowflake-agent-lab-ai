import subprocess
import sys
from pathlib import Path


def main():
    req = Path("requirements.txt")
    snowflake_req = Path("requirements.snowflake.txt")

    req.write_text("snowflake-snowpark-python\n")
    try:
        build = subprocess.run(["snow", "snowpark", "build"])
        if build.returncode != 0:
            sys.exit(build.returncode)
        result = subprocess.run(["snow", "snowpark", "deploy", "--replace"])
    finally:
        req.unlink(missing_ok=True)
        snowflake_req.unlink(missing_ok=True)

    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
