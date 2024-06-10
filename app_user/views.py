from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout as auth_logout
from django.contrib.auth.hashers import make_password, check_password

from django.urls import reverse

from .models import User, Account


def login_page(request):
    global user
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            user_exists = user.check_password(password)
        except User.DoesNotExist:
            user_exists = False

        if user_exists:
            login(request, user)
            return redirect(reverse('home', kwargs={'id': user.id}))
    return render(request, 'login.html')

"""
Purpose: Handles user login functionality.
Request Method: POST to authenticate and GET to render login page.
Parameters: Username and password.
Response: Redirects to the user's home page upon successful login or renders the login page if credentials are invalid.
"""

def registration_page(request):
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            hashed_password = make_password(password2)
            User.objects.create(
                username=request.POST.get('username'),
                first_name=request.POST.get('firstname'),
                last_name=request.POST.get('lastname'),
                password=hashed_password
            )
            return redirect('login')
        else:
            return render(request, 'registration.html', {'eror': 'Password don not match'})
    return render(request, 'registration.html')
"""
Purpose: Handles user registration functionality.
Request Method: POST to register a new user and GET to render the registration page.
Parameters: Username, first name, last name, and password.
Response: Redirects to login page upon successful registration or renders the registration page with an error message if passwords do not match.
"""


def update_user(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        current_password = request.POST.get('current_password')

        # Check if the current password is correct
        if check_password(current_password, user.password):
            new_password = request.POST.get('new_password')

            user.first_name = request.POST.get('firstname')
            user.last_name = request.POST.get('lastname')
            user.username = request.POST.get('username')

            # Update password only if a new one is provided
            if new_password:
                user.password = make_password(new_password)

            user.save()
            return redirect(reverse('home', kwargs={'id': user.id}))
        else:
            # Add an error message if the current password is incorrect
            context = {
                'user': user,
                'error': 'Current password is incorrect'
            }
            return render(request, 'update_user.html', context)

    context = {
        'user': user,
    }
    return render(request, 'update_user.html', context)

"""
Purpose: Handles updating user details.
Request Method: POST to update user details and GET to render the update form.
Parameters: Current password, new password, first name, last name, and username.
Response: Redirects to the user's home page upon successful update or renders the update form with an error message if the current password is incorrect.
"""

def logout_user(request):
    auth_logout(request)
    return redirect('login')

"""
Purpose: Logs out the currently authenticated user.
Request Method: Any.
Response: Redirects to the login page.
"""

def home_page(request, id):
    user = get_object_or_404(User, id=id)
    account_note = Account.objects.filter(owner=user.id)
    context = {
            'user': user,
            'accounts': account_note
            }
    return render(request, 'home.html', context)
"""
Purpose: Renders the user's home page displaying account information.
Request Method: GET.
Parameters: User ID.
Response: Renders the home page with the user's account information.
"""


def create_account(request, id):
    if request.method == 'POST':
        owner = get_object_or_404(User, id=id)
        payment_type = request.POST.get('payment_type')
        total_payment = request.POST.get('total_payment')
        payment_for = request.POST.get('payment_for')

        # Create and save the account
        Account.objects.create(
            payment_type=payment_type,
            total_payment=total_payment,
            payment_for=payment_for,
            owner=owner
        )

        # Redirect to the home page of the logged-in user
        return redirect(reverse('home', kwargs={'id': owner.id}))
    return render(request, 'form.html')
"""
Purpose: Handles the creation of a new account.
Request Method: POST to create an account and GET to render the account creation form.
Parameters: Payment type, total payment, payment for.
Response: Redirects to the user's home page upon successful account creation or renders the account creation form.
"""

def filtered_account(request, id):
    user = get_object_or_404(User, id=id)
    payment_type = request.GET.get('payment_type')
    if payment_type:
        account_note = Account.objects.filter(owner=user, payment_type=payment_type)
    else:
        account_note = Account.objects.filter(owner=user)

    context = {
        'user': user,
        'accounts': account_note,
        'selected_payment_type': payment_type,
    }
    return render(request, 'home.html', context)

"""
Purpose: Filters and displays accounts based on payment type.
Request Method: GET.
Parameters: User ID, payment type.
Response: Renders the home page with filtered account information based on the selected payment type.
"""

def update_account(request, id):
    account = get_object_or_404(Account, pk=id)
    if request.method == 'POST':
        account.payment_type = request.POST.get('payment_type')
        account.total_payment = request.POST.get('total_payment')
        account.payment_for = request.POST.get('payment_for')
        account.save()
        owner = account.owner.id
        return redirect(reverse('home', kwargs={'id': owner}))
    return render(request, 'form.html', {'account':account})

"""
Purpose: Handles updating account details.
Request Method: POST to update account details and GET to render the update form.
Parameters: Payment type, total payment, payment for.
Response: Redirects to the user's home page upon successful update or renders the update form.
"""

def delete_account(request, id):
    account = get_object_or_404(Account, pk=id)
    account.delete()
    user_id = account.owner.id
    return redirect(reverse('home', kwargs={'id': user_id}))
"""
Purpose: Deletes an account.
Request Method: Any.
Parameters: Account ID.
Response: Redirects to the user's home page upon successful deletion.
"""