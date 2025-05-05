from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/describe")
async def describe():
    return {"data":{"name":"Siyam uddin","age":23, "Country":"Bangladesh"}}
