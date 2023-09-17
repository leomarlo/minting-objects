import os

from utils.logging import log


def export_credential_path():
    if not os.getenv("GOOGLE_CREDENTIAL_FILE"):
        raise Exception("GOOGLE_CREDENTIAL_FILE not found in environment variables")
    os.environ['GOOGLE_CREDENTIAL_PATH'] = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','env', os.getenv("GOOGLE_CREDENTIAL_FILE")))

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


def create_directory_if_not_there(folder):
    log(f'Check for {folder} directory')
    not_there = not os.path.exists(folder)
    log(f'not_there: {not_there}')
    if not_there:
        log(f'Creating {folder} directory')
        os.makedirs(folder)