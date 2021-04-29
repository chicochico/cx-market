import uvicorn
from fastapi import FastAPI

import market.orders as orders

app = FastAPI(title="Market", description="An API for trading.")
app.include_router(orders.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
