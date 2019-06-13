import django, csv, io
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError

from .forms import CreateChild, CreateDonationPlan, CreateDonor, Donate, ImportForm
from .models import Child, Donor, DonationPlan, Donation, Title
from django.contrib.auth import authenticate, login, logout, forms
from django.contrib.auth.models import User


# Create your views here.


def user_login(request):
    form = forms.AuthenticationForm()
    if request.method == 'POST':
        form = forms.AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
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
            form = forms.UserCreationForm(request.POST)
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
    elif option == 'donate':
        objs = Donation.objects.all()
    for obj in objs:
        ret.append(obj)
    return render(request, 'tool/view.html', {'option': option, 'ret': ret})


def donate(request, id=None):
    donation_plan = None
    form = Donate()
    if id:
        donation_plan = get_object_or_404(DonationPlan, id=id)
        form = Donate(request.POST or None, instance=donation_plan)
    else:
        donation_plan = DonationPlan.objects.all()
    if request.method == 'POST':
        form = Donate(request.POST)
        form.save()
        return redirect('index')
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


def import_donor(io_string):
    for column in csv.reader(io_string, delimiter=',', quotechar='|'):
        title = column[0]
        for i in Title.objects.all():
            if i.name == title:
                title = i
                break
        else:
            title = Title.objects.get(pk=1)
        letter_paper = column[9] == 'x'
        letter_mail = column[10] == 'x'
        is_member = column[11] == 'x'
        job_description = column[12]
        _, created = Donor.objects.update_or_create(
            title=title,
            name=column[1],
            first_name=column[2],
            road=column[3],
            plz=column[4],
            city=column[5],
            email_address=column[6],
            phone_number=column[7],
            info_letter_paper=letter_paper,
            info_letter_mail=letter_mail,
            is_member=is_member,
            internal_job=job_description,
        )


def import_child(io_string):
    for column in csv.reader(io_string, delimiter=',', quotechar='|'):
        _, created = Donor.objects.update_or_create(
            name=column[0],
            first_name=column[1],
            birthday=column[2],
        )


def import_data(request):
    template = 'tool/import_data.html'

    if str(request.method) == 'GET':
        return render(request, template)

    donors_or_children = False
    csv_file = ""
    try:
        csv_file = request.FILES['donors']
    except MultiValueDictKeyError:
        try:
            csv_file = request.FILES['children']
            donors_or_children = True
        except MultiValueDictKeyError:
            messages.error(request, 'error, please try again')
            return render(request, template)

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a CSV File')
        return render(request, template)

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    if not donors_or_children:
        import_donor(io_string)
    else:
        import_child(io_string)

    return redirect('../')


def create_user(request):
    if str(request.user) is 'AnonymousUser':
        return redirect('login')
    form = forms.UserCreationForm()
    if request.method == 'POST' and form.is_valid():
        print(request.POST)
        user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
        forms.UserCreationForm(request.POST).save()
    return render(request, 'tool/create.html', {'form': form})


def user_logout(request):
    if str(request.user) is 'AnonymousUser':
        return redirect('login')
    logout(request)
    return redirect('login')


def edit_user(request):
    if str(request.user) is 'AnonymousUser':
        return redirect('login')
    form = forms.UserChangeForm(request.POST)
    if request.method == 'POST':
        form.save(request)
        return redirect('index')
    return render(request, 'tool/edit.html', {'form': form})
