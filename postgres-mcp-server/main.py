from typing import List, Dict
import psycopg2
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("postgres-server")

DB_CONFIG = {
    "dbname": "practice_db",
    "user": "postgres",
    "password": "password123",
    "host": "localhost",
    "port": "5432",
}

def run_query(sql: str) -> List[Dict]:
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            colnames = [desc[0] for desc in cur.description]
            rows = [dict(zip(colnames, row)) for row in cur.fetchall()]
    return rows

@mcp.tool()
async def execute_sql(sql: str) -> List[Dict]:
    """Execute a SQL query against the practice Postgres database."""
    return run_query(sql)

@mcp.tool()
async def get_schema(table: str) -> List[Dict]:
    """Return column names and types for a given table."""
    sql = """
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = %s
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (table,))
            rows = [{"column": r[0], "type": r[1]} for r in cur.fetchall()]
    return rows

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
