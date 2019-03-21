from django.shortcuts import render, redirect, get_object_or_404
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
        if option == 'donor':
            form = CreateDonor(request.POST)
        elif option == 'donation_plan':
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
    elif option == 'donor':
        objs = Donor.objects.all()
    elif option == 'donation_plan':
        objs = DonationPlan.objects.all()
    for obj in objs:
        ret.append(obj)
    return render(request, 'tool/view.html', {'option': option, 'ret': ret})


def edit(request, option, id):
    obj = None
    form = None
    if option == 'child':
        obj = get_object_or_404(Child, id=id)
        form = CreateChild(request.POST or None, instance=obj)
    elif option == 'donor':
        obj = get_object_or_404(Donor, id=id)
        form = CreateDonor(request.POST or None, instance=obj)
    elif option == 'donation_plan':
        obj = get_object_or_404(DonationPlan, id=id)
        form = CreateDonationPlan(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request, 'tool/edit.html', {'option': option, 'form': form})
