from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

import os
import sys
import subprocess
import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# Check if we're running in Docker
is_docker = os.path.exists('/.dockerenv')

if not is_docker:
    # Try to connect to the database
    db_url = os.getenv("DATABASE_URL", "postgresql://tiss_user:tiss_password@localhost:5432/tiss")
    engine = create_engine(db_url)
    
    try:
        # Try to connect to the database
        connection = engine.connect()
        connection.close()
        print("Successfully connected to the database!")
    except OperationalError:
        print("Could not connect to the database. Starting database container...")
        
        # Check if Docker is installed
        try:
            subprocess.run(["docker", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except (subprocess.SubprocessError, FileNotFoundError):
            print("Docker is not installed or not in PATH. Please install Docker and try again.")
            sys.exit(1)
        
        # Start the database container
        try:
            subprocess.run(["./start_db.sh"], check=True)
            print("Database container started. Waiting for it to be ready...")
            time.sleep(5)  # Give the database time to start
        except subprocess.SubprocessError:
            print("Failed to start the database container. Please run './start_db.sh' manually.")
            sys.exit(1)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)