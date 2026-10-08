# CI/CD Pipeline

## Stack
- **mise** — manages Python 3.11 + uv
- **uv** — dependency management and virtual environment
- **poethepoet (poe)** — task runner (`poe_tasks.toml`)
- **Snowflake CLI** — snowpark build / deploy / execute (installed via `Snowflake-Labs/snowflake-cli-action@v1` GitHub Action)

---

## CI (Continuous Integration)

Triggers on every push to `main` and on pull requests.

| Step | Command | What it does |
|------|---------|--------------|
| Setup | `jdx/mise-action@v2` | Installs Python 3.11 + uv |
| Setup | `Snowflake-Labs/snowflake-cli-action@v1` | Installs the Snowflake CLI |
| Install | `uv sync --all-groups` | Installs all dependencies (main + dev) |
| Lint | `uv run poe lint` | Runs `ruff check .` to catch style/syntax errors |
| Test | `uv run poe test` | Runs `pytest tests/` to validate core behaviour |
| Validate | `uv run poe snow-validate` | Builds the Snowpark artifact from `snowflake.yml` to catch config errors |

---

## CD (Continuous Deployment)

Triggers only when CI completes successfully.

| Step | Command | What it does |
|------|---------|--------------|
| Setup | same as CI | mise + Snowflake CLI + uv sync |
| Deploy | `uv run poe snow-deploy-dev` | Uploads `main.py` to `DEV_STAGE` and creates/replaces the `SNOWFLAKE_AGENT_JOB` stored procedure |
| Run | `uv run poe snow-run-dev` | Calls `SNOWFLAKE_AGENT_JOB()` and returns its output |

### Viewing procedure output
1. Go to **Snowsight** → **Data** → **Databases** → your database → **Schemas** → your schema → **Procedures**
2. Find `SNOWFLAKE_AGENT_JOB`
3. Click **Run** or query directly: `CALL SNOWFLAKE_AGENT_JOB();`

---

## Required GitHub Secrets

| Secret | Description |
|--------|-------------|
| `SNOWFLAKE_ACCOUNT` | Account identifier e.g. `xy12345.us-east-1` |
| `SNOWFLAKE_USER` | Snowflake username |
| `SNOWFLAKE_PASSWORD` | Snowflake password or service account password |
| `SNOWFLAKE_WAREHOUSE` | Warehouse to use e.g. `COMPUTE_WH` |
| `SNOWFLAKE_DATABASE` | Target database |
| `SNOWFLAKE_SCHEMA` | Target schema |
| `SNOWFLAKE_ROLE` | Role with privileges to create stages and procedures |
