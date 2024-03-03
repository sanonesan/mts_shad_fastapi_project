import pytest
from fastapi import status
from sqlalchemy import select, delete

from src.models import books
from src.models import sellers


# Тест создание продавцов
@pytest.mark.asyncio
async def test_create_sellers(db_session, async_client):
    """
    Create sellers
    """

    await db_session.execute(delete(sellers.Seller))

    data = {
        "first_name": "Martin",
        "second_name": "Iden",
        "email": "martiniden@gmail.com",
        "password": "test00",
    }
    response = await async_client.post("/api/v1/nonjwt/sellers/", json=data)
    result_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert result_data == {
        "id": 1,
        "first_name": "Martin",
        "second_name": "Iden",
        "email": "martiniden@gmail.com",
    }

    data = {
        "first_name": "Zen",
        "second_name": "Pythonovich",
        "email": "zenpythonovich@gmail.com",
        "password": "test00",
    }
    response = await async_client.post("/api/v1/nonjwt/sellers/", json=data)
    result_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert result_data == {
        "id": 2,
        "first_name": "Zen",
        "second_name": "Pythonovich",
        "email": "zenpythonovich@gmail.com",
    }


# Тест меняем продавца
@pytest.mark.asyncio
async def test_update_sellers(db_session, async_client):
    """
    update seller
    """
    await db_session.execute(delete(sellers.Seller))

    seller = sellers.Seller(
        email="martiniden@gmail.com",
        password="test00",
        first_name="Martin",
        second_name="Iden",
    )
    db_session.add(seller)
    await db_session.flush()

    data = {"first_name": "Martin", "second_name": "Idenza", "email": "martinidenza@gmail.com"}
    response = await async_client.put(f"/api/v1/nonjwt/sellers/{seller.id}", json=data)
    result_data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert result_data == {
        "id": seller.id,
        "first_name": "Martin",
        "second_name": "Idenza",
        "email": "martinidenza@gmail.com",
    }


# Тест получить список продавцoв
@pytest.mark.asyncio
async def test_get_sellers(db_session, async_client):
    """
    Get seller list
    """

    await db_session.execute(delete(sellers.Seller))

    seller_1 = sellers.Seller(
        email="martinidenza@gmail.com",
        password="test00",
        first_name="Martin",
        second_name="Idenza",
    )
    seller_2 = sellers.Seller(
        email="zenpythonovich@gmail.com",
        password="test00",
        first_name="Zen",
        second_name="Pythonovich",
    )

    db_session.add_all([seller_1, seller_2])
    await db_session.flush()

    response = await async_client.get(f"/api/v1/nonjwt/sellers/")
    print(response.json())
    assert response.json() == {
        "sellers": [
            {
                "id": seller_1.id,
                "first_name": "Martin",
                "second_name": "Idenza",
                "email": "martinidenza@gmail.com",
            },
            {
                "id": seller_2.id,
                "first_name": "Zen",
                "second_name": "Pythonovich",
                "email": "zenpythonovich@gmail.com",
            },
        ]
    }


# Создаем книгу для продавца
@pytest.mark.asyncio
async def test_create_book_for_seller(db_session, async_client):
    """
    Create book for seller
    """

    await db_session.execute(delete(sellers.Seller))

    seller_1 = sellers.Seller(
        email="martinidenza@gmail.com",
        password="test00",
        first_name="Martin",
        second_name="Idenza",
    )

    db_session.add(seller_1)
    await db_session.flush()

    data = {
        "seller_id": seller_1.id,
        "title": "Wrong Code",
        "author": "Robert Martin",
        "pages": 104,
        "year": 2007,
    }
    response = await async_client.post(f"/api/v1/nonjwt/books/", json=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "id": 1,
        "seller_id": seller_1.id,
        "title": "Wrong Code",
        "author": "Robert Martin",
        "count_pages": 104,
        "year": 2007,
    }


# Книгу по id
@pytest.mark.asyncio
async def test_get_book_by_id(db_session, async_client):
    """
    Get book by id
    """

    await db_session.execute(delete(sellers.Seller))

    seller_1 = sellers.Seller(
        email="martinidenza@gmail.com",
        password="test00",
        first_name="Martin",
        second_name="Idenza",
    )

    db_session.add(seller_1)
    await db_session.flush()

    book_1 = books.Book(
        seller_id=seller_1.id,
        title="Wrong Code",
        author="Robert Martin",
        count_pages=104,
        year=2007,
    )

    db_session.add(book_1)
    await db_session.flush()

    response = await async_client.get(f"/api/v1/nonjwt/books/{book_1.id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": book_1.id,
        "seller_id": seller_1.id,
        "title": "Wrong Code",
        "author": "Robert Martin",
        "count_pages": 104,
        "year": 2007,
    }


# Получение информации о продавце (с книгами)
@pytest.mark.asyncio
async def test_get_seller_info(db_session, async_client):
    """
    Get seller info by id
    """

    await db_session.execute(delete(sellers.Seller))

    seller_1 = sellers.Seller(
        email="martinidenza@gmail.com",
        password="test00",
        first_name="Martin",
        second_name="Idenza",
    )

    db_session.add(seller_1)
    await db_session.flush()

    book_1 = books.Book(
        seller_id=seller_1.id,
        title="Wrong Code",
        author="Robert Martin",
        count_pages=104,
        year=2007,
    )

    book_2 = books.Book(
        seller_id=seller_1.id,
        title="Clean Code",
        author="Robert Martin",
        count_pages=104,
        year=2007,
    )

    db_session.add_all([book_1, book_2])
    await db_session.flush()

    response = await async_client.get(f"/api/v1/nonjwt/sellers/{seller_1.id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": seller_1.id,
        "first_name": "Martin",
        "second_name": "Idenza",
        "email": "martinidenza@gmail.com",
        "books": [
            {
                "id": book_1.id,
                "title": "Wrong Code",
                "author": "Robert Martin",
                "year": 2007,
                "count_pages": 104,
            },
            {
                "id": book_2.id,
                "title": "Clean Code",
                "author": "Robert Martin",
                "year": 2007,
                "count_pages": 104,
            },
        ],
    }


