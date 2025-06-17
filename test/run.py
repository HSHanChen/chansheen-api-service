"""
@Author: Chan Sheen
@Date: 2025/6/17 14:40
@File: run.py
@Description: 
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

