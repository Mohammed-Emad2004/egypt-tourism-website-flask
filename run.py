import os
from dotenv import load_dotenv

load_dotenv()

from app import app

if __name__ == '__main__':
    port = int(os.getenv("FLASK_RUN_PORT", 5000))
    
    app.run(host='0.0.0.0', port=port, debug=True)