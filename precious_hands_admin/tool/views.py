from django.shortcuts import render, redirect
from django.template import loader
from .forms import CreateChild, CreateDonationPlan, CreateDonor

# Create your views here.


def index(request):
    return render(request, 'tool/index.html')


def create(request, option):
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
        form = CreateChild()
        if option is 'donor':
            form = CreateDonor()
        elif option is 'donation_plan':
            form = CreateDonationPlan()
        return render(request, 'tool/create.html', {'form': form})
