import uvicorn


if __name__ == '__main__':
    uvicorn.run('src.glueme.asgi:app', reload=False, workers=4, port=8080, host='127.0.0.1')
