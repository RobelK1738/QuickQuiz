def _valid_quiz_payload():
    return {
        "title": "Sample Quiz",
        "description": "A test quiz.",
        "questions": [
            {"text": "2+2", "correct_answer": "4"},
            {"text": "Sky color", "correct_answer": "blue"},
        ],
    }

def test_create_quiz_success(client):
    resp = client.post("/api/quizzes", json=_valid_quiz_payload())
    assert resp.status_code == 201
    data = resp.json()
    assert data["id"] > 0
    assert data["title"] == "Sample Quiz"

def test_create_quiz_requires_title(client):
    payload = _valid_quiz_payload()
    payload["title"] = "   "
    resp = client.post("/api/quizzes", json=payload)
    assert resp.status_code == 400
    assert "Title is required" in resp.text

def test_create_quiz_requires_at_least_one_question(client):
    payload = {
        "title": "No Questions",
        "description": "oops",
        "questions": [],
    }
    resp = client.post("/api/quizzes", json=payload)
    # Either 422 from Pydantic (min_items) or 400 from manual check is acceptable
    assert resp.status_code in (400, 422)

def test_create_quiz_rejects_empty_question_or_answer(client):
    payload = _valid_quiz_payload()
    payload["questions"][0]["text"] = "   "
    resp = client.post("/api/quizzes", json=payload)
    assert resp.status_code == 400
    assert "Each question and answer must be non-empty" in resp.text
