from django.shortcuts import render, redirect, HttpResponse
from django.utils.timezone import now
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from main.models import WorkerRegistration, WorkerType, Contracts, Cards, WorkRequest, Worker_number, Rapid_service
from main.forms import WorkerRegistrationForm

def index(request):
    return redirect('home_page')

def client_form(request):
    if request.method == 'POST':
        worker_type = request.POST.get('worker_type')
        full_name = request.POST.get('full_name')
        full_address = request.POST.get('full_address')
        landmark = request.POST.get('landmark')
        pincode = request.POST.get('pincode')
        contact_number = request.POST.get('contact_number')
        date_of_work = request.POST.get('date_of_work')
        number_workers_required = request.POST.get('number_workers_required')
        work_location_link = request.POST.get('work_location_link')

        # Create and save the WorkRequest object
        work_request = WorkRequest.objects.create(
            worker_type=worker_type,
            full_name=full_name,
            full_address=full_address,
            landmark=landmark,
            pincode=pincode,
            contact_number=contact_number,
            date_of_work=date_of_work,
            number_workers_required=number_workers_required,
            work_location_link=work_location_link
        )

        # Redirect to a success page or another view after saving
        return redirect(reverse('client_payment'))
    worker = Worker_number.objects.all().last()
    
    worker_type = worker.worker_type
    context = {
        'worker_type':worker_type
    }

    return render(request, 'client_form.html',context)

def home_page(request):
    cards = Cards.objects.all()
    context = {"cards": cards}
    if request.user.is_authenticated:
        # Assuming `WorkerRegistration` model has `username` and `full_name`
        context["username"] = request.user.username
        context["full_name"] = request.user.full_name
    else:
        context["username"] = "Guest"
        context["full_name"] = "No Name"
    print(context)
    if request.method == 'POST':
        worker_type = request.POST.get('heading')
        worker_type = Worker_number.objects.create(
            worker_type = worker_type
        )
        return redirect('worker_number')

    return render(request, 'home_page.html', context)

def worker_login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = WorkerRegistration.objects.get(username=username)
            login(request, user)  # Logs in the user without password
            return redirect('home_page')
        except WorkerRegistration.DoesNotExist:
            return HttpResponse("Invalid username")  # Corrected error message display

    return render(request, 'worker_login_page.html')
    
def worker_registration_form(request):
    worker_types = WorkerType.objects.all()
    cards = Cards.objects.all()
    if request.method == 'POST':
        form = WorkerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Initialize worker instance without saving to database
            worker = form.save(commit=False)
            current_year = str(now().year)[-2:]
            worker_types_selected = form.cleaned_data['worker_type']
            worker_type_name = ''
            print(worker)

            # Check if multiple worker types are selected
            if len(worker_types_selected) > 1:
                worker_type_name = "MW"
            elif len(worker_types_selected) == 1:
                # Mapping for single worker types
                cards = Cards.objects.all()
                worker_type_mapping = {card.name: card.code for card in worker_types}
                
                # Retrieve the worker type name
                worker_type_name = worker_type_mapping.get(worker_types_selected.first().name, 'XX')

            # Generate the unique number as a four-digit identifier
            unique_number = WorkerRegistration.objects.count() + 1
            unique_number_formatted = f"{unique_number:04d}" 
            worker.username = f"{current_year}{worker_type_name}{unique_number_formatted}"
            
            # Hash the password correctly
            worker.set_password('password')
            worker.save()
            form.save_m2m()
            login(request, worker)
            
            # Redirect to the username view, passing the username as an argument
            return redirect('username', username=worker.username)
        else:
            print(form.errors) 

    else:
        form = WorkerRegistrationForm()

    return render(request, 'worker_registration_form.html', {
        'form': form,
        'worker_types': worker_types,
        'cards':cards
    })


@login_required
def username(request, username):
    try:
        worker = WorkerRegistration.objects.get(username=username)
        context = {
            'username': worker.username,
            'full_name': worker.get_full_name()  # Assuming `get_full_name` method exists in Worker model
        }
    except WorkerRegistration.DoesNotExist:
        context = {}

    return render(request, 'username.html', context)

def logout_view(request):
    logout(request)
    return redirect('home_page')

from django.shortcuts import render, redirect
from django.contrib import messages

def contract_form(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        full_address = request.POST.get('full_address')
        landmark = request.POST.get('landmark')
        pincode = request.POST.get('pincode')
        contact_number = request.POST.get('contact_number')
        date_of_work = request.POST.get('date_of_work')
        type_of_work = request.POST.get('type_of_work')
        work_location_link = request.POST.get('work_location_link')

        # Create and save the Contracts object
        contract = Contracts.objects.create(
            full_name=full_name,
            full_address=full_address,
            landmark=landmark,
            pincode=pincode,
            contact_number=contact_number,
            date_of_work=date_of_work,
            type_of_work=type_of_work,
            work_location_link=work_location_link
        )

        # Add a success message
        messages.success(request, "Our team will contact you shortly!")
        return redirect('home_page')
    
    return render(request, 'contract_form.html')








import paypalrestsdk
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from paypalrestsdk import Payment

# Configure PayPal with your settings
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # "sandbox" or "live"
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})
import logging
from paypalrestsdk import Payment

