from fastapi import FastAPI
from starlette.testclient import TestClient

app = FastAPI()

client = TestClient(app)

items = {}

'''
async def override_dependency(q: Optional[str] = None):
    return {"q": q, "skip": 5, "limit": 10}
app.dependency_overrides[common_parameters] = override_dependency

This Workflow this is bugging me
'''


@app.get("/")
async def read():
    return {"Hello": "World"}


def test_read():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

