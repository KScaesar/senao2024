# Account and Password Management APIs

This repository contains two RESTful HTTP APIs for creating and verifying accounts and passwords. The APIs are implemented in Python and packaged in a Docker container.


- [Account and Password Management APIs](#account-and-password-management-apis)
  - [Setup Service](#setup-service)
  - [Access APIs](#access-apis)
  - [APIs Spec](#apis-spec)
    - [API 1: Create Account](#api-1-create-account)
    - [API 2: Verify Account and Password](#api-2-verify-account-and-password)
  - [Software Architecture](#software-architecture)
    - [adapters](#adapters)
      - [api](#api)
      - [database](#database)
    - [app](#app)
  - [Setup For Developer](#setup-for-developer)
    - [develop for localhost](#develop-for-localhost)
    - [develop for container](#develop-for-container)


## Setup Service

1. Prerequisites:
   - Python 3.10.0+ (Optional)
   - Docker
   - Docker Compose

2. Clone the repository:
   ```bash
   git clone https://github.com/KScaesar/senao2024.git
   cd senao2024
   ```

3. Run the Docker container:
   ```bash
   APP_PORT=12450 MYSQL_PORT=3306 docker compose up -d
   ```
   
4. Close the Docker container:
   ```bash
   docker compose down -v
   ```

## Access APIs

- Create Account API:  
    ```bash
    curl -X POST http://127.0.0.1:12450/api/v1/accounts \
    -H "Content-Type: application/json" \
    -d '{"username": "caesar", "password": "Senao2450"}'
    ```

- Verify Account API:  
    ```bash
    curl -X POST http://127.0.0.1:12450/api/v1/accounts/login \
    -H "Content-Type: application/json" \
    -d '{"username": "caesar", "password": "Senao2450"}'
    ```

## APIs Spec

### API 1: Create Account

**Endpoint:** `/api/v1/accounts`  
**Method:** `POST`

**Request Payload:**
```json
{
  "username": "caesar",
  "password": "Senao2450"
}
```
- `username`: 3-32 characters
- `password`: 8-32 characters, at least 1 uppercase, 1 lowercase, and 1 number

**Response Payload:**
```json
{
  "success": true,
  "reason": ""
}
```

### API 2: Verify Account and Password

**Endpoint:** `/api/v1/accounts/login`  
**Method:** `POST`

**Request Payload:**
```json
{
  "username": "caesar",
  "password": "Senao2450"
}
```

**Response Payload:**
```json
{
  "success": false,
  "reason": "Password does not match. Remaining 2 retry attempts."
}
```

**Note:** If password verification fails five times, the user must wait one minute before attempting again. The API will return an HTTP status code `429 Too Many Requests`.

## Software Architecture

![software architecture](asset/software_architecture.png)

### adapters

負責處理與外界的交互，將外部系統、用戶接口等，連接到應用程式。

#### api

負責處理應用程式對外的 API 接口。

接收外部請求並將其轉換為應用程式可以理解的 command 或 query 。

#### database

儲存、查詢和管理資料的功能。

### app

應用程式的主要業務規則。

## Setup For Developer

### develop for localhost

1. `pyenv install 3.10.13`
2. `pyenv virtualenv 3.10.13 senao2024`
3. `pyenv local senao2024`
4. `ln -s $(pyenv virtualenv-prefix senao2024)/envs/senao2024 .venv`
5. `pip install -r requirements.txt`

### develop for container

1. `pyenv install 3.10.13`
2. `pyenv local 3.10.13`
3. `python -m venv .venv`
4. `source .venv/bin/activate`
5. `pip install -r requirements.txt`
6. `DOCKER_BUILDKIT=1 docker build --build-arg BUILDKIT_INLINE_CACHE=1 -f Dockerfile -t x246libra/senaon2024:v0.1.0 .`
7. `docker push x246libra/senaon2024:v0.1.0`
