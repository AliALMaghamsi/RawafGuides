from models.pilgrim import Pilgrim
from models.room import Room
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session, joinedload
import io
import pandas as pd

async def download_pilgrims(db: Session):
    pilgrims = (
        db.query(Pilgrim)
        .options(
            joinedload(Pilgrim.guide),
            joinedload(Pilgrim.hotel1),
            joinedload(Pilgrim.hotel2),
            joinedload(Pilgrim.hotel3),
            joinedload(Pilgrim.room1),
            joinedload(Pilgrim.room2),
            joinedload(Pilgrim.room3),
        )
        .order_by(
                Pilgrim.room_h1_id.is_(None), Pilgrim.room_h1_id,
                Pilgrim.room_h2_id.is_(None), Pilgrim.room_h2_id,
                Pilgrim.room_h3_id.is_(None), Pilgrim.room_h3_id,
                Pilgrim.id
                )
        .all()
    )

    data = []
    for p in pilgrims:
        data.append({
            "name": p.name,
            "group_number": p.group_number,
            "passport_number": p.passport_number,
            "hotel1_name": p.hotel1.name if p.hotel1 else None,
            "h2_hotel": p.hotel2.name if p.hotel2 else None,
            "h3_hotel": p.hotel3.name if p.hotel3 else None,
            "h1_room_number": p.room1.room_number if p.room1 else None,
            "h2_room_number": p.room2.room_number if p.room2 else None,
            "h3_room_number": p.room3.room_number if p.room3 else None,
            "guide_name": p.guide.name if p.guide else None,
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
