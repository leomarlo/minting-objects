import os

def export_credential_path():
    os.environ['GOOGLE_CREDENTIAL_PATH'] = os.path.join(os.path.dirname(__file__), 'env', os.getenv("GOOGLE_CREDENTIAL_FILE"))

def current_environment():
    environment = os.getenv('FLASK_ENV')
    return environment if environment else 'local_without_db'

def load_env():
    if current_environment() == 'local' or current_environment() == 'local_without_db':
        from dotenv import load_dotenv
        load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..','..', '.env'), verbose=True)

def create_tables_if_with_db():
    if current_environment() != 'local_without_db':
        from db.models import Base
        from db.session import engine
        Base.metadata.create_all(bind=engine)


def create_upload_directory_if_not_there(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)