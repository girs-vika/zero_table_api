import asyncpg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
from typing import List
import databases

app = FastAPI()

DATABASE_URL = "postgresql://postgres:ar4isuperstar@localhost/test"
database = databases.Database(DATABASE_URL)


class ZeroTable2(BaseModel):
    id: int
    name: str
    value: dict
    date_update: datetime

# Запускаем соединение
@app.on_event("startup")
async def database_connect():
    await database.connect()

# Останавливаем соединение
@app.on_event("shutdown")
async def database_disconnect():
    await database.disconnect()


# Получение всех записей из таблицы
@app.get("/zerotable2", response_model=List[ZeroTable2])
async def read_zerotable2():
    query = "SELECT * FROM zero_table2"
    rows = await database.fetch_all(query=query)
    return [ZeroTable2(**row) for row in rows]

# Получение записи из таблицы по ее идентификатору
@app.get("/zerotable2/{id}", response_model=ZeroTable2)
async def read_zerotable2_by_id(id: int):
    query = "SELECT * FROM zero_table2 WHERE id = :id"
    values = {"id": id}
    row = await database.fetch_one(query=query, values=values)
    if row:
        return ZeroTable2(**row)
    else:
        raise HTTPException(status_code=404, detail="Запись не найдена")

# Обновление записи в таблице
@app.patch("/zerotable2/{id}", response_model=ZeroTable2)
async def update_zerotable2(id: int, name: str, value: dict):
    query = "UPDATE zero_table2 SET name=:name, value=:value, date_update=:date_update WHERE id=:id"
    values = {"id": id, "name": name, "value": value, "date_update": datetime.now(timezone.utc)}
    await database.execute(query=query, values=values)
    return ZeroTable2(**values)

# Удаление записи из таблицы по ее идентификатору
@app.delete("/zerotable2/{id}")
async def delete_zerotable2(id: int):
    query = "DELETE FROM zero_table2 WHERE id = :id"
    values = {"id": id}
    await database.execute(query=query, values=values)
    return {"message": "Запись {id} успешно удалена"}


