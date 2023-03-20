from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

error_message = str("Book not found!")
delete_message = str("The book has been deleted from the library.")


def test_read_book():
    response = client.get("/view_register/FirstBook")
    assert response.status_code == 200
    assert response.json() == {
        "id":"book1","title":"FirstBook","ISBN":10,"author":"me","genre":None,"pages":100
    }


def test_read_inexistent_book():
    response = client.get("/view_register/LastBook")
    assert response.status_code == 404
    assert response.json() == {
        "detail": error_message
    }





def test_create_book():
    response = client.post("/new_register/", json={"id" : "book4", "title": "FourthBook", "ISBN" : 40, "author" : "me", "genre": None, "pages" : 400})
    assert response.status_code == 200
    assert response.json() == {
        "id" : "book4", "title": "FourthBook", "ISBN" : 40, "author" : "me", "genre": None, "pages" : 400
    }

def test_create_existing_book():
    response = client.post("/new_register/", json={"id" : "book1", "title": "FirstBook", "ISBN" : 10, "author" : "me", "genre": None, "pages" : 100})
    assert response.status_code == 403
    assert response.json() == {
        "detail": "Book already in library, if you want to update it go to /update_register/title."
    }





def test_update_book():
    response =client.put("/update_register/SecondBook", json={"id" : "book2", "title": "SecondBook", "ISBN" : 20, "author" : "you and me", "genre": None, "pages" : 200})
    assert response.status_code == 200
    assert response.json() == {
        "id" : "book2", "title": "SecondBook", "ISBN" : 20, "author" : "you and me", "genre": None, "pages" : 200
    }


def test_update_inexisting_book():
    response =client.put("/update_register/LastBook", json={"id" : "book2", "title": "SecondBook", "ISBN" : 20, "author" : "you and me", "genre": None, "pages" : 200})
    assert response.status_code == 404
    assert response.json() == {
        "detail": error_message
    }





def test_delete_book():
    response = client.delete("/delete_register/FirstBook")
    assert response.status_code == 200
    assert response.json() == delete_message


def test_delete_inexisting_book():
    response = client.delete("/delete_register/LastBook")
    assert response.status_code == 404
    assert response.json() == {
        "detail": error_message
    }
