import os
import unittest
from unittest.mock import patch

os.environ["TESTING"] = "true"

from src.app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>MLH Fellow</title>" in html
        assert '<a class="nav-link" href="#about">About</a>' in html
        assert '<span class="pull"> Pull </span>' in html

    @patch("requests.post")
    @patch("requests.get")
    def test_timeline(self, mock_get, mock_post):
        response = self.client.get("/api/timeline_post", follow_redirects=True)
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        # TODO add more tests relating to the /api/timeline_post GET and POST apis
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "john@example.com",
                "content": "Hello world, I'm john!",
            },
        )
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert json["content"] == "Hello world, I'm john!"
        assert json["email"] == "john@example.com"
        assert json["id"] == 1
        assert json["name"] == "John Doe"
        response = self.client.get("/api/timeline_post")
        json = response.get_json()
        assert response.status_code == 200
        assert response.is_json
        assert json["timeline_posts"][0]["content"] == "Hello world, I'm john!"
        assert json["timeline_posts"][0]["email"] == "john@example.com"
        assert json["timeline_posts"][0]["id"] == 1
        assert json["timeline_posts"][0]["name"] == "John Doe"

        # TODO Add more tests relating to the timeline page
        # Set up mocked responses for GET
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = {
            "timeline_posts": [
                {"name": "John", "email": "john@example.com", "content": "Post 1"}
            ]
        }
        response = self.client.get("/timeline")
        # Check that expected data is displayed on page
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert '<div class="col-md-12">' in html
        assert "<h2>Timeline Posts</h2>" in html
        self.assertIn(b"Post 1", response.data)

        # Set up mocked responses for POST when it succeeds
        mock_post.return_value.ok = True
        data = {"name": "Jane", "email": "jane@example.com", "content": "Post 2"}
        response = self.client.post("/timeline", data=data)
        # Check that expected data is displayed on page after the POST
        assert response.status_code == 200
        self.assertIn("Your post has been created", response.get_data(as_text=True))

        # Set up mocked responses for POST when it fails
        mock_post.return_value.ok = False
        data = {"name": "Jane", "email": "not-an-email", "content": "Post 2"}
        response = self.client.post("/timeline", data=data)
        # Check that expected data is displayed on page after the POST
        assert response.status_code == 200
        self.assertIn(
            "There was an error submitting your post", response.get_data(as_text=True)
        )

    def test_malformed_timeline_post(self):
        response = self.client.post(
            "/api/timeline_post",
            data={"email": "john@example.com", "content": "Hello world, I'm john!"},
        )
        assert response.status_code == 400

        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        response = self.client.post(
            "/api/timeline_post",
            data={"name": "John Doe", "email": "john@example.com", "content": ""},
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "not-an-email",
                "content": "Hello world, I'm john!",
            },
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
