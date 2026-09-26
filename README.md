# 🧩 Headhunter — CV Portfolio Management System

A full-stack **web-based CV portfolio management system** that enables job seekers to create, manage, present, and share professional digital portfolios with prospective employers.

Headhunter is designed to provide users with a centralised platform for managing their professional profiles, educational qualifications, work experience, skills, certifications, projects, photographs, and supporting documents, while generating personalised portfolio pages accessible through unique web links.

> **Note:** Headhunter is a **CV portfolio creation, management, presentation, and sharing system**. It is **not** a recruitment, applicant-tracking, candidate-matching, or hiring management platform.

---

## 🎯 Aim and Objectives

### Aim

The aim of this project is to develop **Headhunter**, a web-based CV portfolio website that enables job seekers to create, manage, and present professional digital portfolios for employment opportunities.

### Objectives

The specific objectives of the study are to:

1. Design a responsive web-based CV portfolio management system that provides secure user registration, authentication, and the ability to create, update, and manage professional CVs online.
2. Provide facilities for uploading certificates, project documents, photographs, and other supporting credentials, and generate personalised portfolio pages that can be shared with employers through unique web links.
3. Develop an administrative dashboard for managing users, website content, and overall platform activities.
4. Evaluate the usability and effectiveness of the developed system.

---

## ✨ Features

### 👤 User Management

- Secure user registration and authentication
- User login and logout
- Profile management
- Personal information management
- Profile photograph upload
- Account management

### 📄 CV Management

- Create and edit professional CVs online
- Manage personal and professional information
- Add educational qualifications
- Add work experience
- Manage professional skills
- Add certifications and professional credentials
- Add projects and portfolio items
- Manage CV sections independently
- Generate professional digital CV/portfolio pages

### 📁 Document & Media Management

- Upload certificates
- Upload project documents
- Upload supporting credentials
- Upload profile photographs
- Manage uploaded files
- Organise supporting documents alongside relevant CV information

### 🌐 Digital Portfolio

- Generate personalised public portfolio pages
- Unique portfolio URLs for users
- Share portfolio links with prospective employers
- Responsive portfolio pages for desktop and mobile devices
- Professional presentation of qualifications, skills, experience, certifications, and projects

### 🛠️ Administration

- Administrative dashboard
- User account management
- Website content management
- Platform activity management
- Monitor registered users
- Manage and maintain portfolio-related content

### 📱 Responsive Design

- Mobile-friendly interface
- Desktop and tablet support
- Responsive navigation and components
- Modern UI using Tailwind CSS and DaisyUI
- Interactive server-rendered interfaces using HTMX

---

## 🏗️ Technology Stack

### Backend

- **FastAPI** — High-performance Python web framework
- **SQLModel** — Database models and ORM functionality
- **MySQL** — Relational database management system
- **Pydantic** — Data validation and settings management
- **Uvicorn** — ASGI application server
- **Jinja2** — Server-side HTML templating
- **Pytest** — Automated testing

### Frontend

- **Jinja2 Templates** — Server-rendered HTML
- **HTMX** — Dynamic and interactive page updates without a traditional SPA architecture
- **Tailwind CSS v4** — Utility-first CSS framework
- **DaisyUI** — UI components built on Tailwind CSS
- **Iconify** — Flexible icon system
- **JavaScript** — Client-side interactions where required

### Database & Data Layer

- **MySQL**
- **SQLModel**
- **SQLAlchemy**
- **Pydantic**

### Development & Testing

- **Pytest**
- **HTTPX** — API/application testing
- **Python Virtual Environment**
- **Git & GitHub**

---

## 📁 Suggested Project Structure

```text
headhunter/
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── profile.py
│   │   ├── education.py
│   │   ├── experience.py
│   │   ├── skill.py
│   │   ├── certification.py
│   │   ├── project.py
│   │   └── document.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── profile.py
│   │   └── portfolio.py
│   │
│   ├── routes/
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── profile.py
│   │   ├── education.py
│   │   ├── experience.py
│   │   ├── skills.py
│   │   ├── certifications.py
│   │   ├── projects.py
│   │   ├── documents.py
│   │   ├── portfolio.py
│   │   └── admin.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── portfolio_service.py
│   │   ├── file_service.py
│   │   └── user_service.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── profile/
│   │   ├── portfolio/
│   │   └── admin/
│   │
│   └── static/
│       ├── css/
│       ├── js/
│       └── images/
│
├── tests/
│   ├── test_auth.py
│   ├── test_users.py
│   ├── test_profile.py
│   ├── test_education.py
│   ├── test_experience.py
│   ├── test_projects.py
│   └── test_portfolio.py
│
├── uploads/
├── screenshots/
├── .env.example
├── .gitignore
├── requirements.txt
├── package.json
├── tailwind.config.js
└── README.md
```

