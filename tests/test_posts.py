from typing import List
from app import schemas
import pytest


def test_get_all_posts(test_posts, client):
    res = client.get("/posts/")
    assert res.status_code == 200


def test_create_post(authorized_client):
    res = authorized_client.post(
        "/posts/",
        json={"title": "How about a title", "content": "How about a content!"},
    )
    assert res.status_code == 201


def test_unauthorized_create_post(client):
    res = client.post(
        "/posts/",
        json={"title": "How about a title", "content": "How about a content!"},
    )
    assert res.status_code == 401


def test_get_one_post(test_posts, client):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 200


def test_not_found_get_one_post(test_posts, client):
    res = client.get(f"/posts/888888")
    assert res.status_code == 404


def test_update_post(test_posts, authorized_client):
    update_post = test_posts[0]
    res = authorized_client.put(
        f"/posts/{update_post.id}",
        json={"title": "New Title", "content": "New Content"},
    )
    assert res.json()["id"] == update_post.id
    assert res.status_code == 200


def test_update_other_post(test_posts, authorized_client):
    update_post = test_posts[3]
    res = authorized_client.put(
        f"/posts/{update_post.id}",
        json={"title": "New Title", "content": "New Content"},
    )
    assert res.status_code == 403


def test_unauthenticated_upate_post(test_posts, client):
    update_post = test_posts[0]
    res = client.put(
        f"/posts/{update_post.id}",
        json={"title": "New Title", "content": "New Content"},
    )
    assert res.json()["detail"] == "Not authenticated"
    assert res.status_code == 401


def test_not_found_update_post(test_posts, authorized_client):
    res = authorized_client.put(
        f"/posts/888888", json={"title": "New Title", "content": "New Content"}
    )
    assert res.status_code == 404


def test_delete_post(test_posts, authorized_client):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_not_found_delete_post(test_posts, authorized_client):
    res = authorized_client.delete(f"/posts/888888")
    assert res.status_code == 404


def test_unauthorized_delete_post(test_posts, client):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_other_user_post(test_posts, authorized_client):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403
