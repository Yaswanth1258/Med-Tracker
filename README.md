# Medicine Dose Tracker

A premium, responsive web application to track your medicine schedule.

## How to Run locally

1.  **Activate Virtual Environment**:
    ```powershell
    .\venv\Scripts\Activate
    ```
    *(You should see `(venv)` appear at the start of your line)*

2.  **Run Server**:
    We use port 5000 to avoid permission issues.
    ```powershell
    python manage.py runserver 5000
    ```

3.  **Access the App**:
    Open your browser -> [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## Admin Panel
To manage users and view logs:
- **URL**: [http://127.0.0.1:5000/admin/](http://127.0.0.1:5000/admin/)
- **Username**: `admin`
- **Password**: `password123`

## Features

### 1. Notifications
To check for overdue medicines based on frequency:
```powershell
python manage.py check_doses
```
*(This will print "Time to take..." notifications to the console for testing)*

### 2. Daily Tracking
- Go to the Dashboard.
- Click "Mark Taken" on a medicine card.
- It will reset daily.
