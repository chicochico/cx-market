# Market

This a coding exercise: An api endpoint to validate orders submissions.

## Running
### With docker
1. clone this repo
2. `cd` into it
3. build the docker image `docker build -t market .` (note the period at the end)
4. run `docker run --rm -p 8000:8000 market`

to run tests you can run `docker run --rm --entrypoint pytest market`


### In a virtualenv
1. clone this repo
2. create a virtualenv and activate it
3. install requirements `pip install -r requirements.txt`
4. run `uvicorn market.market:app`

to run tests run `pytest` in the project directory

### API Documentation
The API docs can be found at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) after executing the app.
API schema is also available at [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json).

## Endpoints
```
POST /orders/order
GET  /orders
```

## Notes
- Framework: [FastAPI](https://fastapi.tiangolo.com/)