---

# ⚙️ Backend Setup — FastAPI

## 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/headhunter.git
cd headhunter
```

---

## 2️⃣ Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Python dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configure MySQL

Create a MySQL database for the application:

```sql
CREATE DATABASE headhunter_db;
```

Create a `.env` file based on `.env.example`:

```env
DATABASE_URL=mysql+mysqlconnector://root:password@localhost/headhunter_db

SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

UPLOAD_DIR=uploads
MAX_UPLOAD_SIZE=10485760

DEBUG=True
```

Update the database credentials according to your local MySQL installation.

---

## 5️⃣ Run database migrations

If database migrations are configured with Alembic:

```bash
alembic upgrade head
```

If migrations are not being used during development, the application can initialise the required database tables according to its database configuration.

---

## 6️⃣ Run the FastAPI application

```bash
uvicorn app.main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

---

## 📚 API Documentation

FastAPI automatically provides interactive API documentation.

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

---

# 🎨 Frontend Setup

Headhunter uses **Jinja2, HTMX, Tailwind CSS, DaisyUI, and Iconify** instead of a separate React/Vue frontend.

## 1️⃣ Install Node.js dependencies

From the project root:

```bash
npm install
```

---

## 2️⃣ Build Tailwind CSS

For development:

```bash
npm run dev
```

For a production build:

```bash
npm run build
```

The generated CSS should be available to the FastAPI application through its configured static files directory.

---

## 3️⃣ Start FastAPI

In another terminal:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

---

# 🔐 Authentication & Security

Headhunter is designed with secure user account management in mind.

The authentication system may include:

- Password hashing
- Secure login and logout
- Session/token-based authentication
- Protected dashboard routes
- Role-based access for administrators
- Input validation using Pydantic
- CSRF protection where applicable
- Secure file upload validation
- File type and file size restrictions
- Environment-based secret configuration
- Protection of private user information

> Never commit `.env`, database credentials, secret keys, or private uploaded documents to version control.

---

# 📂 Supported Portfolio Information

Each user's portfolio can contain sections such as:

```text
Personal Information
├── Full Name
├── Profile Photo
├── Professional Title
├── Biography / About Me
├── Contact Information
└── Social / Professional Links

Education
├── Institution
├── Qualification
├── Field of Study
├── Start Date
├── End Date
└── Description

Work Experience
├── Organisation
├── Job Title
├── Start Date
├── End Date
└── Responsibilities

Skills
├── Technical Skills
├── Professional Skills
└── Skill Level

Certifications
├── Certificate Name
├── Issuing Organisation
├── Issue Date
├── Expiry Date
└── Certificate Document

Projects
├── Project Name
├── Description
├── Technologies Used
├── Project URL
├── Repository URL
└── Supporting Documents
```

---

# 🌐 Public Portfolio URLs

Each registered user can have a unique public portfolio URL.

Example:

```text
http://127.0.0.1:8000/portfolio/john-doe
```

The public portfolio can present:

- Professional profile
- Biography
- Education
- Work experience
- Skills
- Certifications
- Projects
- Supporting credentials
- Contact information
- Professional links

Users can share their portfolio URL directly with prospective employers.

---

# 🧪 Testing

Run all tests with:

```bash
pytest -v
```

Run tests with coverage:

```bash
pytest --cov=app -v
```

Example test structure:

```text
tests/test_auth.py
tests/test_users.py
tests/test_profile.py
tests/test_education.py
tests/test_experience.py
tests/test_projects.py
tests/test_portfolio.py
```

Example output:

```text
tests/test_auth.py::test_register_user PASSED
tests/test_auth.py::test_login_user PASSED
tests/test_profile.py::test_create_profile PASSED
tests/test_education.py::test_create_education PASSED
tests/test_experience.py::test_create_experience PASSED
tests/test_portfolio.py::test_public_portfolio PASSED

========================= 6 passed =========================
```

---

# 🖼️ Screenshots

Screenshots can be stored inside the `screenshots/` directory.

### 🏠 Home Page

![Home Page](screenshots/index_page.png)

### 🔐 Login Page

![Login Page](screenshots/login_page.png)

### 📝 Registration Page

![Registration Page](screenshots/register_page.png)

### 📊 User Dashboard

![Dashboard](screenshots/dashboard.png)

### 👤 Profile Management

