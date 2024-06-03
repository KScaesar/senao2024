# Account and Password Management APIs

This repository contains two RESTful HTTP APIs for creating and verifying accounts and passwords. The APIs are implemented in Python and packaged in a Docker container.


- [Account and Password Management APIs](#account-and-password-management-apis)
  - [Setup Service](#setup-service)
  - [Access APIs](#access-apis)
  - [APIs Spec](#apis-spec)
    - [API 1: Create Account](#api-1-create-account)
    - [API 2: Verify Account and Password](#api-2-verify-account-and-password)
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
   docker compose up -d
   ```

## Access APIs

- Create Account API:  
    ```bash
    curl -X POST http://localhost:12450/v1/api/account \
    -H "Content-Type: application/json" \
    -d '{"username": "caesar", "password": "Senao2450"}'
    ```

- Verify Account API:  
    ```bash
    curl -X POST http://localhost:12450/v1/api/account/verify \
    -H "Content-Type: application/json" \
    -d '{"username": "caesar", "password": "Senao2450"}'
    ```

## APIs Spec

### API 1: Create Account

**Endpoint:** `/v1/api/account`  
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
  "reason": "account created successfully"
}
```

### API 2: Verify Account and Password

**Endpoint:** `/v1/api/account/verify`  
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
  "success": true,
  "reason": "password is ok"
}
```

**Note:** If password verification fails five times, the user must wait one minute before attempting again. The API will return an HTTP status code `429 Too Many Requests`.


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
