# E-Commerce Backend

## 📌 Project Overview

This project is a **real-world e-commerce backend system** designed to simulate professional backend development practices. It focuses on **scalability, security, performance, and clean architecture**, providing a solid foundation for a frontend e-commerce application.

The backend manages:

* Product and category data
* User authentication and authorization
* Advanced product discovery (filtering, sorting, pagination)

It is built using **Django**, **PostgreSQL**, and **JWT authentication**, with full **API documentation** via Swagger/OpenAPI.

---

## 🎯 Project Goals

* Build **CRUD APIs** for products, categories, and users
* Implement **secure authentication** using JWT
* Enable **filtering, sorting, and pagination** for product listings
* Design and optimize a **high-performance relational database schema**
* Provide **clear, hosted API documentation** for frontend integration

---

## 🧠 Real-World Application Context

This project mirrors a production-level backend by emphasizing:

* Clean API design
* Database indexing and query optimization
* Secure authentication flows
* Professional Git commit workflow

It is intended to demonstrate backend engineering skills in a realistic scenario.

---

## 🛠️ Technologies Used

* **Django & Django REST Framework** – Scalable backend framework
* **PostgreSQL** – Relational database optimized for performance
* **JWT (JSON Web Tokens)** – Secure user authentication
* **Swagger / OpenAPI** – API documentation and testing

---

## ✨ Key Features

### 1️⃣ CRUD Operations

* Create, read, update, and delete **products**
* Create, read, update, and delete **categories**
* User registration, login, and authentication using JWT

### 2️⃣ Product Discovery APIs

* **Filtering**: Filter products by category
* **Sorting**: Sort products by price (ascending / descending)
* **Pagination**: Efficient handling of large product datasets

### 3️⃣ API Documentation

* Interactive API documentation using **Swagger/OpenAPI**
* Clear request/response schemas for frontend developers
* Publicly accessible hosted API docs

---

## 🗃️ Database Design & Optimization

* Normalized relational schema for products, categories, and users
* Proper **foreign key relationships**
* **Indexes** added to frequently queried fields (e.g., price, category)
* Optimized queries for filtering and pagination

---

## 📦 API Deployment

* The API is deployed and publicly accessible
* Swagger (or Postman) documentation is hosted for easy testing
* Ready for frontend integration

---

## ✅ Evaluation Criteria

### 1️⃣ Functionality

* Full CRUD APIs for products, categories, and users
* Filtering, sorting, and pagination implemented correctly

### 2️⃣ Code Quality

* Clean, readable, and maintainable code
* Proper use of serializers, views, and services
* Database indexing for high-performance queries

### 3️⃣ User Experience

* Comprehensive and user-friendly API documentation
* Secure JWT-based authentication flow

### 4️⃣ Version Control

* Frequent, meaningful Git commits
* Well-structured and organized repository

---

## 📄 How to Run the Project (Optional)

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

Access API docs at:

```
http://127.0.0.1:8000/swagger/
```