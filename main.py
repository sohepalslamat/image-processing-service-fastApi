from datetime import datetime
import os
import uuid
from dotenv import load_dotenv
from firebase_admin import credentials, storage, initialize_app
from sqlalchemy import text
from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal, Image, Transformation
from image_processing.utils import process_image
import asyncio

# Load environment variables from .env file
load_dotenv()

firebase_credentials_path = os.getenv("FIREBASE_CREDENTIALS")
storage_bucket = os.getenv("FIREBASE_STORAGE_BUCKET")
cred = credentials.Certificate(firebase_credentials_path)
initialize_app(cred, {
    'storageBucket': storage_bucket
})

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Image Processing Service"}

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...), width: int = None, height: int = None, grayscale: bool = False, rotation: int = None, db: Session = Depends(get_db)):
    # Generate a unique image ID
    image_id = str(uuid.uuid4())

    # Process the image based on provided transformations
    transformations = []
    
    if width and height:
        transformations.append({"type": "resize", "params": {"width": width, "height": height}})
    if grayscale:
        transformations.append({"type": "grayscale", "params": {}})
    if rotation:
        transformations.append({"type": "rotate", "params": {"degrees": rotation}})
    
    processed_image = await process_image(file, transformations)

    # Save the processed image to Firebase Storage and get public URL
    bucket = storage.bucket()
    blob = bucket.blob(f"images/{image_id}{os.path.splitext(file.filename)[1]}")
    processed_image.seek(0)
    blob.upload_from_file(processed_image, content_type='image/png')
    blob.make_public()
    public_url = blob.public_url

    # Save image details to the database
    new_image = Image(filename=file.filename, public_url=public_url)
    db.add(new_image)
    db.commit()
    db.refresh(new_image)  # Get the image ID after insertion

    # Save transformations to the database
    for transformation in transformations:
        new_transformation = Transformation(image_id=new_image.id, transformation_type=transformation['type'], parameters=str(transformation['params']))
        db.add(new_transformation)

    db.commit()

    return JSONResponse(content={"image_id": new_image.id, "public_url": public_url, "message": "Upload and transformation successful!"})

@app.get("/get-image/{image_id}")
async def get_image(image_id: int, db: Session = Depends(get_db)):
    # Query the database for the image using the provided image_id
    image = db.query(Image).filter(Image.id == image_id).first()

    if not image:
        return JSONResponse(content={"message": "Image not found"}, status_code=404)

    # Fetch transformations related to the image
    transformations = db.query(Transformation).filter(Transformation.image_id == image.id).all()

    # Prepare transformation data
    transformation_data = [{"type": t.transformation_type, "parameters": t.parameters, "timestamp": t.timestamp.isoformat()} for t in transformations]

    return JSONResponse(content={
        "image_id": image.id,
        "public_url": image.public_url,
        "filename": image.filename,
        "upload_time": image.upload_time.isoformat(),  # Convert to ISO format
        "transformations": transformation_data
    })
    
    
@app.get("/most-frequent-transformation")
async def most_frequent_transformation(db: Session = Depends(get_db)):
    result = db.execute(
        text("SELECT transformation_type, COUNT(*) AS count "
        "FROM transformations "
        "GROUP BY transformation_type "
        "ORDER BY count DESC "
        "LIMIT 1")
    ).fetchone()

    if result:
        return JSONResponse(content={"transformation_type": result.transformation_type, "count": result.count})
    return JSONResponse(content={"message": "No transformations found"}, status_code=404)

@app.get("/latest-transformations")
async def latest_transformations(db: Session = Depends(get_db)):
    result = db.execute(
        text(
            "SELECT i.id AS image_id, i.filename, t.transformation_type, t.timestamp "
            "FROM images i "
            "LEFT JOIN transformations t ON i.id = t.image_id "
            "WHERE t.timestamp = ("
            "    SELECT MAX(timestamp) "
            "    FROM transformations "
            "    WHERE image_id = i.id"
            ");"
        )
    ).fetchall()

    transformations = [
        {
            "image_id": row.image_id,
            "filename": row.filename,
            "transformation_type": row.transformation_type,
            "timestamp": row.timestamp.isoformat() if isinstance(row.timestamp, datetime) else row.timestamp
        }
        for row in result
    ]

    return JSONResponse(content={"latest_transformations": transformations})

@app.get("/ranking-images")
async def ranking_images(db: Session = Depends(get_db)):
    result = db.execute(
        text("SELECT image_id, filename, COUNT(t.id) AS transformation_count, "
        "DENSE_RANK() OVER (ORDER BY COUNT(t.id) DESC) AS rank "
        "FROM images i "
        "LEFT JOIN transformations t ON i.id = t.image_id "
        "GROUP BY image_id, filename "
        "ORDER BY rank;")
    ).fetchall()

    rankings = [{"image_id": row.image_id, "filename": row.filename, "transformation_count": row.transformation_count, "rank": row.rank} for row in result]

    return JSONResponse(content={"rankings": rankings})