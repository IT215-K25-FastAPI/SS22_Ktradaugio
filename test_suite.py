import time
import requests

BASE_URL = "http://127.0.0.1:8000"
SUFFIX = str(int(time.time()))

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name, condition, extra=""):
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT = PASS_COUNT + 1
        print("  [PASS]", name)
    else:
        FAIL_COUNT = FAIL_COUNT + 1
        print("  [FAIL]", name, extra)


alice = "alice_" + SUFFIX
bob = "bob_" + SUFFIX
admin = "admin_" + SUFFIX

print("=== TrustBank Digital - Test Suite ===")

print("\n1) Dang ky tai khoan")
r = requests.post(BASE_URL + "/api/auth/register", json={"username": alice, "password": "secret123"})
check("Dang ky alice -> 201", r.status_code == 201, r.text)
check("So du khoi tao = 10000.0", r.json().get("balance") == 10000.0, r.text)

r = requests.post(BASE_URL + "/api/auth/register", json={"username": alice, "password": "secret123"})
check("Dang ky trung username -> 409", r.status_code == 409 and r.json()["error"] == "USER_ALREADY_EXISTS", r.text)

r = requests.post(BASE_URL + "/api/auth/register", json={"username": bob, "password": "bobpass1"})
check("Dang ky bob -> 201", r.status_code == 201, r.text)

r = requests.post(BASE_URL + "/api/auth/register", json={"username": admin, "password": "adminpass", "role": "admin"})
check("Dang ky admin -> 201", r.status_code == 201, r.text)

print("\n2) Dang nhap va JWT")
r = requests.post(BASE_URL + "/api/auth/login", json={"username": alice, "password": "wrongpass"})
check("Sai mat khau -> 401", r.status_code == 401 and r.json()["error"] == "INVALID_CREDENTIALS", r.text)

r = requests.post(BASE_URL + "/api/auth/login", json={"username": alice, "password": "secret123"})
check("Dang nhap alice -> 200", r.status_code == 200 and "access_token" in r.json(), r.text)
token_alice = r.json()["access_token"]

r = requests.post(BASE_URL + "/api/auth/login", json={"username": bob, "password": "bobpass1"})
token_bob = r.json()["access_token"]

r = requests.post(BASE_URL + "/api/auth/login", json={"username": admin, "password": "adminpass"})
token_admin = r.json()["access_token"]
check("Dang nhap admin -> 200", r.status_code == 200, r.text)

headers_alice = {"Authorization": "Bearer " + token_alice}
headers_bob = {"Authorization": "Bearer " + token_bob}
headers_admin = {"Authorization": "Bearer " + token_admin}

print("\n3) Xem so du")
r = requests.get(BASE_URL + "/api/account/balance", headers=headers_alice)
check("Xem so du alice -> 200", r.status_code == 200 and r.json()["balance"] == 10000.0, r.text)

r = requests.get(BASE_URL + "/api/account/balance")
check("Khong co token -> 401", r.status_code == 401 and r.json()["error"] == "INVALID_TOKEN", r.text)

r = requests.get(BASE_URL + "/api/account/balance", headers={"Authorization": "Bearer gia.mao.token"})
check("Token gia mao -> 401", r.status_code == 401 and r.json()["error"] == "INVALID_TOKEN", r.text)

print("\n4) Chuyen tien noi bo")
r = requests.post(BASE_URL + "/api/account/transfer", json={"to_username": bob, "amount": 1500, "note": "demo"}, headers=headers_alice)
check("Chuyen 1500 alice->bob -> 200", r.status_code == 200 and r.json()["from_balance_after"] == 8500.0, r.text)

r = requests.post(BASE_URL + "/api/account/transfer", json={"to_username": alice, "amount": 10}, headers=headers_alice)
check("Tu chuyen cho chinh minh -> 400", r.status_code == 400 and r.json()["error"] == "INVALID_TRANSFER", r.text)

r = requests.post(BASE_URL + "/api/account/transfer", json={"to_username": "khong_ton_tai_999", "amount": 10}, headers=headers_alice)
check("Nguoi nhan khong ton tai -> 404", r.status_code == 404 and r.json()["error"] == "RECIPIENT_NOT_FOUND", r.text)

r = requests.post(BASE_URL + "/api/account/transfer", json={"to_username": bob, "amount": -50}, headers=headers_alice)
check("So tien <= 0 -> 422", r.status_code == 422 and r.json()["error"] == "VALIDATION_ERROR", r.text)

r = requests.post(BASE_URL + "/api/account/transfer", json={"to_username": bob, "amount": 999999999}, headers=headers_alice)
check("So du khong du -> 400", r.status_code == 400 and r.json()["error"] == "INSUFFICIENT_BALANCE", r.text)

print("\n5) Phan quyen Admin")
r = requests.get(BASE_URL + "/api/admin/users", headers=headers_alice)
check("Customer goi API admin -> 403", r.status_code == 403 and r.json()["error"] == "PERMISSION_DENIED", r.text)

r = requests.get(BASE_URL + "/api/admin/users", headers=headers_admin)
check("Admin goi API admin -> 200", r.status_code == 200 and isinstance(r.json(), list), r.text)

print("\n6) Doi mat khau")
r = requests.post(BASE_URL + "/api/auth/change-password", json={"old_password": "saipass", "new_password": "newpass1"}, headers=headers_alice)
check("Sai mat khau cu -> 401", r.status_code == 401 and r.json()["error"] == "INVALID_CREDENTIALS", r.text)

r = requests.post(BASE_URL + "/api/auth/change-password", json={"old_password": "secret123", "new_password": "secret123"}, headers=headers_alice)
check("Mat khau moi trung cu -> 400", r.status_code == 400, r.text)

r = requests.post(BASE_URL + "/api/auth/change-password", json={"old_password": "secret123", "new_password": "brandnew123"}, headers=headers_alice)
check("Doi mat khau thanh cong -> 200", r.status_code == 200, r.text)

r = requests.post(BASE_URL + "/api/auth/login", json={"username": alice, "password": "brandnew123"})
check("Dang nhap voi mat khau moi -> 200", r.status_code == 200, r.text)

print("\n=== KET QUA:", PASS_COUNT, "PASS /", FAIL_COUNT, "FAIL /", PASS_COUNT + FAIL_COUNT, "tong cong ===")
