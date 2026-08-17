# TrustBank Digital

API dang nhap va phan quyen ngan hang so, xay dung bang FastAPI + SQLAlchemy + MySQL.

## Cau truc thu muc

```
trustbank_digital/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── dependencies.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── models/
│   │   └── user.py
│   ├── schemas/
│   │   ├── auth.py
│   │   └── account.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── account.py
│   │   └── admin.py
│   └── services/
│       ├── auth_service.py
│       ├── account_service.py
│       └── admin_service.py
├── .env.example
├── .env
├── requirements.txt
├── test_suite.py
└── README.md
```

## Cai dat

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Sao chep `.env.example` thanh `.env` roi dien thong tin MySQL that:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=trustbank_digital

TRUSTBANK_SECRET_KEY=change-this-to-a-long-random-secret-string
```

Khong can tao database thu cong, ung dung se tu tao database va bang khi khoi dong.

## Chay server

```bash
uvicorn app.main:app --reload
```

Server chay tai `http://127.0.0.1:8000`. Swagger UI: `http://127.0.0.1:8000/docs`.

## Chay test

Voi server dang chay o terminal khac:

```bash
python test_suite.py
```

## Danh sach endpoint

- POST /api/auth/register - dang ky, cap 10000 USD ban dau
- POST /api/auth/login - dang nhap, tra ve JWT (het han sau 10 phut)
- POST /api/auth/change-password - doi mat khau (can dang nhap)
- GET /api/account/balance - xem so du (can dang nhap)
- POST /api/account/transfer - chuyen tien noi bo (can dang nhap)
- GET /api/admin/users - danh sach tai khoan (chi admin)

## Ma loi

| Truong hop | HTTP | error |
|---|---|---|
| Username da ton tai | 409 | USER_ALREADY_EXISTS |
| Sai username/password | 401 | INVALID_CREDENTIALS |
| Token khong hop le/het han | 401 | INVALID_TOKEN |
| Khong du quyen | 403 | PERMISSION_DENIED |
| Khong tim thay nguoi nhan | 404 | RECIPIENT_NOT_FOUND |
| So du khong du | 400 | INSUFFICIENT_BALANCE |
| Tu chuyen cho chinh minh | 400 | INVALID_TRANSFER |
| Mat khau moi trung mat khau cu | 400 | SAME_PASSWORD |
| Du lieu sai dinh dang | 422 | VALIDATION_ERROR |
| Loi khong xac dinh | 500 | INTERNAL_SERVER_ERROR |
