from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def register(request):
    """Register new user"""
    if request.method != 'POST':
        #Display blank registration form
        form = UserCreationForm()
    else:
        #Process complete form
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Log the user in and redirect to HP
            login(request, new_user)
            return redirect('WebLog:index')
    #Display blank or invalid form
    context = {'form': form}
    return render(request, 'registration/register.html',context)