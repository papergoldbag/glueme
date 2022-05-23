import uvicorn


if __name__ == '__main__':
    uvicorn.run('src.glueme.asgi:app', reload=True, workers=1, port=8080, host='127.0.0.1')
