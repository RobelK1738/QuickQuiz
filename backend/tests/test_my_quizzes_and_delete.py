def _create_quiz(client, title="Owned Quiz"):
    payload = {
        "title": title,
        "description": "Owned by test-user",
        "questions": [
            {"text": "Q1", "correct_answer": "A1"},
        ],
    }
    resp = client.post("/api/quizzes", json=payload)
    assert resp.status_code == 201
    return resp.json()["id"]


def test_my_quizzes_lists_only_created_quizzes(client):
    _create_quiz(client, "Quiz One")
    _create_quiz(client, "Quiz Two")

    resp = client.get("/api/quizzes/my")
    assert resp.status_code == 200
    data = resp.json()

    titles = [q["title"] for q in data]
    assert "Quiz One" in titles
    assert "Quiz Two" in titles
    # At least these two are present
    assert len(data) >= 2


def test_delete_quiz_by_owner(client):
    quiz_id = _create_quiz(client, "Delete Me")

    delete_resp = client.delete(f"/api/quizzes/{quiz_id}")
    assert delete_resp.status_code == 204

    # Confirm it's not in public list
    list_resp = client.get("/api/quizzes")
    assert list_resp.status_code == 200
    assert all(q["id"] != quiz_id for q in list_resp.json())
