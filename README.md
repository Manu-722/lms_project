#  Learning Management System (LMS)

A full-featured Learning Management System built with Django and Django REST Framework. Supports role-based access for instructors and students, secure JWT authentication, assignment submissions, grading, messaging, and more.

---

##  Features

### Authentication & Roles
- JWT-based login and token refresh
- Custom user model with `student` and `instructor` roles
- Role-based permissions for all views

### Course Management
- Instructors can create and manage courses
- Students can enroll in courses
- Prerequisite support for course structure

###  Lectures & Assignments
- Instructors can add lectures and assignments to their courses
- Assignments have due dates and are linked to specific courses

###  Submissions & Grading
- Students can submit assignments (with optional file upload)
- Deadline enforcement blocks late submissions
- Instructors can grade and provide feedback
- Students can view their grades and progress

###  Messaging System
- Instructors and students can send messages related to a course
- Inbox, sent messages, and read/unread tracking

---

##  Tech Stack

- Python 3.x
- Django 5.x
- Django REST Framework
- Simple JWT
- PostgreSQL 
- Bootstrap or React

---

##  Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Manu-722/lms_core.git
cd lms_core