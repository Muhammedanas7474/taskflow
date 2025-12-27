# TaskFlow Backend API

TaskFlow is a backend API for managing tasks in software teams, built using Django REST Framework with JWT authentication and role-based access control (RBAC).

This project was implemented as part of a machine test to demonstrate backend development skills such as secure authentication, authorization, data isolation, and RESTful API design.

---

## Features

- JWT Authentication using SimpleJWT
- Role-Based Access Control
  - Backend Developer: can view and update only their own tasks (status only)
  - Project Manager: full access to all tasks (CRUD)
- Secure endpoints with permissions
- SQLite database (easy to replace with PostgreSQL/MySQL)
- RESTful APIs using DRF APIView
- Filtering tasks by status and assignee for managers
- Postman tested
- Modular project structure

---

## Tech Stack

- Python 3.x  
- Django  
- Django REST Framework  
- SimpleJWT  
- SQLite  
- drf-yasg (Swagger)

---



