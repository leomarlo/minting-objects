from db.models import Image

def create_tables(Base: object, engine: object):
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        return {"error": "Base: " + str(Base) + ". Error: " + str(e)}, 500
    return {"message": "Tables created!"}

def db_create_image_entry(session: object, filename, cid, gs):

    # Create a new Image entry
    new_image = Image(filename=filename, cid=cid, gs=gs)
    session.add(new_image)

    # Commit the transaction to save the entry to the database
    session.commit()

def db_fetch_image_from_filename(session: object, filename: str):
      
  # Fetch the image entry with the given filename
  image_entry = session.query(Image).filter_by(filename=filename).first()

  # Print the details (you can access other fields similarly)
  if image_entry:
      print(f"Filename: {image_entry.filename}, CID: {image_entry.cid}, GS: {image_entry.gs}, Timestamp: {image_entry.timestamp}")
      return {"filename": image_entry.filename, "cid": image_entry.cid, "gs": image_entry.gs, "timestamp": image_entry.timestamp}
  else:
      print("Image not found!")
      return {"error": "Image not found!"}

    

def db_close_session(session: object):
    # Close the session
    session.close()
