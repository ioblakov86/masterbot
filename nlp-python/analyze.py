import spacy
import asyncpg
import os

DB_DSN = "postgres://marketbot:marketbot@db:5432/marketbot"
nlp = spacy.load("ru_core_news_sm")

async def analyze_messages():
    conn = await asyncpg.connect(dsn=DB_DSN)
    rows = await conn.fetch("SELECT id, text FROM raw_messages WHERE id NOT IN (SELECT raw_id FROM listings)")
    for row in rows:
        doc = nlp(row['text'])
        # простой пример: ищем цену
        price = None
        for token in doc:
            if token.like_num:
                price = int(token.text)
                break
        # классификация типа объявления (простейшая)
        type_ = "sale" if "продам" in row['text'].lower() else "buy"
        category = "general"
        await conn.execute(
            "INSERT INTO listings(type, category, title, description, price, contact, source_chat) VALUES($1,$2,$3,$4,$5,$6,$7)",
            type_, category, row['text'][:50], row['text'], price, None, 0
        )
    await conn.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(analyze_messages())
