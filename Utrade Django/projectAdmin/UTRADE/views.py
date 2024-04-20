from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


from . forms import CreateUserForm, LoginForm
#Authentication models and functions
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required



from .models import UserProfile

def Logout(request):
    logout(request)
    return redirect('/login')

@login_required(login_url="/login")
def dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'Utrade/dashboard.html', {'user_profile': user_profile})




def register(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            error_message = 'This username is already taken. Please choose a different one.'
            return render(request, 'Utrade/pages-register.html', {'error_message': error_message})

        my_user = User.objects.create_user(username, email, password)
        my_user.save()

        # Create a UserProfile instance for the new user
        UserProfile.objects.create(user=my_user)

        return redirect('/login')
        # print(username, email, password)
    return render(request, 'Utrade/pages-register.html')

def Login(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/first_interests")
        else:
            error_message = 'User Name or Password is not valid'
            return render(request, 'Utrade/pages-login.html', {'error_message': error_message})
        
    return render(request, 'Utrade/pages-login.html')



@login_required(login_url="/login")
def first_interests(request):
    return render(request, 'Utrade/first_interests.html')

@login_required(login_url="/login")
def next_interests(request):
    return render(request, 'Utrade/next_interests.html')



@login_required(login_url="/login")
def portfolio(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'Utrade/portfolio.html', {'user_profile': user_profile})

@login_required(login_url="/login")
def news(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'Utrade/news.html', {'user_profile': user_profile})

@login_required(login_url="/login")
def search(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'Utrade/search.html', {'user_profile': user_profile})

@login_required(login_url="/login")
def fav(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'Utrade/fav.html', {'user_profile': user_profile})


@login_required(login_url="/login")
def trade(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'Utrade/trade.html', {'user_profile': user_profile})

@login_required(login_url="/login")
def next_trade(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'Utrade/next_trade.html', {'user_profile': user_profile})

@login_required(login_url="/login")
def result(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'Utrade/result.html', {'user_profile': user_profile})



@login_required(login_url="/login")
def contact(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'Utrade/pages-contact.html', {'user_profile': user_profile})

@login_required(login_url="/login")
def user_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'Utrade/users-profile.html', {'user_profile': user_profile})

@login_required(login_url="/login")
def faq(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'Utrade/pages-faq.html', {'user_profile': user_profile})








#################################################################################
#for the database
from .models import UserProfile
from django.http import JsonResponse

@login_required
def profile(request):
    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        new_email = request.POST.get('new_email')

        # Check if the new username is already taken
        if new_username != request.user.username and User.objects.filter(username=new_username).exists():
            error_message = 'This username is already taken. Please choose a different one.'
            return render(request, 'Utrade/users-profile.html', {'error_message': error_message})

        # Update the user's username and email
        request.user.username = new_username
        request.user.email = new_email
        request.user.save()

        return redirect('/users-profile')
    else:
        return render(request, 'Utrade/users-profile.html')



def save_favorite_stocks(request):
    if request.method == 'POST':
        user = request.user  # Assuming the user is logged in
        stocks = request.POST.getlist('favorite_stocks[]')  # Example: ['AAPL', 'GOOGL', 'MSFT']

        # Get the UserProfile instance for the logged-in user
        user_profile = UserProfile.objects.get(user=user)

        # Update the favorite_stocks field
        user_profile.favorite_stocks = stocks
        user_profile.save()

        return HttpResponse("Favorite stocks saved successfully.")
    else:
        return HttpResponse("Invalid request method.")

def get_favorite_stocks(request):
    if request.method == 'GET':
        user = request.user  # Assuming the user is logged in

        try:
            # Get the UserProfile instance for the logged-in user
            user_profile = UserProfile.objects.get(user=user)
            favorite_stocks = user_profile.favorite_stocks
            return JsonResponse({'favorite_stocks': favorite_stocks})
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'UserProfile does not exist for the user.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)




def save_plans(request):
    if request.method == 'POST':
        user = request.user  # Assuming the user is logged in
        plans = request.POST.get('plans', '')  # Assuming 'plans' is the name of the input field

        # Get the UserProfile instance for the logged-in user
        user_profile = UserProfile.objects.get(user=user)

        # Update the plans field
        user_profile.plans = plans
        user_profile.save()

        return HttpResponse("Favorite message saved successfully.")
    else:
        return HttpResponse("Invalid request method.")

def get_plans(request):
    if request.method == 'GET':
        user = request.user  # Assuming the user is logged in

        try:
            # Get the UserProfile instance for the logged-in user
            user_profile = UserProfile.objects.get(user=user)
            plans = user_profile.plans
            return JsonResponse({'plans': plans})
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'UserProfile does not exist for the user.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)




def save_wallet(request):
    if request.method == 'POST':
        user = request.user  # Assuming the user is logged in
        wallet = request.POST.get('wallet', '')  # Assuming 'wallet' is the name of the input field

        # Get the UserProfile instance for the logged-in user
        user_profile = UserProfile.objects.get(user=user)

        # Update the wallet field
        user_profile.wallet = wallet
        user_profile.save()

        return HttpResponse("Favorite message saved successfully.")
    else:
        return HttpResponse("Invalid request method.")

def get_wallet(request):
    if request.method == 'GET':
        user = request.user  # Assuming the user is logged in

        try:
            # Get the UserProfile instance for the logged-in user
            user_profile = UserProfile.objects.get(user=user)
            wallet = user_profile.wallet
            return JsonResponse({'wallet': wallet})
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'UserProfile does not exist for the user.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)




from .forms import ProfilePictureForm

def edit_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES)
        if form.is_valid():
            # Update profile picture
            user_profile.profile_picture = form.cleaned_data['profile_picture']
            print(form.cleaned_data['profile_picture'])
            user_profile.save()
            return redirect('/users-profile')  # Redirect to the user's profile page
    else:
        form = ProfilePictureForm()

    return render(request, 'Utrade/users-profile.html', {'form': form, 'user_profile': user_profile})

