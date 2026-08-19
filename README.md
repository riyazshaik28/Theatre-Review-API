# # 🎭 Theatre Review Platform

A full-stack theatre review platform built with **FastAPI**, **SQLModel**, **SQLite**, and a modern frontend interface. The application allows audiences to submit ratings and reviews for plays, browse reviews, manage feedback, and view average ratings for performances through an interactive user interface.

---

## 🚀 Features

### Backend
- Create reviews
- View all reviews with pagination
- Filter reviews by play name
- Get review by ID
- Update reviews
- Delete reviews
- Calculate average ratings
- RESTful API with Swagger documentation

### Frontend
- User-friendly review submission form
- View all reviews in a clean interface
- Search and filter reviews
- Display average ratings
- Responsive design
- Real-time interaction with backend APIs

---

## 🛠️ Tech Stack

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- FastAPI
- SQLModel
- SQLAlchemy
- SQLite

### Tools
- Git
- GitHub
- Uvicorn

---
## 📂 Project Structure

```text
Theatre-Review-API/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── routes/
│   └── reviews.py
│
├── database.py
├── models.py
├── main.py
├── REVIEWAPI.db
├── requirements.txt
└── README.md
```
---

## ⚙️ Installation

### Clone the Repository

```bash
git clone https://github.com/riyazshaik28/Theatre-Review-API.git
cd Theatre-Review-API
```

### Create Virtual Environment

```bash
python -m venv env
```

### Activate Virtual Environment

#### Windows

```bash
env\Scripts\activate
```

#### Linux / macOS

```bash
source env/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
uvicorn main:app --reload
```

The server will start at:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

## 📌 API Endpoints

### Create Review

**POST**

```http
/review/
```

Request Body:

```json
{
  "play_name": "Hamlet",
  "reviewer_name": "Riyaz",
  "rating": 5,
  "comment": "Outstanding performance"
}
```

---

### Get All Reviews

**GET**

```http
/review/get
```

Query Parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| play_name | string | Filter by play name |
| offset | integer | Pagination offset |
| limit | integer | Number of records to return |

Example:

```http
/review/get?play_name=Hamlet&offset=0&limit=10
```

---

### Get Review By ID

**GET**

```http
/review/getbyid/{id}
```

Example:

```http
/review/getbyid/1
```

---

### Update Review

**PATCH**

```http
/review/getbyid/{id}
```

Request Body:

```json
{
  "rating": 4,
  "comment": "Updated review comment"
}
```

---

### Delete Review

**DELETE**

```http
/review/deletebyid/{id}
```

Example:

```http
/review/deletebyid/1
```

---

### Get Average Rating of a Play

**GET**

```http
/review/avg/{play_name}
```

Example:

```http
/review/avg/Hamlet
```

Response:

```json
{
  "play_name": "Hamlet",
  "average_rating": 4.5,
  "total_reviews": 2
}
```

---

## 🧪 Sample Data

```json
{
  "play_name": "Hamlet",
  "reviewer_name": "Riyaz",
  "rating": 5,
  "comment": "Outstanding performance and excellent acting."
}
```

---

## 🔮 Future Enhancements

- User Authentication & Authorization
- Search Reviews by Reviewer Name
- Sorting by Rating and Date
- PostgreSQL/MySQL Support
- Review Analytics Dashboard
- Like/Dislike Reviews

---

## 👨‍💻 Author

**Shaik Riyaz**

GitHub: https://github.com/riyazshaik28

---

## 📄 License

This project is licensed under the MIT License.
