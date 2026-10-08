# CI/CD Pipeline

## Stack
- **mise** — manages Python 3.11 + uv
- **uv** — dependency management and virtual environment
- **poethepoet (poe)** — task runner (`poe_tasks.toml`)
- **Snowflake CLI** — snowpark deploy / execute (installed via `Snowflake-Labs/snowflake-cli-action@v2` GitHub Action)

---

## Local Development

Install dependencies locally using:
```bash
pip install -r requirements_local.txt
```

`requirements_local.txt` is for local use only and is never used by the CI/CD pipeline.

---

## CI (Continuous Integration)

Triggers on every push to `main` and on pull requests.
No Snowflake credentials required — runs lint and tests only.

| Step | Command | What it does |
|------|---------|--------------|
| Setup | `jdx/mise-action@v2` | Installs Python 3.11 + uv |
| Install | `uv sync --all-groups` | Installs all dependencies (main + dev) from `pyproject.toml` |
| Lint | `uv run poe lint` | Runs `ruff check .` to catch style/syntax errors |
| Test | `uv run poe test` | Runs `pytest tests/` to validate core behaviour |

---

## CD (Continuous Deployment)

Triggers only when CI completes successfully.
Writes `~/.snowflake/config.toml` from GitHub Secrets at runtime — no credentials stored in the repo.

| Step | Command | What it does |
|------|---------|--------------|
| Setup | `jdx/mise-action@v2` | Installs Python 3.11 + uv |
| Setup | `Snowflake-Labs/snowflake-cli-action@v2` | Installs the Snowflake CLI |
| Configure | writes `~/.snowflake/config.toml` | Builds the CLI connection config from GitHub Secrets |
| Install | `uv sync --all-groups` | Installs all dependencies from `pyproject.toml` |
| Deploy | `uv run poe snow-deploy-dev` | Runs `_deploy.py`, which: (1) writes a temporary `requirements.txt` with `snowflake-snowpark-python`, (2) runs `snow snowpark build` to resolve Anaconda packages into `requirements.snowflake.txt`, (3) runs `snow snowpark deploy --replace` to upload `main.py` and create/replace the `SNOWFLAKE_AGENT_JOB` stored procedure with the correct `PACKAGES` clause, (4) cleans up both temp files |
| Run | `uv run poe snow-run-dev` | Calls `DEMO_DB.DEMO_SCHEMA.SNOWFLAKE_AGENT_JOB()` and returns its output |

### Viewing procedure output
1. Go to **Snowsight** → **Data** → **Databases** → `DEMO_DB` → **Schemas** → `DEMO_SCHEMA` → **Procedures**
2. Find `SNOWFLAKE_AGENT_JOB`
3. Click **Run** or query directly: `CALL DEMO_DB.DEMO_SCHEMA.SNOWFLAKE_AGENT_JOB();`

---

## One-time Snowflake Setup

Run once in Snowsight before the first deploy:
```sql
CREATE DATABASE IF NOT EXISTS DEMO_DB;
CREATE SCHEMA IF NOT EXISTS DEMO_DB.DEMO_SCHEMA;
CREATE STAGE IF NOT EXISTS DEMO_DB.DEMO_SCHEMA.DEV_STAGE;
```

---

## Required GitHub Secrets

Go to **Settings → Secrets and variables → Actions** in the GitHub repo and add:

| Secret | Description |
|--------|-------------|
| `SNOWFLAKE_ACCOUNT` | Account identifier e.g. `xy12345.us-east-1` |
| `SNOWFLAKE_USER` | Snowflake username |
| `SNOWFLAKE_PASSWORD` | Snowflake password or service account password |
| `SNOWFLAKE_WAREHOUSE` | Warehouse to use e.g. `COMPUTE_WH` |
| `SNOWFLAKE_DATABASE` | Target database e.g. `DEMO_DB` |
| `SNOWFLAKE_SCHEMA` | Target schema e.g. `DEMO_SCHEMA` |
| `SNOWFLAKE_ROLE` | Role with privileges to create stages and procedures |