![Profile Management](screenshots/profile_management.png)

### 🎓 Education Management

![Education Management](screenshots/education.png)

### 💼 Work Experience

![Work Experience](screenshots/work_experience.png)

### 📜 Certifications

![Certifications](screenshots/certifications.png)

### 🚀 Projects

![Projects](screenshots/projects.png)

### 🌐 Public Portfolio

![Public Portfolio](screenshots/public_portfolio.png)

### 🛠️ Admin Dashboard

![Admin Dashboard](screenshots/admin_dashboard.png)

---

# 📱 Responsive Design

Headhunter is designed as a responsive web application and supports:

- 🖥️ Desktop computers
- 💻 Laptops
- 📱 Mobile phones
- 📟 Tablets

The interface uses **Tailwind CSS** and **DaisyUI** to provide reusable responsive components and consistent styling across supported screen sizes.

---

# ⚡ HTMX

HTMX is used to provide dynamic interactions without requiring a traditional JavaScript single-page application.

Potential HTMX interactions include:

- Inline editing
- Form submission
- Adding CV sections
- Updating portfolio information
- Deleting records
- Modal dialogs
- Partial page updates
- Dynamic dashboard components
- File upload interactions

This allows Headhunter to retain the simplicity of server-rendered Jinja templates while providing a modern interactive experience.

---

# 🎨 UI & Icons

The interface is built using:

- **Tailwind CSS v4**
- **DaisyUI**
- **Iconify**
- Jinja2 templates
- HTMX

Iconify can be used for interface icons:

```html
<span class="iconify" data-icon="mdi:account"></span>
```

The UI follows a responsive and accessible design approach while maintaining a consistent visual language throughout the application.

---

# 🗃️ Database

Headhunter uses **MySQL** as its primary relational database.

The data model may include entities such as:

```text
User
 │
 ├── Profile
 ├── Education
 ├── Work Experience
 ├── Skills
 ├── Certifications
 ├── Projects
 └── Documents
```

SQLModel is used to define Python models and interact with the database.

---

# 👨‍💼 Administrative Dashboard

The administrative section provides authorised administrators with tools for managing the platform.

Possible administrative functions include:

- View registered users
- View user profiles
- Manage user accounts
- Activate/deactivate accounts
- Manage website content
- Monitor uploaded content
- Review platform activity
- Manage administrative roles

Administrative functionality is restricted to authorised users.

---

# 🚫 Project Limitations

Headhunter focuses specifically on **CV portfolio creation and presentation**.

The system does **not** cover advanced recruitment features such as:

- ❌ AI-based candidate matching
- ❌ Automated interview scheduling
- ❌ Online aptitude testing
- ❌ Payroll management
- ❌ Applicant Tracking System (ATS)
- ❌ Automated recruitment workflows
- ❌ Automated hiring decisions
- ❌ Employer-side candidate ranking

The system's primary purpose is to allow job seekers to **create, manage, present, and share professional digital portfolios**.

---

# 🔮 Future Enhancements

Possible future improvements include:

- PDF CV generation
- Multiple portfolio themes
- Portfolio analytics
- QR codes for public portfolios
- Custom portfolio domains
- Email verification
- Password recovery
- Two-factor authentication
- Advanced portfolio templates
- Portfolio SEO optimisation
- Social sharing previews
- Portfolio view statistics
- Cloud-based document storage

These features can be introduced in future versions without changing the core purpose of the system.

---

# 🤝 Contributing

Contributions, suggestions, bug reports, and improvements are welcome.

To contribute:

```bash
git checkout -b feature/your-feature
```

Make your changes, test them, and commit:

```bash
git add .
git commit -m "Add your feature"
git push origin feature/your-feature
```

Then open a pull request.

---

# 📄 License

This project is developed for academic/research purposes.

Add an appropriate open-source license such as MIT if the project is intended to be distributed publicly.

---

# 👨‍💻 Author

- **Selim Adekola**
- 📧 [salimdotpy@gmail.com](mailto:salimdotpy@gmail.com)
- 📞 [+2348076738293](https://wa.me/+2348076738293)

---

## ⭐ Project Summary

**Headhunter** is a responsive web-based CV portfolio management system that provides job seekers with a professional platform for creating, managing, presenting, and sharing their digital professional profiles.

The system combines **FastAPI, MySQL, SQLModel, Jinja2, HTMX, Tailwind CSS v4, DaisyUI, and Iconify** to provide a modern, responsive, and maintainable web application.

> **Headhunter helps job seekers present themselves professionally online — it does not perform recruitment or applicant tracking.**
