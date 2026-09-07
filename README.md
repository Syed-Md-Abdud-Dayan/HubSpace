# HubSpace

**One Hub. Every Purpose.**

HubSpace is a Flask-based web application developed for a tech lounge offering PC rentals and food service under a single platform. The system allows users to reserve Gaming or Study PCs for a specified date and time, browse and order from a food & drinks menu, and complete payments through an integrated SSLCommerz gateway. An administrative dashboard is included for managing reservations, orders, and PC availability in real time.

---

## Features

- **PC Booking** — Reserve a Gaming or Study PC by category, date, time, and duration, with automatic availability checks.
- **Food & Drinks Ordering** — Browse a menu, add items to a cart, and place an order tied to a specific PC number.
- **Payment Integration** — Checkout for both PC bookings and food orders via the SSLCommerz payment gateway.
- **Admin Dashboard** — View and manage reservations, orders, and PC availability from a protected admin panel.
- **Responsive UI** — Bootstrap 5 and custom CSS styling across all pages.

## Tech Stack

| Layer      | Technology                          |
|------------|--------------------------------------|
| Backend    | Python, Flask                        |
| Database   | MySQL                                |
| Frontend   | HTML, CSS, Bootstrap 5, JavaScript   |
| Payments   | SSLCommerz (sandbox)                 |

## Project Structure

```
main
├── db
│   └── hubspace.sql
├── static
│   ├── css
│   │   └── style.css
│   └── images
│       └── logo.png
├── templates
│   ├── admin_login.html
│   ├── admin.html
│   ├── book.html
│   ├── contact.html
│   ├── error.html
│   ├── faq.html
│   ├── index.html
│   ├── menu.html
│   ├── order_success.html
│   ├── order.html
│   └── success.html
├── app.py
└── requirements.txt
```

## Getting Started

### Prerequisites

- Python 3.8+
- MySQL Server
- A SSLCommerz sandbox account (for payment testing)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/hubspace.git
   cd hubspace/main
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database**
   ```bash
   mysql -u root -p < db/hubspace.sql
   ```

4. **Configure environment variables**

   This project currently reads database credentials, the Flask secret key, and SSLCommerz store credentials directly from `app.py`. Before deploying or sharing this project, it's recommended to move these into environment variables (e.g. using `python-dotenv`) rather than hardcoding them:

   - `SECRET_KEY`
   - `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`
   - `SSLCOMMERZ_STORE_ID`, `SSLCOMMERZ_STORE_PASSWORD`

5. **Run the application**
   ```bash
   python app.py
   ```

   The app will be available at `http://127.0.0.1:5000`.

## Admin Access

The admin panel is available at `/admin_login`. Default demo credentials are set in `app.py` — replace these with a secure authentication method before deploying publicly.

## Security Notes

This project was built for learning/demo purposes. Before using it in production:
- Move all secrets (Flask secret key, DB credentials, SSLCommerz keys) to environment variables.
- Replace the hardcoded admin username/password with a proper authentication system (hashed passwords, database-backed users).
- Add CSRF protection to forms.
- Switch from the SSLCommerz sandbox to production credentials only after thorough testing.

## License

This project is not licensed for reuse. All rights reserved — please do not copy, modify, or redistribute this code without permission.
