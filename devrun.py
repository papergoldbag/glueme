import uvicorn


if __name__ == '__main__':
    uvicorn.run('src.utils.asgi:app', reload=True, workers=1, port=8081, host='127.0.0.1')
