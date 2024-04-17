import json

from fastapi import FastAPI, HTTPException

from models import Composer, Piece


app = FastAPI()

with open("composers.json", "r") as f:
    composers_list: list[dict] = json.load(f)

with open("pieces.json", "r") as f:
    piece_list: list[dict] = json.load(f)

composers: list[Composer] = []
for composer in composers_list:
    composers.append(Composer(**composer))

pieces: list[Piece] = []
for piece in piece_list:
    pieces.append(Piece(**piece))


@app.get("/composers")
async def get_composers() -> list[Composer]:
    return composers

@app.get("/pieces")
async def get_pieces(composer_id: int = None) -> list[Piece]:
    if composer_id is None:
        return pieces
    else:
        filtered_pieces = []
        for piece in pieces:
            if piece.composer_id == composer_id:
                filtered_pieces.append(piece)
        return filtered_pieces

@app.post("/composers")
async def add_composer(composer: Composer) -> None:
    for existing_composer in composers:
        if existing_composer.composer_id == composer.composer_id:
            raise HTTPException(status_code=400, detail="Duplicate ID")
    composers.append(composer)
    
@app.post("/pieces")
async def add_piece(piece: Piece) -> None:
    composer_ids = []
    for existing_id in pieces:
        composer_ids.append(existing_id.composer_id)
    if piece.composer_id not in composer_ids:
        raise HTTPException(status_code=400, detail="Composer ID Not Found")
    pieces.append(piece)

@app.put("/composers/{composer_id}")
async def update_composer(composer_id: int, updated_composer: Composer) -> None:
    for i, composer in enumerate(composers):
        if composer.composer_id == composer_id:
            composers[i] = updated_composer
            raise HTTPException(status_code=400, detail="Duplicate ID")
    return

@app.put("/pieces/{piece_name}")
async def update_piece(piece_name: str, updated_piece: Piece) -> None:
    composer_ids = []
    for existing_id in pieces:
        composer_ids.append(existing_id.composer_id)
    if updated_piece.composer_id not in composer_ids:
        raise HTTPException(status_code=400, detail="Composer ID Not Found")
    
    for i, piece in enumerate(pieces):
        if piece.name == piece_name:
            pieces[i] = updated_piece
            return

@app.delete("/composer/{composer_id}")
async def remove_composer(composer_id: int) -> None:
    for i, composer in enumerate(composers):
        if composer.composer_id == composer_id:
            composers.pop(i)
            return

@app.delete("/pieces/{piece_name}")
async def remove_piece(piece_name: str) -> None:
    for i, piece in enumerate(pieces):
        if piece.name == piece_name:
            pieces.pop(i)
            return