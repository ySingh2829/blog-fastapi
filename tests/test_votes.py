import pytest
from app import models


@pytest.fixture
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(user_id=test_user["id"], post_id=test_posts[3].id)
    session.add(new_vote)
    session.commit()


def test_vote_on_post(test_posts, authorized_client):
    upvote = 1
    res = authorized_client.post(
        "/vote/", json={"post_id": test_posts[0].id, "dir": upvote}
    )
    assert res.json()["message"] == "successfully added vote"
    assert res.status_code == 201


def test_vote_twice_post(test_vote, authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 409


def test_vote_delete(test_vote, authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 201


def test_delete_vote_not_exist(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 404


def test_vote_not_exist(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": 888888, "dir": 0})
    assert res.status_code == 404


def test_vote_unathorized_client(client, test_posts):
    res = client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 401
