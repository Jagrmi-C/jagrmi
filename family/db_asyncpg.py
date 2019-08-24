import asyncio
import asyncpg
import datetime

async def main():
    conn = await asyncpg.connect("postgresql://andrei@localhost/family")
    row = await conn.fetchrow(
        "SELECT * FROM test"
    )
    print(row)
    await conn.close()

asyncio.get_event_loop().run_until_complete(main())
