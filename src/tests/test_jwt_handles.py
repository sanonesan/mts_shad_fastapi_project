import pytest
from fastapi import status
from sqlalchemy import select, delete

from src.models import books_jwt
from src.models import sellers_jwt

from src.configurations.auth import utils as auth_utils


# Тест создание продавцов
@pytest.mark.asyncio
async def test_signup_seller_jwt(db_session, async_client):
    """
    sign up seller
    """
    await db_session.execute(delete(sellers_jwt.SellerJWT))

    data = {
        "first_name": "Martin",
        "second_name": "Iden",
        "email": "martiniden@gmail.com",
        "password": "test00",
    }
    response = await async_client.post("/api/v1/jwt/signup", data=data)
    result_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert result_data == {
        "id": 1,
        "first_name": "Martin",
        "second_name": "Iden",
        "email": "martiniden@gmail.com",
    }


@pytest.mark.asyncio
async def test_login_seller_jwt(db_session, async_client):
    """
    Login seller (get token)
    """
    await db_session.execute(delete(sellers_jwt.SellerJWT))

    test_password = "test"
    seller = sellers_jwt.SellerJWT(
        email="martiniden@gmail.com",
        password=auth_utils.hash_password(test_password),
        first_name="Martin",
        second_name="Iden",
    )
    db_session.add(seller)
    await db_session.flush()

    jwt_payload = {
        "email": seller.email,
        "seller_id": seller.id,
    }

    token = auth_utils.encode_jwt(payload=jwt_payload)

    data = {
        "email": seller.email,
        "password": test_password,
    }
    response = await async_client.post(
        "/api/v1/jwt/login",
        data=data,
    )
    result_data = response.json()

    # assert response.status_code == status.HTTP_200_OK
    # print(result_data)
    assert result_data == {
        "access_token": token,
        "token_type": "Bearer",
    }


@pytest.mark.asyncio
async def test_update_seller_jwt(db_session, async_client):
    """
    update seller info
    """
    await db_session.execute(delete(sellers_jwt.SellerJWT))

    test_password = "test"
    seller = sellers_jwt.SellerJWT(
        email="martiniden@gmail.com",
        password=auth_utils.hash_password(test_password),
        first_name="Martin",
        second_name="Iden",
    )
    db_session.add(seller)
    await db_session.flush()

    jwt_payload = {
        "email": seller.email,
        "seller_id": seller.id,
    }

    token = auth_utils.encode_jwt(payload=jwt_payload)

    data = {
        "email": "martinidenza@gmail.com",
        "first_name": "Martin",
        "second_name": "Idenza",
    }
    headers = {"Authorization": "Bearer " + token}
    response = await async_client.put(
        "/api/v1/jwt/sellers/me/info/update",
        data=data,
        headers=headers,
    )
    result_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result_data == {
        "id": seller.id,
        "first_name": "Martin",
        "second_name": "Idenza",
        "email": "martinidenza@gmail.com",
    }


@pytest.mark.asyncio
async def test_get_seller_jwt_list(db_session, async_client):
    """
    get sellers list
    """
    await db_session.execute(delete(sellers_jwt.SellerJWT))

    test_password = "test"
    seller_1 = sellers_jwt.SellerJWT(
        email="martiniden@gmail.com",
        password=auth_utils.hash_password(test_password),
        first_name="Martin",
        second_name="Iden",
    )
    seller_2 = sellers_jwt.SellerJWT(
        email="zenpythonovich@gmail.com",
        password=auth_utils.hash_password(test_password),
        first_name="Zen",
        second_name="Pythonovich",
    )
    db_session.add_all([seller_1, seller_2])
    await db_session.flush()

    response = await async_client.get(
        "/api/v1/jwt/sellers/list",
    )
    result_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result_data == {
        "sellers": [
            {
                "id": seller_1.id,
                "first_name": seller_1.first_name,
                "second_name": seller_1.second_name,
                "email": seller_1.email,
            },
            {
                "id": seller_2.id,
                "first_name": seller_2.first_name,
                "second_name": seller_2.second_name,
                "email": seller_2.email,
            },
        ]
    }


@pytest.mark.asyncio
async def test_add_book_seller_jwt(db_session, async_client):
    """
    add book to seller
    """
    await db_session.execute(delete(sellers_jwt.SellerJWT))

    test_password = "test"
    seller = sellers_jwt.SellerJWT(
        email="martiniden@gmail.com",
        password=auth_utils.hash_password(test_password),
        first_name="Martin",
        second_name="Iden",
    )
    db_session.add(seller)
    await db_session.flush()

    jwt_payload = {
        "email": seller.email,
        "seller_id": seller.id,
    }

    token = auth_utils.encode_jwt(payload=jwt_payload)

    data = {
        "title": "Wrong Code",
        "author": "Robert Martin",
        "count_pages": 104,
        "year": 2007,
    }
    headers = {"Authorization": "Bearer " + token}
    response = await async_client.post(
        "/api/v1/jwt/sellers/me/books/add",
        data=data,
        headers=headers,
    )
    result_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert result_data == {
        "seller_id": seller.id,
        "title": "Wrong Code",
        "author": "Robert Martin",
        "year": 2007,
        "id": 1,
        "count_pages": 104,
    }


