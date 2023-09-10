import os
from flask import Flask, jsonify
from flask_cors import CORS
from utils.path import export_credential_path, load_env, create_tables_if_with_db
from db.session import engine, SessionLocal
from db.mock import mockdb
from db.models import (
    Base, 
    User
)

# save global enviornment variable to the os
load_env()
export_credential_path()
print("GOOGLE_CREDENTIAL_PATH: " + os.getenv('GOOGLE_CREDENTIAL_PATH'))

app = Flask(__name__)
# CORS(app, origins=["http://localhost:3000", "http://another.domain"])  # This will allow all origins to access your app. It's okay for development but not for production!

create_tables_if_with_db()


@app.route('/add-leonardo', methods=['POST'])
def add_leonardo():
    session = SessionLocal()  # create a new database session

    try:
        leonardo = User(username="Leonardo daVinci", password="securepassword")  # You should hash this!
        session.add(leonardo)
        session.commit()

        return {"message": "Leonardo daVinci added!"}

    except Exception as e:
        session.rollback()
        return {"error": str(e)}

    finally:
        session.close()




@app.route('/add-user', methods=['GET'])
def add_user():
    session = SessionLocal()  # create a new database session
    success = False,
    failMessage = ""
    try:
        paul = User(username="Paul", password="apassword")  # You should hash this!
        session.add(paul)
        session.commit()
        success = True

    except Exception as e:
        session.rollback()
        success = False
        failMessage = str(e)

    finally:
        session.close()

    if success:
        return {"message": "Paul added!"}, 200
    else:
        return {"error": "Paul not added! " + failMessage}, 400


@app.route('/get-user/<string:username>', methods=['GET'])
def get_user(username):
    session = SessionLocal()

    try:
        user = session.query(User).filter(User.username == username).first()
        
        if user:
            return {
                "id": user.id,
                "username": user.username
            }
        else:
            return {"message": "User not found."}, 404

    except Exception as e:
        return {"error": str(e)}, 500

    finally:
        session.close()


@app.route('/check-os', methods=['GET'])
def checkos():
    # print environment variables os.getenv('POSTGRES_USER') and passw=os.getenv('POSTGRES_PASSWORD')
    print(os.getenv('POSTGRES_USER'))
    print(os.getenv('POSTGRES_PASSWORD'))
    return {"postgres-user": os.getenv('POSTGRES_USER'), "postgres-password": os.getenv('POSTGRES_PASSWORD')}


@app.route('/get-article', methods=['GET'])
def get_article():
    article_content = mockdb.get_article()
    return jsonify(articleContent=article_content)

@app.route('/button-endpoint', methods=['POST'])
def button_endpoint():
    return jsonify(message="Button was pressed!")

@app.route('/test', methods=['GET'])
def test():
    return {"message": "Hello from the button endpoint!"}


@app.route('/createTables', methods=['GET'])
def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        return {"error": "Base: " + str(Base) + ". Error: " + str(e)}, 500
    return {"message": "Tables created!"}

@app.route('/createTablesBrutal', methods=['GET'])
def create_tables_brutal():
    Base.metadata.create_all(bind=engine)
    return {"message": "Tables created!"}


if __name__ == '__main__':
    print("Starting Flask app...")
    CORS(app)
    app.run(debug=True, port=5000)