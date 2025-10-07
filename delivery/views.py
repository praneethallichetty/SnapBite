from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.conf import settings
import razorpay
from .models import Customer, Restaurant, Item, Cart
from django.shortcuts import get_object_or_404


# Create your views here.
def index(request):
    return render(request, 'index.html')

def open_signin(request):
    return render(request, 'signin.html')

def open_signup(request):
    return render(request, 'signup.html')

def signup(request):
   #return HttpResponse("Received")
   if request.method == 'POST':
       username = request.POST.get('username')
       password = request.POST.get('password')
       email = request.POST.get('email')
       mobile = request.POST.get('mobile')
       address = request.POST.get('address')

       try:
           Customer.objects.get(username = username)
           return HttpResponse("Duplicate username is not allowed")
       except:
       #Creating Customer table objects (nothing but records in table)
        Customer.objects.create(username = username,
                            password = password,
                            email = email,
                            mobile = mobile,
                            address = address)
   
       return render(request, 'signin.html')
   
def signin(request):
    #return HttpResponse('Received')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == "admin" and password == "admin":
            return render(request, "admin_home.html")
    try:
        customer = Customer.objects.get(username = username, password = password)
        restaurants = Restaurant.objects.all()
        # persist logged-in customer in session for subsequent actions
        request.session['username'] = customer.username
        # if username == "admin":
        #     return render(request, "admin_home.html")
        return render(request, "customer_home.html", {"restaurants": restaurants, "customer": customer})
       # return render(request, "success.html")  
    except Customer.DoesNotExist:
        return render(request, "fail.html")

#Open add restaurant page    
def open_add_restaurant(request):
    return render(request, "add_restaurant.html")

#Adds restaurants
def add_restaurant(request):
    #return HttpResponse("working")
    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')

        Restaurant.objects.create(name=name,
                                  picture=picture,
                                  cuisine=cuisine,
                                  rating=rating)
        
        restaurants = Restaurant.objects.all()
        return render(request, 'show_restaurants.html', {"restaurants": restaurants})
    
    return HttpResponse("Bad Request")

#Show restaurants
def open_show_restaurants(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'display_restaurants.html', {"restaurants": restaurants})


#opens update restaurant page
def open_update_restaurant(request, restaurant_id):
    #return HttpResponse("Working")
    restaurant = Restaurant.objects.get(id = restaurant_id)
    # restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    return render(request, 'update_restaurant.html', {"restaurant": restaurant})

#Update Restaurant
def update_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')
        
        restaurant.name = name
        restaurant.picture = picture
        restaurant.cuisine = cuisine
        restaurant.rating = rating

        restaurant.save()

    restaurant = Restaurant.objects.all()
    return render(request, 'show_restaurants.html', {"restaurants" : restaurant})


#Delete Restaurant
def delete_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == "POST":
        restaurant.delete()
        return redirect("open_show_restaurants")

def open_update_menu(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    itemList = restaurant.items.all()
    #itemList = Item.objects.all()
    return render(request, 'update_menu.html',{"itemList" : itemList, "restaurant" : restaurant})
    
def update_menu(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        vegeterian = request.POST.get('vegeterian') == 'on'
        picture = request.POST.get('picture')
        
        try:
            Item.objects.get(name = name)
            return HttpResponse("Duplicate item!")
        except:
            Item.objects.create(
                restaurant = restaurant,
                name = name,
                description = description,
                price = price,
                vegeterian = vegeterian,
                picture = picture,
            )
    return render(request, 'admin_home.html')


def view_menu(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    itemList = restaurant.items.all()
    #itemList = Item.objects.all()
    customer = None
    username = request.session.get('username')
    if username:
        try:
            customer = Customer.objects.get(username=username)
        except Customer.DoesNotExist:
            customer = None
    return render(request, 'customer_menu.html'
                  ,{"itemList" : itemList,
                     "restaurant" : restaurant,
                     "customer": customer,
                     })

def delete_menu_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    restaurant_id = item.restaurant.id
    
    if request.method == "POST":
        item.delete()
        return redirect("open_update_menu", restaurant_id=restaurant_id)
    
    return redirect("open_update_menu", restaurant_id=restaurant_id)


def add_to_cart(request, item_id):
    username = request.session.get('username')
    if not username:
        # fallback: accept username from POST for cases where session isn't set
        username = request.POST.get('username')
        if username:
            request.session['username'] = username
        else:
            return HttpResponse('Unauthorized', status=401)

    item = get_object_or_404(Item, id=item_id)
    customer = get_object_or_404(Customer, username=username)

    cart, created = Cart.objects.get_or_create(Customer=customer)
    cart.items.add(item)

    return HttpResponse('YaY! Your item was dded to cart')

def view_cart(request):
    username = request.session.get('username')
    if not username:
        # fallback: accept username from query param
        username = request.GET.get('u')
        if username:
            request.session['username'] = username
        else:
            return HttpResponse('Unauthorized', status=401)

    customer = get_object_or_404(Customer, username=username)
    cart, _ = Cart.objects.get_or_create(Customer=customer)
    items = cart.items.all()
    total = cart.total_price() if hasattr(cart, 'total_price') else sum(i.price for i in items)

    return render(request, 'cart.html', {
        "customer": customer,
        "itemList": items,
        "total_price": total,
        "username": customer.username,
    })

def checkout(request, username):
    # Fetch customer and their cart
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(Customer=customer).first()
    cart_items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    if total_price == 0:
        return render(request, 'checkout.html', {
            'error': 'Your cart is empty!',
        })

    # Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Create Razorpay order
    order_data = {
        'amount': int(total_price * 100),  # Amount in paisa
        'currency': 'INR',
        'payment_capture': '1',  # Automatically capture payment
    }
    order = client.order.create(data=order_data)

    # Pass the order details to the frontend
    return render(request, 'checkout.html', {
        'username': username,
        'cart_items': cart_items,
        'total_price': total_price,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'order_id': order['id'],  # Razorpay order ID
        'amount_paise': int(total_price * 100),
    })


# Orders Page
def orders(request, username):
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(Customer=customer).first()

    # Fetch cart items and total price before clearing the cart
    cart_items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    # Clear the cart after fetching its details
    if cart:
        cart.items.clear()

    return render(request, 'orders.html', {
        'username': username,
        'customer': customer,
        'cart_items': cart_items,
        'total_price': total_price,
    })