@pytest.mark.asyncio
async def test_get_book_by_id_seller_jwt(db_session, async_client):
    """
    Get book by id
    """
    await db_session.execute(delete(sellers_jwt.SellerJWT))

    test_password = "test"
    seller_1 = sellers_jwt.SellerJWT(
        email="martiniden@gmail.com",
        password=auth_utils.hash_password(test_password),
        first_name="Martin",
        second_name="Iden",
    )
    db_session.add(seller_1)
    await db_session.flush()

    book_1 = books_jwt.BookJWT(
        seller_id=seller_1.id,
        title="Wrong Code",
        author="Robert Martin",
        count_pages=104,
        year=2007,
    )

    book_2 = books_jwt.BookJWT(
        seller_id=seller_1.id,
        title="Clean Code",
        author="Robert Martin",
        count_pages=104,
        year=2007,
    )
    db_session.add_all([book_1, book_2])
    await db_session.flush()

    response = await async_client.get(
        f"/api/v1/jwt/books/{book_2.id}",
    )
    result_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result_data == {
        "seller_id": seller_1.id,
        "title": book_2.title,
        "author": book_2.author,
        "year": book_2.year,
        "id": book_2.id,
        "count_pages": book_2.count_pages,
    }


@pytest.mark.asyncio
async def test_get_books_list_seller_jwt(db_session, async_client):
    """
    Get books list
    """
    await db_session.execute(delete(sellers_jwt.SellerJWT))

    test_password = "test"
    seller_1 = sellers_jwt.SellerJWT(
        email="martiniden@gmail.com",
        password=auth_utils.hash_password(test_password),
        first_name="Martin",
        second_name="Iden",
    )
    db_session.add(seller_1)
    await db_session.flush()

    book_1 = books_jwt.BookJWT(
        seller_id=seller_1.id,
        title="Wrong Code",
        author="Robert Martin",
        count_pages=104,
        year=2007,
    )

    book_2 = books_jwt.BookJWT(
        seller_id=seller_1.id,
        title="Clean Code",
        author="Robert Martin",
        count_pages=104,
        year=2007,
    )
    db_session.add_all([book_1, book_2])
    await db_session.flush()

    response = await async_client.get(
        "/api/v1/jwt/books/list",
    )
    result_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result_data == {
        "books": [
            {
                "seller_id": seller_1.id,
                "title": book_1.title,
                "author": book_1.author,
                "year": book_1.year,
                "id": book_1.id,
                "count_pages": book_1.count_pages,
            },
            {
                "seller_id": seller_1.id,
                "title": book_2.title,
                "author": book_2.author,
                "year": book_2.year,
                "id": book_2.id,
                "count_pages": book_2.count_pages,
            },
        ]
    }


@pytest.mark.asyncio
async def test_get_seller_jwt_info(db_session, async_client):
    """
    get seller info (with books)
    """
    await db_session.execute(delete(sellers_jwt.SellerJWT))

    test_password = "test"
    seller_1 = sellers_jwt.SellerJWT(
        email="martiniden@gmail.com",
        password=auth_utils.hash_password(test_password),
        first_name="Martin",
        second_name="Iden",
    )
    db_session.add(seller_1)
    await db_session.flush()

    jwt_payload = {
        "email": seller_1.email,
        "seller_id": seller_1.id,
    }

    token = auth_utils.encode_jwt(payload=jwt_payload)

    book_1 = books_jwt.BookJWT(
        seller_id=seller_1.id,
        title="Wrong Code",
        author="Robert Martin",
        count_pages=104,
        year=2007,
    )

    book_2 = books_jwt.BookJWT(
        seller_id=seller_1.id,
        title="Clean Code",
        author="Robert Martin",
        count_pages=104,
        year=2007,
    )

    db_session.add_all([book_1, book_2])
    await db_session.flush()

    headers = {"Authorization": "Bearer " + token}
    response = await async_client.get(
        "/api/v1/jwt/sellers/me/info",
        headers=headers,
    )
    result_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result_data == {
        "id": seller_1.id,
        "first_name": seller_1.first_name,
        "second_name": seller_1.second_name,
        "email": seller_1.email,
        "books": [
            {
                "id": book_1.id,
                "title": book_1.title,
                "author": book_1.author,
                "year": book_1.year,
                "count_pages": book_1.count_pages,
            },
            {
                "id": book_2.id,
                "title": book_2.title,
                "author": book_2.author,
                "year": book_2.year,
                "count_pages": book_2.count_pages,
            },
        ],
    }


