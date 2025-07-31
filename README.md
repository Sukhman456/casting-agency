
# Casting Agency

## Project Description
The Casting Agency models a company responsible for creating movies and managing actors. This project provides a RESTful API and a frontend interface to manage movies and actors with role-based access control (RBAC).

### Motivation
This project is part of the Udacity Full Stack Nanodegree program. It teaches API development, RBAC implementation, and cloud deployment using Flask, SQLAlchemy, and Auth0.

---

## Hosted URLs
- **Backend API:** https://casting-agency-gfyq.onrender.com
- **Frontend:** https://casting-agency-1-7fwe.onrender.com

---

## Dependencies & Local Development

### Prerequisites
- Python 3.x
- Node.js & npm
- pip

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

---

## Authentication Setup
This project uses Auth0 for authentication & authorization.

1. Create an Auth0 account.
2. Create an API in Auth0 named `casting-agency`.
3. Set permissions:
    - get:movies
    - get:actors
    - post:movies
    - post:actors
    - patch:movies
    - patch:actors
    - delete:movies
    - delete:actors
4. Create roles:
    - **Casting Assistant**: get:movies, get:actors
    - **Casting Director**: All get & patch permissions + post:actors, delete:actors
    - **Executive Producer**: All permissions
5. Update `.env` or config with your Auth0 domain, client ID, and audience.

---

## API Reference

### GET /movies
- Returns a list of movies.
- Requires `get:movies` permission.
```json
{
  "movies": [
    {
      "id": 1,
      "title": "Inception",
      "release_date": "2010-07-16"
    }
  ],
  "success": true
}
```

### GET /actors
- Returns a list of actors.
- Requires `get:actors` permission.

### POST /movies
- Creates a new movie.
- Requires `post:movies` permission.

### POST /actors
- Creates a new actor.
- Requires `post:actors` permission.

### PATCH /movies/<id>
- Updates a movie's details.
- Requires `patch:movies` permission.

### PATCH /actors/<id>
- Updates an actor's details.
- Requires `patch:actors` permission.

### DELETE /movies/<id>
- Deletes a movie.
- Requires `delete:movies` permission.

### DELETE /actors/<id>
- Deletes an actor.
- Requires `delete:actors` permission.

---

## RBAC Controls
- **Casting Assistant**: View actors & movies.
- **Casting Director**: View, edit actors & movies; add/delete actors.
- **Executive Producer**: Full control over actors & movies.

---

## Authors
Developed by Sukhmanpreet Singh as part of the Udacity Full Stack Nanodegree.

---

## Acknowledgements
Thanks to Udacity for the project guidelines and example structure.
