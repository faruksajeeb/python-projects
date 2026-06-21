def test_create_todo(client, auth_headers):
    response = client.post(
        "/todos/",
        json={
            "title": "Learn FastAPI",
            "description": "Build CRUD API"
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Learn FastAPI"


def test_get_all_todos(client, auth_headers):
    response = client.get(
        "/todos/",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_single_todo(client, auth_headers):
    create = client.post(
        "/todos/",
        json={
            "title": "Test",
            "description": "single"
        },
        headers=auth_headers
    )

    todo_id = create.json()["id"]

    response = client.get(
        f"/todos/{todo_id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["id"] == todo_id


def test_update_todo(client, auth_headers):
    create = client.post(
        "/todos/",
        json={
            "title": "Old",
            "description": "Old"
        },
        headers=auth_headers
    )

    todo_id = create.json()["id"]

    response = client.put(
        f"/todos/{todo_id}",
        json={
            "title": "New",
            "description": "Updated",
            "is_completed": True
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["is_completed"] is True


def test_delete_todo(client, auth_headers):
    create = client.post(
        "/todos/",
        json={
            "title": "Delete",
            "description": "me"
        },
        headers=auth_headers
    )

    todo_id = create.json()["id"]

    response = client.delete(
        f"/todos/{todo_id}",
        headers=auth_headers
    )

    assert response.status_code == 200