@pytest.mark.asyncio
async def test_update_book_seller_jwt(db_session, async_client):
    """
    update seller's book
    """
    await db_session.execute(delete(sellers_jwt.SellerJWT))

    test_password = "test"
    seller_1 = sellers_jwt.SellerJWT(
        email="martiniden@gmail.com",
        password=auth_utils.hash_password(test_password),
        first_name="Martin",
        second_name="Iden",
    )
    db_session.add(seller_1)
    await db_session.flush()

    jwt_payload = {
        "email": seller_1.email,
        "seller_id": seller_1.id,
    }

    token = auth_utils.encode_jwt(payload=jwt_payload)

    book_1 = books_jwt.BookJWT(
        seller_id=seller_1.id,
        title="Wrong Code",
        author="Robert Martin",
        count_pages=104,
        year=2007,
    )

    db_session.add(book_1)
    await db_session.flush()

    data = {
        "title": "Clean Code",
    }
    headers = {"Authorization": "Bearer " + token}
    response = await async_client.put(
        f"/api/v1/jwt/sellers/me/books/{book_1.id}/update",
        data=data,
        headers=headers,
    )
    result_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result_data == {
        "id": book_1.id,
        "seller_id": seller_1.id,
        "title": "Clean Code",
        "author": book_1.author,
        "year": book_1.year,
        "count_pages": book_1.count_pages,
    }


@pytest.mark.asyncio
async def test_delete_book_seller_jwt(db_session, async_client):
    """
    delete seller's book
    """
    await db_session.execute(delete(sellers_jwt.SellerJWT))

    test_password = "test"
    seller_1 = sellers_jwt.SellerJWT(
        email="martiniden@gmail.com",
        password=auth_utils.hash_password(test_password),
        first_name="Martin",
        second_name="Iden",
    )
    db_session.add(seller_1)
    await db_session.flush()

    jwt_payload = {
        "email": seller_1.email,
        "seller_id": seller_1.id,
    }

    token = auth_utils.encode_jwt(payload=jwt_payload)

    book_1 = books_jwt.BookJWT(
        seller_id=seller_1.id,
        title="Wrong Code",
        author="Robert Martin",
        count_pages=104,
        year=2007,
    )

    db_session.add(book_1)
    await db_session.flush()

    headers = {"Authorization": "Bearer " + token}

    response = await async_client.delete(
        f"/api/v1/jwt/sellers/me/books/{book_1.id}/delete_book",
        headers=headers,
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    await db_session.flush()

    all_sellers = await db_session.execute(select(sellers_jwt.SellerJWT))
    res = all_sellers.scalars().all()
    assert len(res) == 1

    all_books = await db_session.execute(select(books_jwt.BookJWT))
    res = all_books.scalars().all()
    assert len(res) == 0


@pytest.mark.asyncio
async def test_delete_seller_jwt(db_session, async_client):
    """
    delete seller
    """
    await db_session.execute(delete(sellers_jwt.SellerJWT))

    test_password = "test"

    seller_1 = sellers_jwt.SellerJWT(
        email="martinidenza@gmail.com",
        password=auth_utils.hash_password(test_password),
        first_name="Martin",
        second_name="Idenza",
    )

    seller_2 = sellers_jwt.SellerJWT(
        email="zenpythonovich@gmail.com",
        password=auth_utils.hash_password(test_password),
        first_name="Zen",
        second_name="Pythonovich",
    )

    db_session.add_all([seller_1, seller_2])
    await db_session.flush()

    book_1 = books_jwt.BookJWT(
        seller_id=seller_1.id,
        title="Wrong Code",
        author="Robert Martin",
        count_pages=104,
        year=2007,
    )

    book_2 = books_jwt.BookJWT(
        seller_id=seller_1.id,
        title="Clean Code",
        author="Robert Martin",
        count_pages=104,
        year=2007,
    )

    book_3 = books_jwt.BookJWT(
        seller_id=seller_2.id,
        title="Wrong Code",
        author="Robert Martin",
        count_pages=104,
        year=2007,
    )

    book_4 = books_jwt.BookJWT(
        seller_id=seller_2.id,
        title="Clean Code",
        author="Robert Martin",
        count_pages=104,
        year=2007,
    )

    db_session.add_all([book_1, book_2, book_3, book_4])
    await db_session.flush()

    jwt_payload = {
        "email": seller_1.email,
        "seller_id": seller_1.id,
    }
    token = auth_utils.encode_jwt(payload=jwt_payload)

    headers = {"Authorization": "Bearer " + token}

    response = await async_client.delete(
        f"/api/v1/jwt/sellers/me/delete_account",
        headers=headers,
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    await db_session.flush()

    all_sellers = await db_session.execute(select(sellers_jwt.SellerJWT))
    res = all_sellers.scalars().all()
    assert len(res) == 1

    all_books = await db_session.execute(select(books_jwt.BookJWT))
    res = all_books.scalars().all()
    assert len(res) == 2
