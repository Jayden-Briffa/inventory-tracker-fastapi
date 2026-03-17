"""
Tests for the Item endpoints.
"""

def test_create_item(client):
    qrCode = "cfcc62ec-d003-447f-936e-c2816cfa3291"
    name = "Test item"
    description = "This is a test item."
    isCollection = False
    response = client.post(
        "/items/",
        json={"qrCode": qrCode, 
              "name": name, 
              "description": description,
              "isCollection": isCollection
              }
    )
    assert response.status_code == 201
    assert response.json() == {
        "itemId": 1,
        "qrCode": qrCode,
        "name": name,
        "description": description,
        "isCollection": isCollection
    }

def test_create_item_with_invalid_fields(client):
    qrCode = 123
    name = True
    description = False
    isCollection = "abc"
    response = client.post(
        "/items/",
        json={"qrCode": qrCode, 
              "name": name, 
              "description": description,
              "isCollection": isCollection
              }
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': [
        {
            'input': qrCode,
            'loc': ['body', 'qrCode'],
            'msg': 'Input should be a valid string',
            "type": 'string_type',
        },
        {
            'input': name,
            'loc': ['body', 'name'],
            'msg': 'Input should be a valid string',
            'type': 'string_type',
        },
        {
            'input': description,
            'loc': ['body', 'description'],
            'msg': 'Input should be a valid string',
            'type': 'string_type',
        },
        {
            'input': isCollection,
            'loc': ['body','isCollection'],
            'msg': 'Input should be a valid boolean, unable to interpret input',
            'type': 'bool_parsing',
        },
        ]
    }

def test_get_items(client):
    populate_database_with_items(client)
    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3 # 3 items in database
    assert data[0] == {'name': 'Test item 1',
                        'isCollection': True, 
                        'itemId': 1, 
                        'qrCode': 'cfcc62ec-d003-447f-936e-c2816cfa3291', 
                        'description': 'This is test item 1.'}
    assert data[1] == {'name': 'Test item 2',
                        'isCollection': True, 
                        'itemId': 2, 
                        'qrCode': '31f5d2f7-9a28-4121-9fa6-9f1190de274d', 
                        'description': 'This is test item 2.'}
    assert data[2] == {'name': 'Test item 3',
                        'isCollection': False, 
                        'itemId': 3, 
                        'qrCode': '4e7bdd31-6cfe-4528-a769-42fcfb01748d', 
                        'description': 'This is test item 3.'}
    
def test_get_items_with_collection_query_false(client):
    populate_database_with_items(client)
    response = client.get("/items?collection=false")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1 # 1 individual item in database
    assert data[0] == {'name': 'Test item 3',
                        'isCollection': False, 
                        'itemId': 3, 
                        'qrCode': '4e7bdd31-6cfe-4528-a769-42fcfb01748d', 
                        'description': 'This is test item 3.'}
    
def test_get_items_with_collection_query_true(client):
    populate_database_with_items(client)
    response = client.get("/items?collection=true")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2 # 2 collection items in database
    assert data[0] == {'name': 'Test item 1',
                        'isCollection': True, 
                        'itemId': 1, 
                        'qrCode': 'cfcc62ec-d003-447f-936e-c2816cfa3291', 
                        'description': 'This is test item 1.'}
    assert data[1] == {'name': 'Test item 2',
                        'isCollection': True, 
                        'itemId': 2, 
                        'qrCode': '31f5d2f7-9a28-4121-9fa6-9f1190de274d', 
                        'description': 'This is test item 2.'}
    
def test_get_items_with_invalid_collection_query(client):
    populate_database_with_items(client)
    response = client.get("/items?collection=abc123")
    assert response.status_code == 422
    data = response.json()
    assert data['detail'][0] == {'type': 'bool_parsing', 
                                 'loc': ['query', 'collection'], 
                                 'msg': 'Input should be a valid boolean, unable to interpret input', 
                                 'input': 'abc123'
                                 }
    
def test_get_item_by_qr_code(client):
    populate_database_with_items(client)
    response = client.get("/items/cfcc62ec-d003-447f-936e-c2816cfa3291")
    assert response.status_code == 200
    assert response.json() == {"qrCode": "cfcc62ec-d003-447f-936e-c2816cfa3291", 
                               "name": "Test item 1", 
                               "itemId": 1,
                               "description": "This is test item 1.",
                               "isCollection": True
                               }
    
def test_get_item_by_nonexistent_qr_code(client):
    populate_database_with_items(client)
    response = client.get("/items/test")
    assert response.status_code == 404
    data = response.json()
    assert data['detail'] ==  "Item with QR code 'test' does not exist."

# def test_update_item(client):
#     populate_database_with_items(client)
#     response = client.patch()

def test_delete_item(client):
    populate_database_with_items(client)
    response = client.get("/items/")
    data = response.json()
    assert len(data) == 3 # 3 items in database
    response = client.delete("/items/cfcc62ec-d003-447f-936e-c2816cfa3291")
    assert response.status_code == 204
    response = client.get("/items/")
    data = response.json()
    assert len(data) == 2 # 2 items in database after deletion

def test_delete_nonexistent_item(client):
    populate_database_with_items(client)
    response = client.get("/items/")
    data = response.json()
    assert len(data) == 3 # 3 items in database
    response = client.delete("/items/test")
    assert response.status_code == 404
    data = response.json()
    assert data['detail'] == "Item with QR code 'test' does not exist."
    response = client.get("/items/")
    data = response.json()
    assert len(data) == 3 # No items deleted from database
    

"""
Helper methods.
"""

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