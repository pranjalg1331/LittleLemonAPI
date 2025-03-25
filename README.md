# Little Lemon API

## Introduction
Welcome to the **Little Lemon API** project! This API provides a fully functional backend for the Little Lemon restaurant, enabling client applications (web and mobile) to interact with the system.

## Scope
The API allows users with different roles to:
- Browse, add, and edit menu items
- Place orders
- Browse orders
- Assign delivery crew to orders
- Manage order delivery status

## Project Structure
This project consists of a **single Django app** named **LittleLemonAPI**. All API endpoints are implemented within this app.

### **Development Setup**
- Use `pipenv` to manage dependencies in a virtual environment.
- Follow Django best practices for API development.
- Use either **function-based views** or **class-based views**.

## **User Groups**
The API defines three user roles:
1. **Manager** - Manages menu items and orders.
2. **Delivery Crew** - Handles order deliveries.
3. **Customer** (default) - Places orders and browses menu items.

User groups and their permissions can be managed through the Django admin panel.

## **API Endpoints**

### **User Authentication and Registration** (via **Djoser**)
| Endpoint | Role | Method | Purpose |
|----------|------|--------|---------|
| `/api/users` | No role required | POST | Creates a new user with name, email, and password |
| `/api/users/me/` | Authenticated users | GET | Displays the current user |
| `/token/login/` | Any valid user | POST | Generates an access token for API requests |

### **Menu Items Endpoints**
| Endpoint | Role | Method | Purpose |
|----------|------|--------|---------|
| `/api/menu-items` | Customer, Delivery Crew | GET | Lists all menu items |
| `/api/menu-items/{menuItem}` | Customer, Delivery Crew | GET | Retrieves a single menu item |
| `/api/menu-items` | Manager | POST | Creates a new menu item |
| `/api/menu-items/{menuItem}` | Manager | PUT, PATCH | Updates a menu item |
| `/api/menu-items/{menuItem}` | Manager | DELETE | Deletes a menu item |

### **User Group Management**
| Endpoint | Role | Method | Purpose |
|----------|------|--------|---------|
| `/api/groups/manager/users` | Manager | GET | Lists all managers |
| `/api/groups/manager/users` | Manager | POST | Assigns a user as a manager |
| `/api/groups/manager/users/{userId}` | Manager | DELETE | Removes a user from the manager role |
| `/api/groups/delivery-crew/users` | Manager | GET | Lists all delivery crew members |
| `/api/groups/delivery-crew/users` | Manager | POST | Assigns a user as delivery crew |
| `/api/groups/delivery-crew/users/{userId}` | Manager | DELETE | Removes a user from delivery crew role |

### **Cart Management**
| Endpoint | Role | Method | Purpose |
|----------|------|--------|---------|
| `/api/cart/menu-items` | Customer | GET | Retrieves the current cart |
| `/api/cart/menu-items` | Customer | POST | Adds an item to the cart |
| `/api/cart/menu-items` | Customer | DELETE | Clears the cart |

### **Order Management**
| Endpoint | Role | Method | Purpose |
|----------|------|--------|---------|
| `/api/orders` | Customer | GET | Retrieves orders for the current user |
| `/api/orders` | Customer | POST | Places an order using cart items |
| `/api/orders/{orderId}` | Customer | GET | Retrieves a specific order |
| `/api/orders/{orderId}` | Manager | PUT, PATCH | Assigns a delivery crew and updates order status |
| `/api/orders/{orderId}` | Manager | DELETE | Deletes an order |
| `/api/orders` | Delivery Crew | GET | Lists all assigned orders |
| `/api/orders/{orderId}` | Delivery Crew | PATCH | Updates order status (delivered or out for delivery) |

## **Error Handling & Status Codes**
| HTTP Status Code | Meaning |
|------------------|---------|
| `200 - OK` | Successful GET, PUT, PATCH, DELETE requests |
| `201 - Created` | Successful POST requests |
| `401 - Forbidden` | Authentication failure |
| `403 - Unauthorized` | Authorization failure |
| `400 - Bad Request` | Validation failure |
| `404 - Not Found` | Requested resource not found |

## **Additional Features**
### **Filtering, Pagination, and Sorting**
- Implement **filtering** for menu items and orders.
- Implement **pagination** to improve performance.
- Implement **sorting** for efficient data retrieval.

### **Throttling**
- Set request limits for authenticated and unauthenticated users.

## **Setup Instructions**
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd LittleLemonAPI
   ```
2. **Setup Virtual Environment**
   ```bash
   pipenv install --dev
   pipenv shell
   ```
3. **Run Migrations**
   ```bash
   python manage.py migrate
   ```
4. **Create Superuser** (for admin access)
   ```bash
   python manage.py createsuperuser
   ```
5. **Start the Server**
   ```bash
   python manage.py runserver
   ```
6. **Access API Documentation**
   - API is accessible at `http://127.0.0.1:8000/api/`
   - Django Admin Panel: `http://127.0.0.1:8000/admin/`

## **Conclusion**
This project provides a robust API for managing restaurant operations. Follow the provided instructions to implement, test, and deploy the API successfully.

### **Happy Coding!** 🚀

