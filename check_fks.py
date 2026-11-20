import asyncio
import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

async def main():
    db_url = os.getenv("DATABASE_URL")
    clean_url = db_url.replace("&channel_binding=require", "").replace("?channel_binding=require", "")
    conn = await asyncpg.connect(clean_url)
    try:
        # Check views
        views = await conn.fetch("""
            SELECT table_schema, table_name
            FROM information_schema.views
            WHERE table_schema NOT IN ('information_schema', 'pg_catalog');
        """)
        print("Views:", [f"{v['table_schema']}.{v['table_name']}" for v in views])

        # Check foreign keys pointing to app.session_invites
        fks = await conn.fetch("""
            SELECT
                tc.table_schema, tc.table_name, kcu.column_name,
                ccu.table_schema AS foreign_table_schema,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name 
            FROM information_schema.table_constraints AS tc 
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
              AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage AS ccu
              ON ccu.constraint_name = tc.constraint_name
              AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY'
              AND (ccu.table_name = 'session_invites' OR tc.table_name = 'session_invites');
        """)
        print("Foreign keys on session_invites:", [dict(r) for r in fks])
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(main())
