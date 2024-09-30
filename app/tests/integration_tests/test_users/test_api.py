import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("email,password,status_code", [
    ("kot@pes.com", "kotopes", 201),
    ("kot@pes.com", "kot0pes", 409),
    ("pes@kot.com", "pesokot", 201),
    ("abcde", "pesokot", 422),
])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/api/auth/register", json={
        "email": email,
        "password": password,
    })

    assert response.status_code == status_code


@pytest.mark.parametrize("email,password,status_code", [
    ("test@test.com", "test", 200),
    ("danil@example.com", "danil", 200),
    ("wrong@person.com", "danil", 401),
])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/api/auth/login", json={
        "email": email,
        "password": password,
    })

    assert response.status_code == status_code
