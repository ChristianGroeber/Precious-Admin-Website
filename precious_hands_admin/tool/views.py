import django
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateChild, CreateDonationPlan, CreateDonor, CustomUserCreationForm, Donate
from .models import Child, Donor, DonationPlan
from django.contrib.auth import authenticate, login, logout, forms
from django.contrib.auth.models import User


# Create your views here.


def user_login(request):
    form = forms.AuthenticationForm()
    print(form)
    if request.method == 'POST':
        print('post')
        form = forms.AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('index')
    return render(request, 'login/login.html', {'form': form})


def index(request):
    if str(request.user) is 'AnonymousUser':
        return redirect('login')
    return render(request, 'tool/index.html', {'user_type': request.user.is_superuser})


def create(request, option):
    if str(request.user) is 'AnonymousUser':
        return redirect('login')
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
        elif option == 'user' and request.user.is_superuser:
            form = forms.UserCreationForm()
        return render(request, 'tool/create.html', {'form': form, 'option': option})


def view(request, option):
    if str(request.user) is 'AnonymousUser':
        return redirect('login')
    ret = []
    objs = None
    if option == 'child':
        objs = Child.objects.all()
    elif option == 'donor':
        objs = Donor.objects.all()
    elif option == 'donation_plan':
        objs = DonationPlan.objects.all()
    elif option == 'user' and request.user.is_superuser:
        objs = django.contrib.auth.models.User.objects.all()
    for obj in objs:
        ret.append(obj)
    return render(request, 'tool/view.html', {'option': option, 'ret': ret})


def donate(request, id):
    donation_plan = get_object_or_404(DonationPlan, id=id)
    form = Donate()
    return render(request, 'tool/donate.html', {'donation_plan': donation_plan, 'form': form})


def edit(request, option, id):
    if str(request.user) is 'AnonymousUser':
        return redirect('login')
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
    elif option == 'user' and request.user.is_superuser:
        form = forms.UserChangeForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request, 'tool/edit.html', {'option': option, 'form': form})


def create_user(request):
    if str(request.user) is 'AnonymousUser':
        return redirect('login')
    form = forms.UserCreationForm()
    if request.method == 'POST' and form.is_valid():
        print(request.POST)
        user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
        forms.UserCreationForm(request.POST).save()
    print(request.method)
    return render(request, 'tool/create.html', {'form': form})


def user_logout(request):
    if str(request.user) is 'AnonymousUser':
        return redirect('login')
    logout(request)
    return redirect('login')


def edit_user(request):
    if str(request.user) is 'AnonymousUser':
        return redirect('login')
    form = CustomUserCreationForm(request.POST)
    if request.method == 'POST':
        form.save(request)
        return redirect('index')
    return render(request, 'tool/edit.html', {'form': form})
