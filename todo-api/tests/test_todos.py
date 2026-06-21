def test_create_todo(client):
    response = client.post(
        "/todos/",
        json={
            "title": "Learn FastAPI",
            "description": "Build CRUD API"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Learn FastAPI"


def test_get_all_todos(client):
    response = client.get("/todos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_single_todo(client):
    create = client.post(
        "/todos/",
        json={"title": "Test", "description": "single"}
    )

    todo_id = create.json()["id"]

    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200


def test_update_todo(client):
    create = client.post(
        "/todos/",
        json={"title": "Old", "description": "Old"}
    )

    todo_id = create.json()["id"]

    response = client.put(
        f"/todos/{todo_id}",
        json={
            "title": "New",
            "description": "Updated",
            "is_completed": True
        }
    )

    assert response.status_code == 200
    assert response.json()["is_completed"] is True


def test_delete_todo(client):
    create = client.post(
        "/todos/",
        json={"title": "Delete", "description": "me"}
    )

    todo_id = create.json()["id"]

    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200