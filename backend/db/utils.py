

def create_tables(Base: object, engine: object):
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        return {"error": "Base: " + str(Base) + ". Error: " + str(e)}, 500
    return {"message": "Tables created!"}