def delete_profile_picture(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.profile_picture:
        # Delete the file from storage
        user_profile.profile_picture.delete()
        
        # Set profile_picture to None and save the user profile
        user_profile.profile_picture = None
        user_profile.save()
    
    return redirect('edit_profile')


#these are just for testing ajax

# def is_ajax(request):
#     return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

# # testing
# # def test(request):
# #     return render(request, 'test.html')


# # myapp/views.py

# # def sum_numbers(request):
# #     if request.method == 'GET':
# #         num1 = int(request.GET.get('num1', 0))
# #         num2 = int(request.GET.get('num2', 0))
# #         result = num1 + num2
# #         return JsonResponse({'result': result})
# #     else:
# #         return JsonResponse({'error': 'Invalid request method'})
    
# def sum_numbers(request):
#     return render(request, 'test.html')



# @csrf_exempt
# def calculate(request):

#     if request == None:
#         print('YESS')

#     print(F"REQUEST = {request.body}")
#     data = request.body.decode()
#     print(data)

#     print('\nin calc\n')

#     num1 = int(request.GET.get('d1').decode())
#     num2 = int(request.GET.get('d2').decode())

#     result = num1 + num2

#     response = {'status': 'success', 'res': result}

#     if is_ajax(request):
#         return JsonResponse(response, status=200)


from .models import StockData, Stock
def get_stock_data(request):
    symbol = request.GET.get('symbol', '')  # Assuming you pass 'symbol' as a parameter in your AJAX request
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    # Your query to retrieve StockData based on the parameters
    stock_data = StockData.objects.filter(stock__symbol=symbol, Date__range=(start_date, end_date))

    # Convert the QuerySet to a list of dictionaries
    stock_data_list = [{'Date': entry.Date, 'Open': entry.Open, 'High': entry.High,
                        'Low': entry.Low, 'Close': entry.Close, 'Volume': entry.Volume,
                        'Dividends': entry.Dividends, 'Stock_Splits': entry.Stock_Splits} for entry in stock_data]

    return JsonResponse({'stock_data': stock_data_list})




@csrf_exempt  # Disable CSRF protection for demonstration purposes. You should handle CSRF properly in production.
def add_stock_data(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        stock_symbol = data.get('symbol', '')
        stock_data_list = data.get('stock_data', [])

        # Retrieve or create the Stock object
        stock, created = Stock.objects.get_or_create(symbol=stock_symbol)

        # Iterate through stock data list and create StockData objects
        for stock_data_entry in stock_data_list:
            stock_data = StockData(
                stock=stock,
                Date=stock_data_entry.get('Date'),
                Open=stock_data_entry.get('Open'),
                High=stock_data_entry.get('High'),
                Low=stock_data_entry.get('Low'),
                Close=stock_data_entry.get('Close'),
                Volume=stock_data_entry.get('Volume'),
                Dividends=stock_data_entry.get('Dividends'),
                Stock_Splits=stock_data_entry.get('Stock_Splits')
            )
            stock_data.save()

        return JsonResponse({'status': 'success', 'message': 'Data added successfully'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})