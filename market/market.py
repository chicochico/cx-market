import uvicorn
from fastapi import FastAPI

import market.orders as orders

app = FastAPI()
app.include_router(orders.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
