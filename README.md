# 🛒 S_Cart — Django E-Commerce & Blog Platform

A full-featured e-commerce web application built with Django, featuring a product shop, seller dashboard, order tracking, and an integrated blog.

---

## ✨ Features

### 🛍️ Shop
- Browse and search products by category
- Product detail pages with ratings & reviews
- Product inquiry system (contact seller directly)
- Session-based shopping cart (AJAX)
- Checkout with order placement
- Order tracking by order ID
- Deal of the Day & Featured Products

### 👤 Auth & Seller Dashboard
- User registration & login
- Seller dashboard to manage own products
- Add / Edit / Delete products
- View & manage product inquiries

### 📝 Blog
- Blog post listing with categories & tags
- Slug-based article URLs
- Post comments
- Create / Edit / Delete posts (authenticated users)
- Featured posts & view counter

---

## 🗂️ Project Structure

```
S_Cart/
├── S_Cart/          # Project settings & root URLs
├── shop/            # E-commerce app (products, orders, cart)
├── blog/            # Blog app (posts, comments)
├── manage.py
├── populate_data.py # Script to seed sample data
├── .env.example     # Environment variable template
└── .gitignore
```

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/shreya-goyal26/S_Cart.git
cd S_Cart
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# or
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
```
Open `.env` and fill in your values:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_ENGINE=sqlite
```

### 5. Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. (Optional) Populate sample data
```bash
python populate_data.py
```

### 7. Create a superuser
```bash
python manage.py createsuperuser
```

### 8. Run the development server
```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**

---

## 🗄️ Database

By default the project uses **SQLite** (no setup needed). To switch to **PostgreSQL**, update `.env`:

```env
DB_ENGINE=postgres
DB_NAME=scart_db
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

---

## 🔑 Environment Variables

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | Django secret key | *(required)* |
| `DEBUG` | Debug mode | `True` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `127.0.0.1,localhost` |
| `DB_ENGINE` | `sqlite` or `postgres` | `sqlite` |
| `DB_NAME` | PostgreSQL database name | `scart_db` |
| `DB_USER` | PostgreSQL username | `postgres` |
| `DB_PASSWORD` | PostgreSQL password | — |
| `DB_HOST` | PostgreSQL host | `localhost` |
| `DB_PORT` | PostgreSQL port | `5432` |

---

## 🛠️ Built With

- [Django](https://www.djangoproject.com/) 6.0
- SQLite / PostgreSQL
- Python · python-dotenv

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
