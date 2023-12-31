import pytest
from jose import jwt
from app import schemas
from app.config import settings
      
# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'We made it, Awesome!'
#     assert res.status_code == 200
    
def test_create_user(client):
    res = client.post("/users/", json={"email": "pedrito@gmail.com", "password": "123456789"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "pedrito@gmail.com"
    assert res.status_code == 201

def test_login_user(test_user, client):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())    
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200    

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', '123456789', 403),
    ('emanuel@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, '123456789', 422),
    ('emanuel@gmail.com', None, 422)
])  
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
    #assert res.json().get('detail') == 'Invalid Credentials'  #DON'T UNCOMMENT THIS LINE
        

def test_create_same_user(test_user, client):
    
    # request = {"email": test_user['email'], "password": "omaiga"}
    # print(request)
    res = client.post("/users/", json={"email": test_user['email'], "password": "omaiga"})
    new_user = res.json()
    print(new_user)
    assert res.status_code == 409
    assert new_user['detail'] == 'Email Already Registered'    