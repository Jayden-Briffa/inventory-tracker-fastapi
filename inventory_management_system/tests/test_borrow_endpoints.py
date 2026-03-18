"""
Tests for the Borrow endpoints.
"""

# NOTE: Should we use itemId or qrCode? In the item routes we identify items with their qrCode but here it's the id?
def test_create_borrow(client):
    populate_database_with_items(client)
    itemId = 1
    email = "user@test.com"
    borrowDate = "2026-03-10T11:53:50.151000"
    expectedReturnDate = "2026-03-20"
    isReturned = False
    response = client.post(
            "/borrows/",
            json={"itemId": itemId,
              "email": email,
              "borrowDate": borrowDate,
              "expectedReturnDate": expectedReturnDate,
              "isReturned": isReturned
             }
        )
    assert response.status_code == 201
    assert response.json() == {
        "borrowId": 1,
        "itemId": itemId,
        "email": email,
        "borrowDate": borrowDate,
        "expectedReturnDate": expectedReturnDate,
        "isReturned": isReturned
    }

def test_create_borrow_with_invalid_fields(client):
    populate_database_with_items(client)
    itemId = "abc"
    email = False
    borrowDate = True
    expectedReturnDate = 1
    isReturned = "abc"
    response = client.post(
            "/borrows/",
            json={"itemId": itemId,
              "email": email,
              "borrowDate": borrowDate,
              "expectedReturnDate": expectedReturnDate,
              "isReturned": isReturned
             }
        )
    assert response.status_code == 422
    errors = response.json()['detail']
    
    # Check that we have 5 validation errors
    assert len(errors) == 5
    
    # Check error types and locations, independent of order
    error_locs = {tuple(err['loc']): err['type'] for err in errors}
    assert error_locs[('body', 'itemId')] == 'int_parsing'
    assert error_locs[('body', 'email')] == 'string_type'
    assert error_locs[('body', 'borrowDate')] == 'datetime_type'
    assert error_locs[('body', 'expectedReturnDate')] == 'date_from_datetime_inexact'
    assert error_locs[('body', 'isReturned')] == 'bool_parsing'

