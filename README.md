# Coffee-shop-website



☕ Coffee Shop Website

A dynamic and user-friendly coffee shop website built using Flask (Python) for the backend and HTML, CSS, JavaScript for the frontend. This project allows users to place coffee orders, manage their accounts, and provides an admin panel for sales analysis.

🚀 Features

🔹 User Authentication

Sign Up & Login: Secure user authentication with session management.

Logout & Account Deletion: Account gets deleted automatically on logout.

Duplicate Email Handling: Error message displayed if email already exists.


🔹 Coffee Order Management

Order Form: Users can place orders with details like name, email, coffee type, quantity, and date.

Order Confirmation: Users receive a success message after placing an order.

Order Cancellation: Canceled orders are not stored in the database.


🔹 Admin Panel

Admin Login: Separate login for admin to access the dashboard.

Sales Analysis: Monthly order data displayed in table and pie chart format.


🔹 Data Management & Visualization

Orders stored in Flask Database.

Sales trends analyzed using pie charts.

User data displayed in tabular form with monthly bar charts.


🛠️ Tech Stack

Backend: Flask (Python)

Frontend: HTML, CSS, JavaScript (jQuery)

Database: SQLAlchemy

Visualization: Matplotlib


📂 Project Structure

📦 cofs (Project Root)
 ┣ 📂 assets  
 ┃ ┣ 📂 css  
 ┃ ┣ 📂 js  
 ┃ ┣ 📂 images  
 ┣ 📂 templates  
☕ Coffee Shop Website

A dynamic and user-friendly coffee shop website built using Flask (Python) for the backend and HTML, CSS, JavaScript for the frontend. This project allows users to place coffee orders, manage their accounts, and provides an admin panel for sales analysis.

🚀 Features

🔹 User Authentication

Sign Up & Login: Secure user authentication with session management.

Logout & Account Deletion: Account gets deleted automatically on logout.

Duplicate Email Handling: Error message displayed if email already exists.


🔹 Coffee Order Management

Order Form: Users can place orders with details like name, email, coffee type, quantity, and date.

Order Confirmation: Users receive a success message after placing an order.

Order Cancellation: Canceled orders are not stored in the database.


🔹 Admin Panel

Admin Login: Separate login for admin to access the dashboard.

Sales Analysis: Monthly order data displayed in table and pie chart format.


🔹 Data Management & Visualization

Orders stored in Flask Database.

Sales trends analyzed using pie charts.

User data displayed in tabular form with monthly bar charts.


🛠️ Tech Stack

Backend: Flask (Python)

Frontend: HTML, CSS, JavaScript (jQuery)

Database: SQLAlchemy

Visualization: Matplotlib


📂 Project Structure

📦 cofs (Project Root)
 ┣ 📂 assets  
 ┃ ┣ 📂 css  
 ┃ ┣ 📂 js  
 ┃ ┣ 📂 images  
 ┣ 📂 templates  
 ┃ ┣ 📜 index.html  
 ┃ ┣ 📜 login.html  
 ┃ ┣ 📜 signup.html  
 ┃ ┣ 📜 order.html  
 ┃ ┣ 📜 view_order.html  
 ┃ ┣ 📜 analysis.html 
 ┃ ┣ 📜 admin_dashboard.html  
 ┃ ┣ 📜 admin_login.html  
 ┃ ┣ 📜 change_admin_step1.html  
 ┃ ┣ 📜 change_admin_step2.html  
 ┃ ┣ 📜 view_bill.html  
 ┃ ┣ 📜 users.html
 ┣ 📜 app.py  
 ┣ 📜 requirements.txt  
 ┣ 📜 README.md

🔧 Installation & Setup

Step 1: Clone the Repository

git clone  https://github.com/yourusername/coffe-shop.git

Step 2: Create Virtual Environment

python -m venv venv
source venv/bin/activate  # (Linux/Mac)
venv\Scripts\activate  # (Windows)

Step 3: Install Dependencies

pip install -r requirements.txt

Step 4: Run the Application

python app.py  
 ┣ 📜 app.py  
 ┣ 📜 requirements.txt  
 ┣ 📜 README.md

🔧 Installation & Setup

Step 1: Clone the Repository

git clone https://github.com/ArNavalekar/Coffee-shop-website.git

Step 2: Create Virtual Environment

python -m venv venv
source venv/bin/activate  # (Linux/Mac)
venv\Scripts\activate  # (Windows)

Step 3: Install Dependencies

pip install -r requirements.txt

Step 4: Run the Application

python app.py

Step 5: Open in Browser

Go to http://127.0.0.1:8000/ to access the website.



📝 License

This project is for educational purposes. You are free to use and modify it.








