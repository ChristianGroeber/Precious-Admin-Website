import os

import django, csv, io, json, random
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError

from .forms import CreateChild, CreateDonationPlan, CreateDonor, Donate, CustomCreateUser, EditUserForm
from .models import Child, Donor, DonationPlan, Donation, Title, MyUser
from django.contrib.auth import authenticate, login, logout, forms
from django.contrib.auth.models import User, Group
from precious_hands_admin.settings import MEDIA_ROOT, STATICFILES_DIRS

from PIL import Image, ImageDraw, ImageFont


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


def create_user_profile_image(user):
    rnd = random.randint(1, 11)
    with open(STATICFILES_DIRS[0] + '/json/colors.json', 'r') as f:
        datastore = json.load(f)
    color = datastore['calendar'][str(rnd)]['background']
    text_color = datastore['calendar'][str(rnd)]['foreground']
    img = Image.new('RGB', (256, 256), color=color)
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(os.path.join(STATICFILES_DIRS[0], 'fonts', 'Product Sans Regular.ttf'), 90)
    d.text((128-30, 128-50), user.username[0].upper(), fill=text_color, font=font)
    image_path = os.path.join(MEDIA_ROOT, 'profile_images', user.username + '.jpg')
    img.save(image_path)
    return os.path.join('profile_images', user.username + '.jpg')


def index(request):
    if str(request.user) is 'AnonymousUser':
        return redirect('login')
    user_group = str(request.user.groups.all()[0])
    return render(request, 'tool/index.html', {'user_type': request.user.is_superuser, 'user_group': user_group})


def create(request, option):
    if str(request.user) is 'AnonymousUser':
        return redirect('login')
    if request.method == 'POST':
        if option == 'child':
            form = CreateChild(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('index')
        form = None
        if option == 'donor':
            form = CreateDonor(request.POST)
        elif option == 'donation_plan':
            form = CreateDonationPlan(request.POST)
        elif option == 'user' and str(request.user.groups.all()[0]) == 'Administrators':
            form = CustomCreateUser(request.POST)
            if form.is_valid():
                print(form.cleaned_data)
                a = User.objects.create_user(username=form.cleaned_data['username'],
                                             password='1234',
                                             first_name=form.cleaned_data['first_name'],
                                             last_name=form.cleaned_data['last_name'])
                a.save()
                b = MyUser(user=a, profile_picture=create_user_profile_image(a))
                b.save()
                Group.objects.get(name='Employees').user_set.add(a)
                return redirect('index')
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
        elif option == 'user' and str(request.user.groups.all()[0]) == 'Administrators':
            form = CustomCreateUser()
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
    context = {}
    if option == 'child':
        obj = get_object_or_404(Child, id=id)
        form = CreateChild(request.POST or None, request.FILES or None, instance=obj)
        context['image'] = obj.image
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
    context['option'] = option
    context['form'] = form
    return render(request, 'tool/edit.html', context)


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


def user_logout(request):
    if str(request.user) is 'AnonymousUser':
        return redirect('login')
    logout(request)
    return redirect('login')


def edit_user(request):
    if str(request.user) is 'AnonymousUser':
        return redirect('login')
    user = request.user
    form = EditUserForm(instance=user)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            print('valid')
            form.save()
        return redirect('index')
    return render(request, 'tool/edit.html', {'form': form})


def edit_password(request):
    if str(request.user) is 'AnonymousUser':
        return redirect('login')
    user = request.user
    form = PasswordChangeForm(user=user)
    if str(request.method == 'POST'):
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request, 'tool/edit.html', {'form': form})

