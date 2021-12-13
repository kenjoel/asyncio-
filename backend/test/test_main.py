from starlette.testclient import TestClient
from main import app

client = TestClient(app)

items = {}

'''
async def override_dependency(q: Optional[str] = None):
    return {"q": q, "skip": 5, "limit": 10}
app.dependency_overrides[common_parameters] = override_dependency

This Workflow this is bugging me
'''


def test_read():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_hello():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"I said": "Hello"}
