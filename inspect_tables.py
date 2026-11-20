import asyncio
import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

async def main():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("DATABASE_URL not set")
        return
    # asyncpg expects postgresql:// without channel_binding query param if it causes issues
    clean_url = db_url.replace("&channel_binding=require", "").replace("?channel_binding=require", "")
    conn = await asyncpg.connect(clean_url)
    try:
        tables = await conn.fetch("""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
            ORDER BY table_schema, table_name;
        """)
        print(f"Total tables found: {len(tables)}")
        for t in tables:
            schema = t['table_schema']
            name = t['table_name']
            count = await conn.fetchval(f'SELECT COUNT(*) FROM "{schema}"."{name}"')
            print(f"- {schema}.{name}: {count} rows")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(main())
