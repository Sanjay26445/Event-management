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