# Получить cписок всех книг
@pytest.mark.asyncio
async def test_get_all_books(db_session, async_client):
    """
    Get list of books
    """

    await db_session.execute(delete(sellers.Seller))

    seller_1 = sellers.Seller(
        email="martinidenza@gmail.com",
        password="test00",
        first_name="Martin",
        second_name="Idenza",
    )

    db_session.add(seller_1)
    await db_session.flush()

    book_1 = books.Book(
        seller_id=seller_1.id,
        title="Wrong Code",
        author="Robert Martin",
        count_pages=104,
        year=2007,
    )

    book_2 = books.Book(
        seller_id=seller_1.id,
        title="Clean Code",
        author="Robert Martin",
        count_pages=104,
        year=2007,
    )

    db_session.add_all([book_1, book_2])
    await db_session.flush()

    response = await async_client.get(f"/api/v1/nonjwt/books/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "books": [
            {
                "id": book_1.id,
                "seller_id": seller_1.id,
                "title": "Wrong Code",
                "author": "Robert Martin",
                "year": 2007,
                "count_pages": 104,
            },
            {
                "id": book_2.id,
                "seller_id": seller_1.id,
                "title": "Clean Code",
                "author": "Robert Martin",
                "year": 2007,
                "count_pages": 104,
            },
        ],
    }


# Изменить книгу
@pytest.mark.asyncio
async def test_update_book(db_session, async_client):
    """
    update book's info
    """

    await db_session.execute(delete(sellers.Seller))

    seller_1 = sellers.Seller(
        email="martinidenza@gmail.com",
        password="test00",
        first_name="Martin",
        second_name="Idenza",
    )

    db_session.add(seller_1)
    await db_session.flush()

    book_1 = books.Book(
        seller_id=seller_1.id,
        title="Wrong Code",
        author="Robert Martin",
        count_pages=104,
        year=2007,
    )

    db_session.add_all([book_1])
    await db_session.flush()

    data = {
        "seller_id": seller_1.id,
        "title": "Clean Code",
        "author": "Robert Martin",
        "pages": 104,
        "year": 2007,
    }

    response = await async_client.put(f"/api/v1/nonjwt/books/{book_1.id}", json=data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": book_1.id,
        "seller_id": seller_1.id,
        "title": "Clean Code",
        "author": "Robert Martin",
        "year": 2007,
        "count_pages": 104,
    }


# Удалить книгу
@pytest.mark.asyncio
async def test_delete_book(db_session, async_client):
    """
    Delete books info
    """

    await db_session.execute(delete(sellers.Seller))

    seller_1 = sellers.Seller(
        email="martinidenza@gmail.com",
        password="test00",
        first_name="Martin",
        second_name="Idenza",
    )

    db_session.add(seller_1)
    await db_session.flush()

    book_1 = books.Book(
        seller_id=seller_1.id,
        title="Wrong Code",
        author="Robert Martin",
        count_pages=104,
        year=2007,
    )

    book_2 = books.Book(
        seller_id=seller_1.id,
        title="Clean Code",
        author="Robert Martin",
        count_pages=104,
        year=2007,
    )

    db_session.add_all([book_1, book_2])
    await db_session.flush()

    response = await async_client.delete(f"/api/v1/nonjwt/books/{book_1.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    await db_session.flush()

    response = await async_client.get(f"/api/v1/nonjwt/sellers/{seller_1.id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": seller_1.id,
        "first_name": "Martin",
        "second_name": "Idenza",
        "email": "martinidenza@gmail.com",
        "books": [
            {
                "id": book_2.id,
                "title": "Clean Code",
                "author": "Robert Martin",
                "year": 2007,
                "count_pages": 104,
            },
        ],
    }


# Удалить продавца
@pytest.mark.asyncio
async def test_delete_seller(db_session, async_client):
    """
    Delete seller info (with its books)
    """

    await db_session.execute(delete(sellers.Seller))

    seller_1 = sellers.Seller(
        email="martinidenza@gmail.com",
        password="test00",
        first_name="Martin",
        second_name="Idenza",
    )

    seller_2 = sellers.Seller(
        email="zenpythonovich@gmail.com",
        password="test00",
        first_name="Zen",
        second_name="Pythonovich",
    )

    db_session.add_all([seller_1, seller_2])
    await db_session.flush()

    book_1 = books.Book(
        seller_id=seller_1.id,
        title="Wrong Code",
        author="Robert Martin",
        count_pages=104,
        year=2007,
    )

    book_2 = books.Book(
        seller_id=seller_1.id,
        title="Clean Code",
        author="Robert Martin",
        count_pages=104,
        year=2007,
    )

    book_3 = books.Book(
        seller_id=seller_2.id,
        title="Wrong Code",
        author="Robert Martin",
        count_pages=104,
        year=2007,
    )

    book_4 = books.Book(
        seller_id=seller_2.id,
        title="Clean Code",
        author="Robert Martin",
        count_pages=104,
        year=2007,
    )

    db_session.add_all([book_1, book_2, book_3, book_4])
    await db_session.flush()

    response = await async_client.delete(f"/api/v1/nonjwt/sellers/{seller_1.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    await db_session.flush()

    all_books = await db_session.execute(select(books.Book))
    res = all_books.scalars().all()
    assert len(res) == 2
