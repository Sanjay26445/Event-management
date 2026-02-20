# EventHub - Event Management System

A Django-based event management platform for creating, managing, and registering for events.

## Features

- User authentication (Admin, Organizer, Attendee)
- Create and manage events
- Event registration and seat management
- View attendee registrations
- User profiles with images
- Search and filter events
- Responsive design with Bootstrap 5

## Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd eventmanagement
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Setup environment
```bash
cp .env.example .env
```

5. Run migrations
```bash
python manage.py migrate
```

6. Create admin user
```bash
python manage.py createsuperuser
```

7. Start server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`

## Deployment (Free Options)

### Option 1: Render.com (Recommended)

1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. Create new Web Service
4. Connect GitHub repository
5. Set environment variables:
   - `SECRET_KEY`: Generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
   - `DEBUG`: False
   - `ALLOWED_HOSTS`: your-domain.onrender.com
6. Build command: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
7. Start command: `gunicorn event_management.wsgi:application`

### Option 2: Railway.app

1. Push to GitHub
2. Go to [railway.app](https://railway.app)
3. Create new project from GitHub
4. Add PostgreSQL database
5. Set environment variables (same as above)
6. Deploy

### Option 3: Heroku (Limited free tier)

1. Install Heroku CLI
2. `heroku login`
3. `heroku create your-app-name`
4. `git push heroku main`
5. `heroku run python manage.py migrate`

## Project Structure

```
eventmanagement/
├── event_management/    # Django settings
├── events/             # Main app
│   ├── models.py       # Database models
│   ├── views.py        # Views
│   ├── forms.py        # Forms
│   ├── urls.py         # URL routing
│   └── templates/      # HTML templates
├── manage.py
├── requirements.txt
└── README.md
```

## User Roles

- **Admin**: Manage all users and events
- **Organizer**: Create and manage events, view registrations
- **Attendee**: Browse and register for events

## Environment Variables

```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=localhost,yourdomain.com
DATABASE_URL=postgresql://user:password@host/dbname
```

## Database

- Development: SQLite
- Production: PostgreSQL (recommended)

## License

MIT License
