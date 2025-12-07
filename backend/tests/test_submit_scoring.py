def _create_simple_quiz(client):
    payload = {
        "title": "Math & Color",
        "description": "tiny test quiz",
        "questions": [
            {"text": "2+2", "correct_answer": "4"},
            {"text": "Sky color", "correct_answer": "Blue"},
            {"text": "Copy 'Hi'", "correct_answer": "Hi"},
        ],
    }
    resp = client.post("/api/quizzes", json=payload)
    assert resp.status_code == 201
    return resp.json()["id"]

def test_get_quiz_details(client):
    quiz_id = _create_simple_quiz(client)

    resp = client.get(f"/api/quizzes/{quiz_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == quiz_id
    assert len(data["questions"]) == 3

def test_submit_quiz_scoring_case_insensitive_and_trim(client):
    quiz_id = _create_simple_quiz(client)

    submission = {
        "answers": [
            " 4 ",       # correct with spaces
            "blue",      # correct, different case
            "hi",        # correct, lower
        ]
    }
    resp = client.post(f"/api/quizzes/{quiz_id}/submit", json=submission)
    assert resp.status_code == 200
    data = resp.json()

    assert data["score"] == 3
    assert data["total"] == 3
    assert all(r["is_correct"] for r in data["results"])

def test_submit_quiz_handles_incorrect_and_missing(client):
    quiz_id = _create_simple_quiz(client)

    submission = {
        "answers": [
            "5",  # wrong
            "",   # blank
            # missing third -> should be treated as ""
        ]
    }
    resp = client.post(f"/api/quizzes/{quiz_id}/submit", json=submission)
    assert resp.status_code == 200
    data = resp.json()

    assert data["score"] == 0
    assert data["total"] == 3
    assert len(data["results"]) == 3
    assert all(not r["is_correct"] for r in data["results"])
