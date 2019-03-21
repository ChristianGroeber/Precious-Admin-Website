from django.shortcuts import render, redirect
from django.template import loader
from .forms import CreateChild, CreateDonationPlan, CreateDonor, LoginUser
from .models import User

# Create your views here.


def login(request):
    form = LoginUser()
    if request.method == 'POST':
        form = LoginUser(request.POST)
        if form.is_valid():
            user = User.objects.all()
            for u in user:
                if u.name == form.cleaned_data['name'] and u.password == form.cleaned_data['password']:
                    return redirect('index')
    return render(request, 'login/login.html', {'form': form})


def index(request):
    return render(request, 'tool/index.html')


def create(request, option):
    print(option)
    if request.method == 'POST':
        form = CreateChild(request.POST)
        if option is 'donor':
            form = CreateDonor(request.POST)
        elif option is 'donation_plan':
            form = CreateDonationPlan(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.save()
            return redirect('index')
    else:
        form = None
        if option == 'child':
            form = CreateChild()
        elif option == 'donor':
            form = CreateDonor()
        elif option == 'donation_plan':
            form = CreateDonationPlan()
        return render(request, 'tool/create.html', {'form': form})
