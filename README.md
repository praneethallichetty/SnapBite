<h1>SnapBite</h1>

SnapBite: A full-stack food ordering platform that allows customers to browse restaurants, place orders, and make payments while allowing vendors to manage their restaurant details, orders, and menus.
The platform includes secure user authentication and role-based access control to ensure only authorized users can access specific resources.

---

<h2>Features</h2>

<h3>Customer Features</h3>

**Customer Registration and Login:**
Customers can register and log in to place an order. Only active users can log in.

**Profile Management:**
Customers can edit their personal details (name, email, etc.).

**Order Management:**
Customers can view their order history, including vendor, items, total price, and order status.

**Marketplace:**
Customers can browse a marketplace of approved restaurants.

**Order Placement:**
Customers can place orders from multiple vendors and view available menus.

**Payment:**
Razorpay integration for order payments.

**Access Control:**
Unauthorized access to vendor-specific links or pages results in an error message.

---

<h3>Vendor Features</h3>

**Vendor Registration and Login:**
Vendors can register and log in to manage their restaurant and orders.

**Restaurant Management:**
Vendors can add and edit restaurant details, categories, menu items, and opening hours.

**Order Management:**
Vendors can view and manage orders placed for their restaurant, including customer information, items ordered, and payment status.

**Access Control:**
Unauthorized access to customer-specific pages results in an error message.

**Marketplace Display:**
Vendors’ restaurants are displayed in the marketplace only after backend approval.

---

<h3>Backend Features</h3>

**Approval Process:**
New restaurant listings must be approved by the backend before being visible in the marketplace.

**User Management:**
Admins can manage customer and vendor accounts, activating/deactivating users as needed.

**Order Verification:**
Vendors can verify and update the status of orders placed at their restaurants.

**Error Handling and Access Control:**
Unauthorized access: users trying to access pages or resources they don’t have permission to should be redirected to an “Unauthorized User” page.

**Authentication and Authorization:**
Both are implemented to validate users before accessing specific functionalities.

---

<h3>Database Requirements</h3>

**Customers Table:**
Store customer and vendor information (user type, email, password, etc.), and track user status (active/inactive).

**Restaurants Table:**
Store restaurant details (name, description, categories, menu items, opening hours, approval status).

**Cart Table:**
Store order details (customer, vendor, items, total price, payment status, order status).

**Items Table:**
Store menu items for each restaurant, including item name, description, price, and availability.


---

<h3>Technologies and Tools</h3>

**Frontend**: HTML, CSS, JavaScript

**Backend**: Django (with Django REST Framework) or Flask

**Payment Integration**: Razorpay API for payment processing

**Error Handling**: Proper error handling and redirection for unauthorized access