def payment_success(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    payment = Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return HttpResponse("Payment completed successfully!")
    else:
        return HttpResponse("Payment failed.")

def payment_cancel(request):
    return HttpResponse("Payment canceled.")


def payment_success(request):
    return HttpResponse('Payment_successful')

def payment_failure(request):
    return HttpResponse('failed')


def convert_inr_to_usd(inr_amount):
    try:
        # Use a currency exchange API
        url = f"https://api.exchangerate-api.com/v4/latest/INR"
        
        # Make the request to get the exchange rates
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        
        data = response.json()
        
        # Get the exchange rate for USD
        exchange_rate = data["rates"]["USD"]
        
        # Convert the INR amount to USD
        usd_amount = inr_amount * exchange_rate
        
        return round(usd_amount, 2)  # Round to 2 decimal places for currency
    except requests.exceptions.RequestException as e:
        print("Error fetching exchange rate:", e)
        return None
    
    


def worker_number(request):
    if request.method == 'POST':
        worker_number = request.POST.get('worker_number')
        worker = Worker_number.objects.all().last()
        worker.worker_number = worker_number
        worker.save()
        return redirect('client_form')
    worker = Worker_number.objects.all().last()
    
    worker_type = worker.worker_type
    context = {
        'worker_type':worker_type
    }
    return render(request,'worker_number.html',context)

FINAL_COST = 0
def payment_page(request):
    # Get the latest Worker_number record
    worker_num = Worker_number.objects.all().last()

    if worker_num:  # Ensure worker_num exists
        worker_number = worker_num.worker_number
        worker_type = worker_num.worker_type
    else:
        # Handle the case where no worker record is found
        worker_number = 0
        worker_type = None

    # Ensure worker_number is an integer
    try:
        worker_number = int(worker_number)
    except ValueError:
        worker_number = 0  # In case the value cannot be converted to an integer

    print(worker_number)
    print(worker_type)

    # Assuming worker_type should match Cards.heading
    if worker_type:
        cards = Cards.objects.filter(heading=worker_type)
    else:
        cards = Cards.objects.none()  # If no worker_type, avoid querying Cards unnecessarily

    amount = 0
    for card in cards:
        amount = card.price  # Assuming the latest card's price is used

    # Ensure amount is treated as an integer
    try:
        amount = float(amount)  # Convert to float if it's a number in string format
    except ValueError:
        amount = 0  # If amount is not a valid number, set it to 0

    # Now you can safely compare amount with integers
    total_amount = amount * worker_number
    margin = 20 * worker_number if amount <= 600 else 30 * worker_number
    final_cost = margin + total_amount
    
    # Store FINAL_COST in session for later access
    request.session['FINAL_COST'] = final_cost
    
    context = {
        'total_amount': total_amount,
        'margin': margin,
        'final_cost': final_cost
    }

    return render(request, 'payment_page.html', context)


import requests
from django.conf import settings

amount_in_dollar = convert_inr_to_usd(FINAL_COST)
import requests
from django.shortcuts import redirect, HttpResponse
import logging

def convert_inr_to_usd(inr_amount):
    try:
        url = "https://api.exchangerate-api.com/v4/latest/INR"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        exchange_rate = data["rates"]["USD"]
        usd_amount = inr_amount * exchange_rate
        return round(usd_amount, 2)
    except requests.exceptions.RequestException as e:
        print("Error fetching exchange rate:", e)
        return None

def create_payment(request):
    # Retrieve FINAL_COST from session
    final_cost_inr = request.session.get('FINAL_COST', 0)
    
    # Convert to USD
    amount_in_dollar = convert_inr_to_usd(final_cost_inr)
    if amount_in_dollar is None:
        logging.error("Currency conversion failed.")
        return HttpResponse("Currency conversion failed. Please try again later.")
    
    # Create PayPal payment
    payment = Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://127.0.0.1:8000/client_form/",
            "cancel_url": "http://127.0.0.1:8000/payment_cancel/"
        },
        "transactions": [{
            "amount": {
                "total": str(amount_in_dollar),
                "currency": "USD"
            },
            "description": "Payment description here."
        }]
    })

    # Attempt to create the payment
    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                return redirect(link.href)
    else:
        error_details = payment.error
        logging.error(f"PayPal Payment Creation Error: {error_details}")
        return HttpResponse("An error occurred while creating the payment. Please try again.")


def rapid_service(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        full_address = request.POST.get('full_address')
        landmark = request.POST.get('landmark')
        pincode = request.POST.get('pincode')
        contact_number = request.POST.get('contact_number')
        date_of_work = request.POST.get('date_of_work')
        type_of_work = request.POST.get('type_of_work')
        work_location_link = request.POST.get('work_location_link')

        # Create and save the Contracts object
        rapid = Rapid_service.objects.create(
            full_name=full_name,
            full_address=full_address,
            landmark=landmark,
            pincode=pincode,
            contact_number=contact_number,
            date_of_work=date_of_work,
            type_of_work=type_of_work,
            work_location_link=work_location_link
        )

        # Add a success message
        messages.success(request, "Our team will contact you shortly!")
        return redirect('home_page')
    return render(request,'rapid_service.html')