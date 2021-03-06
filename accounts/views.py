from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from contacts.models import Contact



# Register User
def register(request):
  if request.method == 'POST':
    # Get form data
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']

    # Check password 
    if password == password2:
      # Check username
      if User.objects.filter(username=username).exists():
        messages.error(request, 'Username already taken')
        return redirect('register')
      else:
        # Check for email 
        if User.objects.filter(email=email).exists():
          messages.error(request, 'Email already exist')
          return redirect('register')
        else: 
          user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
          user.save()
          messages.success(request, 'You are now registered and can login')
          return redirect('login')
    else:
      messages.error(request, 'Passwords do not match')
      return redirect('register')
  else:
    return render(request, 'accounts/register.html')


def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None:
      auth.login(request, user)
      messages.success(request, 'logged in')
      return redirect('dashboard')
    else:
      messages.error(request, 'username or password incorrect')
      return redirect('login')
  else:
    return render(request, 'accounts/login.html')

def logout(request):
  if request.method == 'POST':
    auth.logout(request)
    messages.success(request, 'Logged out')
    return redirect('index')

def dashboard(request):
  user_contact = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
  context = {
    'contacts': user_contact
  }
  return render(request, 'accounts/dashboard.html', context)
