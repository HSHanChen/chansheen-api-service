import uvicorn

if __name__ == "__main__":
    config = uvicorn.Config(
        "app.main:app",
        host="0.0.0.0",
        port=18323,
        reload=True,
        log_level="info",
        access_log=True,
    )
    server = uvicorn.Server(config)
    server.run()