def test_get_borrows(client):
    populate_database_with_borrows(client)
    response = client.get("/borrows/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3 # 3 borrows in database
    assert data[0] == {'itemId': 1, 
                       'email': 'user2@test.com', 
                       'expectedReturnDate': '2026-03-05', 
                       'borrowDate': '2026-03-01T10:50:50.151000', 
                       'borrowId': 2, 
                       'isReturned': True}
    assert data[1] == {'itemId': 2, 
                       'email': 'user3@test.com', 
                       'expectedReturnDate': '2026-03-08', 
                       'borrowDate': '2026-03-03T10:50:50.151000', 
                       'borrowId': 3, 
                       'isReturned': False}
    assert data[2] == {'itemId': 1, 
                       'email': 'user1@test.com', 
                       'expectedReturnDate': '2026-03-12', 
                       'borrowDate': '2026-03-11T11:53:50.151000', 
                       'borrowId': 1, 
                       'isReturned': False}
    
def test_get_borrows_retrieves_borrows_in_ascending_order_of_expected_return_date(client):
    populate_database_with_borrows(client)
    response = client.get("/borrows/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3 # 3 borrows in database
    firstBorrowDate = data[0]['expectedReturnDate']
    secondBorrowDate = data[1]['expectedReturnDate']
    thirdBorrowDate = data[2]['expectedReturnDate']
    assert firstBorrowDate <= secondBorrowDate
    assert secondBorrowDate <= thirdBorrowDate

def test_get_borrows_with_returned_query_false(client):
    populate_database_with_borrows(client)
    response = client.get("/borrows?returned=false")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2 # 2 active borrows in database
    assert data[0] == {'itemId': 2, 
                       'email': 'user3@test.com', 
                       'expectedReturnDate': '2026-03-08', 
                       'borrowDate': '2026-03-03T10:50:50.151000', 
                       'borrowId': 3, 
                       'isReturned': False}
    assert data[1] == {'itemId': 1, 
                       'email': 'user1@test.com', 
                       'expectedReturnDate': '2026-03-12', 
                       'borrowDate': '2026-03-11T11:53:50.151000', 
                       'borrowId': 1, 
                       'isReturned': False}
    
def test_get_borrows_with_returned_query_true(client):
    populate_database_with_borrows(client)
    response = client.get("/borrows?returned=true")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1 # 1 returned borrows in database
    assert data[0] == {'itemId': 1, 
                       'email': 'user2@test.com', 
                       'expectedReturnDate': '2026-03-05', 
                       'borrowDate': '2026-03-01T10:50:50.151000', 
                       'borrowId': 2, 
                       'isReturned': True}
    
def test_get_borrows_with_invalid_returned_query(client):
    populate_database_with_borrows(client)
    response = client.get("/borrows?returned=abc123")
    assert response.status_code == 422
    data = response.json()
    assert data['detail'][0] == {'type': 'bool_parsing', 
                                 'loc': ['query', 'returned'], 
                                 'msg': 'Input should be a valid boolean, unable to interpret input', 
                                 'input': 'abc123'
                                 }
    
def test_get_borrows_in_ascending_order_of_expected_return_date(client):
    populate_database_with_borrows(client)
    response = client.get("/borrows?order=asc&sort_by=expectedReturnDate")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3 # 3 borrows in database
    assert data[0] == {'itemId': 1, 
                       'email': 'user2@test.com', 
                       'expectedReturnDate': '2026-03-05', 
                       'borrowDate': '2026-03-01T10:50:50.151000', 
                       'borrowId': 2, 
                       'isReturned': True}
    assert data[1] == {'itemId': 2, 
                       'email': 'user3@test.com', 
                       'expectedReturnDate': '2026-03-08', 
                       'borrowDate': '2026-03-03T10:50:50.151000', 
                       'borrowId': 3, 
                       'isReturned': False}
    assert data[2] == {'itemId': 1, 
                       'email': 'user1@test.com', 
                       'expectedReturnDate': '2026-03-12', 
                       'borrowDate': '2026-03-11T11:53:50.151000', 
                       'borrowId': 1, 
                       'isReturned': False}
    firstBorrowDate = data[0]['expectedReturnDate']
    secondBorrowDate = data[1]['expectedReturnDate']
    thirdBorrowDate = data[2]['expectedReturnDate']
    assert firstBorrowDate <= secondBorrowDate
    assert secondBorrowDate <= thirdBorrowDate

def test_get_borrows_in_descending_order_of_expected_return_date(client):
    populate_database_with_borrows(client)
    response = client.get("/borrows?order=desc&sort_by=expectedReturnDate")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3 # 3 borrows in database
    assert data[0] == {'itemId': 1, 
                       'email': 'user1@test.com', 
                       'expectedReturnDate': '2026-03-12', 
                       'borrowDate': '2026-03-11T11:53:50.151000', 
                       'borrowId': 1, 
                       'isReturned': False}
    assert data[1] == {'itemId': 2, 
                       'email': 'user3@test.com', 
                       'expectedReturnDate': '2026-03-08', 
                       'borrowDate': '2026-03-03T10:50:50.151000', 
                       'borrowId': 3, 
                       'isReturned': False}
    assert data[2] == {'itemId': 1, 
                       'email': 'user2@test.com', 
                       'expectedReturnDate': '2026-03-05', 
                       'borrowDate': '2026-03-01T10:50:50.151000', 
                       'borrowId': 2, 
                       'isReturned': True}
    firstBorrowDate = data[0]['expectedReturnDate']
    secondBorrowDate = data[1]['expectedReturnDate']
    thirdBorrowDate = data[2]['expectedReturnDate']
    assert firstBorrowDate >= secondBorrowDate
    assert secondBorrowDate >= thirdBorrowDate

def test_get_borrows_in_ascending_order_of_borrow_date(client):
    populate_database_with_borrows(client)
    response = client.get("/borrows?order=asc&sort_by=borrowDate")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3 # 3 borrows in database
    assert data[0] == {'itemId': 1, 
                       'email': 'user2@test.com', 
                       'expectedReturnDate': '2026-03-05', 
                       'borrowDate': '2026-03-01T10:50:50.151000', 
                       'borrowId': 2, 
                       'isReturned': True}
    assert data[1] == {'itemId': 2, 
                       'email': 'user3@test.com', 
                       'expectedReturnDate': '2026-03-08', 
                       'borrowDate': '2026-03-03T10:50:50.151000', 
                       'borrowId': 3, 
                       'isReturned': False}
    assert data[2] == {'itemId': 1, 
                       'email': 'user1@test.com', 
                       'expectedReturnDate': '2026-03-12', 
                       'borrowDate': '2026-03-11T11:53:50.151000', 
                       'borrowId': 1, 
                       'isReturned': False}
    firstBorrowDate = data[0]['borrowDate']
    secondBorrowDate = data[1]['borrowDate']
    thirdBorrowDate = data[2]['borrowDate']
    assert firstBorrowDate <= secondBorrowDate
    assert secondBorrowDate <= thirdBorrowDate

def test_get_borrows_in_descending_order_of_borrow_date(client):
    populate_database_with_borrows(client)
    response = client.get("/borrows?order=desc&sort_by=borrowDate")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3 # 3 borrows in database
    assert data[0] == {'itemId': 1, 
                       'email': 'user1@test.com', 
                       'expectedReturnDate': '2026-03-12', 
                       'borrowDate': '2026-03-11T11:53:50.151000', 
                       'borrowId': 1, 
                       'isReturned': False}
    assert data[1] == {'itemId': 2, 
                       'email': 'user3@test.com', 
                       'expectedReturnDate': '2026-03-08', 
                       'borrowDate': '2026-03-03T10:50:50.151000', 
                       'borrowId': 3, 
                       'isReturned': False}
    assert data[2] == {'itemId': 1, 
                       'email': 'user2@test.com', 
                       'expectedReturnDate': '2026-03-05', 
                       'borrowDate': '2026-03-01T10:50:50.151000', 
                       'borrowId': 2, 
                       'isReturned': True}
    firstBorrowDate = data[0]['borrowDate']
    secondBorrowDate = data[1]['borrowDate']
    thirdBorrowDate = data[2]['borrowDate']
    assert firstBorrowDate >= secondBorrowDate
    assert secondBorrowDate >= thirdBorrowDate

def test_get_borrows_order_query_with_no_sort_by_query_has_no_effect(client):
    populate_database_with_borrows(client)
    queryResponse = client.get("/borrows?order=asc")
    assert queryResponse.status_code == 200
    queryData = queryResponse.json()
    nonQueryResponse = client.get("/borrows/")
    assert nonQueryResponse.status_code == 200
    nonQueryData = nonQueryResponse.json()
    assert queryData == nonQueryData
    
    
def test_get_borrows_sort_by_query_with_no_order_query_has_no_effect(client):
    populate_database_with_borrows(client)
    queryResponse = client.get("/borrows?sort_by=borrowDate")
    assert queryResponse.status_code == 200
    queryData = queryResponse.json()
    nonQueryResponse = client.get("/borrows/")
    assert nonQueryResponse.status_code == 200
    nonQueryData = nonQueryResponse.json()
    assert queryData == nonQueryData
    
    
def test_get_borrows_order_query_must_be_asc_or_desc_or_else_error(client):
    populate_database_with_borrows(client)
    queryResponse = client.get("/borrows?order=abc&sort_by=borrowDate")
    assert queryResponse.status_code == 400
    data = queryResponse.json()
    assert data['detail'] == "Invalid order. Must be 'asc' or 'desc'"


# I've added more sorting options, feel free to remove the additional options or remove this test - George

# def test_get_borrows_sort_by_query_must_be_expected_return_date_or_borrow_date_or_else_has_no_effect(client):
#     populate_database_with_borrows(client)
#     queryResponse = client.get("/borrows?order=asc&sort_by=abc")
#     assert queryResponse.status_code == 200
#     queryData = queryResponse.json()
#     nonQueryResponse = client.get("/borrows/")
#     assert nonQueryResponse.status_code == 200
#     nonQueryData = nonQueryResponse.json()
#     assert queryData == nonQueryData

def test_get_borrow_by_id(client):
    populate_database_with_borrows(client)
    response = client.get("/borrows/1")
    assert response.status_code == 200
    assert response.json() == {'itemId': 1, 
                              'email': 'user1@test.com', 
                              'expectedReturnDate': '2026-03-12', 
                              'borrowDate': '2026-03-11T11:53:50.151000', 
                              'borrowId': 1, 
                              'isReturned': False}
    
def test_get_borrow_by_nonexistent_qr_code(client):
    populate_database_with_borrows(client)
    response = client.get("/borrows/9")
    assert response.status_code == 404
    data = response.json()
    assert data['detail'] ==  "Borrow with ID '9' does not exist."

def test_get_borrow_by_invalid_qr_code(client):
    populate_database_with_borrows(client)
    response = client.get("/borrows/test")
    assert response.status_code == 422
    

# def test_update_borrow(client):
#     populate_database_with_borrows(client)
#     response = client.patch()

def test_delete_borrow(client):
    populate_database_with_borrows(client)
    response = client.get("/borrows/")
    data = response.json()
    assert len(data) == 3 # 3 borrows in database
    response = client.delete("/borrows/1")
    assert response.status_code == 204
    response = client.get("/borrows/")
    data = response.json()
    assert len(data) == 2 # 2 borrows in database after deletion

def test_delete_nonexistent_borrow(client):
    populate_database_with_borrows(client)
    response = client.get("/borrows/")
    data = response.json()
    assert len(data) == 3 # 3 borrows in database
    response = client.delete("/borrows/123")
    assert response.status_code == 404
    data = response.json()
    assert data['detail'] == "Borrow with ID '123' does not exist."
    response = client.get("/borrows/")
    data = response.json()
    assert len(data) == 3 # No borrows deleted from database
    

"""
Helper methods.
"""

def populate_database_with_borrows(client):
    """Create items and 3 borrows in the database."""
    populate_database_with_items(client)
    
    """Create 3 borrows in the database."""
    client.post(
        "/borrows/",
        json={"itemId": 1,
              "email": "user1@test.com",
              "borrowDate": "2026-03-11T11:53:50.151000",
              "expectedReturnDate": "2026-03-12",
              "isReturned": False
             }
    )
    client.post(
        "/borrows/",
        json={"itemId": 1,
              "email": "user2@test.com",
              "borrowDate": "2026-03-01T10:50:50.151000",
              "expectedReturnDate": "2026-03-05",
              "isReturned": True
             }
    )
    client.post(
        "/borrows/",
        json={"itemId": 2,
              "email": "user3@test.com",
              "borrowDate": "2026-03-03T10:50:50.151000",
              "expectedReturnDate": "2026-03-08",
              "isReturned": False
             }
    )

def populate_database_with_items(client):
    """Create 3 items in the database."""
    client.post(
        "/items/",
        json={"qrCode": "cfcc62ec-d003-447f-936e-c2816cfa3291", 
              "name": "Test item 1", 
              "description": "This is test item 1.",
              "isCollection": True
              }
    )
    client.post(
        "/items/",
        json={"qrCode": "31f5d2f7-9a28-4121-9fa6-9f1190de274d", 
              "name": "Test item 2", 
              "description": "This is test item 2.",
              "isCollection": True
              }
    )
    client.post(
        "/items/",
        json={"qrCode": "4e7bdd31-6cfe-4528-a769-42fcfb01748d", 
              "name": "Test item 3", 
              "description": "This is test item 3.",
              "isCollection": False
              }
    )