"""
Verification tests for static routes and frontend dashboard serving.
"""

import pytest
from fastapi.testclient import TestClient
from backend.api.main import app

client = TestClient(app)

@pytest.mark.dashboard
def test_serve_dashboard_index():
    r = client.get("/")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]
    html = r.text
    assert "<title>Deep Space Mission OS - Engineering Dashboard</title>" in html
    assert "id=\"plot-3d\"" in html
    assert "id=\"plot-porkchop\"" in html

@pytest.mark.dashboard
def test_serve_static_css():
    r = client.get("/static/style.css")
    assert r.status_code == 200
    assert "text/css" in r.headers["content-type"]
    css = r.text
    assert "--bg-primary" in css
    assert ".app-container" in css

@pytest.mark.dashboard
def test_serve_static_js():
    r = client.get("/static/app.js")
    assert r.status_code == 200
    # On Windows/FastAPI, content type can be application/javascript or text/javascript
    assert "javascript" in r.headers["content-type"]
    js = r.text
    assert "function runSimulation" in js
    assert "function plot3DOrbit" in js
