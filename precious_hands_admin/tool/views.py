from django.shortcuts import render, redirect
from django.template import loader
from .forms import CreateChild, CreateDonationPlan, CreateDonor, LoginUser
from .models import User, Child, Donor, DonationPlan

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
        return render(request, 'tool/create.html', {'form': form, 'option': option})


def view(request, option):
    ret = []
    objs = None
    if option == 'child':
        objs = Child.objects.all()
    for obj in objs:
        ret.append(obj)
    return render(request, 'tool/view.html', {'option': option, 'ret': ret})


def edit(request, option, id):
    obj = None
    if option == 'child':
        obj = Child.objects.get(pk=id)
    return render(request, 'tool/edit.html', {'option': option, 'obj': obj})
