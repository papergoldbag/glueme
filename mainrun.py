import uvicorn


if __name__ == '__main__':
    uvicorn.run('glueme.app.asgi:app', reload=False, workers=4, port=8080, host='127.0.0.1')
