from models.pilgrim import Pilgrim
from models.room import Room
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
import io
import pandas as pd 

async def download_pilgrims(db:Session):
    pilgrims = (
        db.query(Pilgrim)
        .options(joinedload(Pilgrim.room))
        .order_by(Pilgrim.room_id)
        .all()
    )

    data = []

    for p in pilgrims:
        data.append({
            "name":p.name,
            "passport_number":p.passport_number,
            "room_number":p.room.room_number if p.room else None,
            "room_type":p.room.capacity,
            "room_current_capacity":p.room.current_capacity,
            "guide":p.guide.name if p.guide else None, 
        })
    df = pd.DataFrame(data)
    stream = io.BytesIO()
    with pd.ExcelWriter(stream, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Pilgrims")
    stream.seek(0)

    return StreamingResponse(
        stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=pilgrims.xlsx"}
    )




