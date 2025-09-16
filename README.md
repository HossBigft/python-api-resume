# Resume Service 

## Features

- User registration and login (JWT-based)
- Create, read, update, delete resumes
- "Improve" resume endpoint (Stub)
- Pydantic request validation
- Pytest API tests

---

## Tech Stack

- **Backend:** FastAPI  
- **Database:** PostgreSQL (via SQLAlchemy + Alembic)  
- **Authentication:** JWT (OAuth2PasswordBearer)  
- **Validation:** Pydantic  
- **Testing:** Pytest (API & CRUD tests)  
- **Frontend:** React
- **Database management UI:** Adminer 
- **Deployment:**  + Docker Compose  
- **Reverse Proxy & TLS:** Traefik  

---

## Deployment

1. Clone the repository:

```sh
git clone <repo-url>
cd resume-service
```

2. Create env from template and populate it
```sh
cp -v env .env
```

3. Deploy project
Oneliner to deploy project, you need to run it after setting all values in `.env`
```sh
sh scripts/init_environment.sh &&  sudo docker compose up -d
```
