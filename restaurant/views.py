# file: views.py
# author: theodore harlan hpt@bu.edu
# created: feb 6
# description: controller for the views of restaurant django 

from django.http import HttpRequest
from django.shortcuts import render
import random

# Create your views here.

logo = "https://static.wikia.nocookie.net/undertale-dont-forget/images/c/c0/Bratty_n_catty.PNG/revision/latest?cb=20210212063931"

orderimg = "https://m.media-amazon.com/images/M/MV5BZjVlNDBhN2EtNTM5Yy00YWRiLThmNjQtMzBjMDE1Y2E1NzRjXkEyXkFqcGdeQVRoaXJkUGFydHlJbmdlc3Rpb25Xb3JrZmxvdw@@._V1_.jpg"


menu = {
    "Junk Food" : 20,
    "Hot Dog" : 10,
    "MTT Resort Burger" : 35,
    "Steak in the Shape of Mettaton's Face" : 40,
    "Inedible Cowboy Hat" : 5,
    "Dog Salad (vegan)" : 15
    }

specials = {
    "Snow (vegan)" : 3,
    "Seeds, of the Grass Variety" : 7,
    "Bubblegum, chewed" : 2,
    "Thai-style Khao Moo Dang" : 18,
    "Cinnamon Bun" : 5
    }

hours = {
    "Monday": "11:00 AM - 9:00 PM",
    "Tuesday": "11:00 AM - 9:00 PM",
    "Wednesday": "11:00 AM - 9:00 PM",
    "Thursday": "11:00 AM - 10:00 PM",
    "Friday": "11:00 AM - 11:00 PM",
    "Saturday": "10:00 AM - 11:00 PM",
    "Sunday": "10:00 AM - 8:00 PM",
}


context={ "logo" : logo}


def main(request : HttpRequest):
    """Controller for the main and home pages.
    Send context from the view page to the template renderer"""
    context = {
        "logo" : logo,
        "hours": hours,
        }
    
    return render(request, "restaurant/main.html", context)


def order(request : HttpRequest):
    """Controller for the order page. Fill the context with the
    menu and special items. Generate a special item to send to the renderer"""
    special = random.choice(list(specials.keys()))
    extras = ["Catchup", "Dogchup", "Aligatorchup"]
    context = {
        "menu" : menu,
        "orderimg" : orderimg,
        "special" : special,
        "extras" : extras
        }
    
    return render(request, "restaurant/order.html", context)

    

def confirmation(request: HttpRequest):
    """Controller for the confirmation page. Compute from the post
    request the contities and the total"""
    context = {}
    if request.method == "POST":
        # 1. Store basic customer info
        name = request.POST.get("customer_name")
        email = request.POST.get("customer_email")
        phone = request.POST.get("customer_phone")

        
        special = request.POST.get("special_item") # Hidden input or logic
        hat_extras = request.POST.getlist("hat_extras")

        # 3. Compute the Total
        grand_total = 0
        ordered_items = []
        
        # We use the existing 'menu' dict to validate prices
        for item, price in menu.items():
            # Get the quantity from the form: name="qty_{{ item }}"
            qty_str = request.POST.get(f"qty_{item}", "0")
            
            try:
                qty = int(qty_str)
            except ValueError:
                qty = 0

            if qty > 0:
                line_total = qty * price
                grand_total += line_total
                ordered_items.append({
                    'name': item,
                    'qty': qty,
                    'price': price,
                    'total': line_total
                })

        # 4. Fill the context
        context = {
            "name": name,
            "email": email,
            "phone": phone,
            "ordered_items": ordered_items,
            "grand_total": grand_total,
            "special": special,
            "hat_extras": hat_extras,
        }

    return render(request, "restaurant/confirmation.html", context)
  

