# Farm2Consumer
---

````markdown
# 🌿 GreenKart – Farm to Consumer Platform

GreenKart is a full-stack web application that connects **farmers** directly with **consumers**, enabling fresh produce sales without intermediaries.  
It provides two separate dashboards — one for **farmers** to manage products, and one for **consumers** to browse, add to cart, and place orders.

---

## 🧩 Tech Stack

| Layer | Technology Used |
|-------|------------------|
| **Frontend** | HTML, CSS, JavaScript |
| **Backend** | Django (Python Framework) |
| **Database** | Firebase (Realtime Database / Firestore) |
| **Authentication** | Django’s built-in auth system |
| **Hosting (optional)** | Firebase Hosting / Render / PythonAnywhere |

---

## 🏗️ System Architecture

```mermaid
graph TD
A[Frontend - HTML/CSS/JS] --> B[Django Backend]
B --> C[Firebase Database]
B --> D[Django Auth System]
C --> E[Farmer Dashboard]
C --> F[Consumer Dashboard]
F --> G[Cart & Orders]
G --> H[Payment Page]
H --> I[Order Confirmation]
````

---

## 🚀 Features

### 👨‍🌾 Farmer Features

* Login/Signup for farmers
* Add, view, and delete products
* Upload product images
* Manage pricing, quantity, and location

### 🛒 Consumer Features

* Browse available products
* Add items to cart
* View and update cart
* Place orders
* Redirect to payment page
* View order confirmation

### ⚙️ Admin / System

* Role-based authentication (Farmer / Consumer)
* Secure user sessions
* Firebase backend integration

---

## 📁 Project Structure

```
GreenKart/
│
├── greenkart/               # Main Django app
│   ├── models.py             # Models for Users, Products, Cart, Orders
│   ├── views.py              # All app logic and role-based views
│   ├── urls.py               # URL routing
│   └── templates/greenkart/  # All HTML templates
│       ├── login.html
│       ├── signup.html
│       ├── consumer_dashboard.html
│       ├── farmer_dashboard.html
│       ├── cart.html
│       ├── payment.html
│       └── order_success.html
│
├── static/                   # CSS, JS, and images
│   └── default_product.jpg
│
├── db.sqlite3                # Local Django DB (for dev)
├── manage.py
└── README.md
```

---

## ⚙️ Installation and Setup

1. **Clone this repository**

   ```bash
   git clone https://github.com/your-username/GreenKart.git
   cd GreenKart
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv env
   env\Scripts\activate     # On Windows
   source env/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**

   ```bash
   python manage.py migrate
   ```

5. **Run the development server**

   ```bash
   python manage.py runserver
   ```

6. **Access the app**

   ```
   http://127.0.0.1:8000/
   ```

---

## 🔐 Roles and Access

| Role         | Access                                  |
| ------------ | --------------------------------------- |
| **Consumer** | Browse, add to cart, and order products |
| **Farmer**   | Add, view, and delete products          |

---

## 💳 Payment Integration (Demo)

The payment process is simulated through a **payment page** (`payment.html`) for demonstration purposes.
Future enhancement could include:

* Stripe or Razorpay API integration
* Firebase payment status tracking

---

## 🧠 Future Enhancements

* Add product analytics for farmers
* Implement real payment gateway (Stripe/Razorpay)
* Add delivery tracking and notifications
* Integrate AI-based price recommendations

---

## 🧑‍💻 Author

**Vishal**
Computer Science Student | Web Developer
📧 [Your Email Here]
🌐 [Your Portfolio or LinkedIn]

---

## 🪴 License

This project is licensed under the **MIT License**.
You are free to use and modify it with proper attribution.

---

> “Empowering farmers and connecting consumers — one click at a time.” 🌾

```

---

✅ Just copy this entire text and paste it into a file named **`README.md`** in your project root folder.  

Would you like me to **add a “Firebase Setup Guide”** section below installation (to show how to connect Firebase with Django for storage or authentication)?
```
