import os

import uvicorn

from glueme.app.settings import setup_from_env

if __name__ == '__main__':
    setup_from_env()
    uvicorn.run('glueme.app.createapp:app', workers=1, port=os.getenv('PORT'), host='0.0.0.0')
