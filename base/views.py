from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from . import models
from .forms import RoomForms

# Create your views here.


def home_page_view(request):
    topics = models.Topic.objects.all()
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = models.Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    context = {
        'topics': topics,
        'rooms': rooms
    }
    return render(request, 'home.html', context)


def add_home_page(request):
    form = RoomForms()
    if request.method == 'POST':
        form = RoomForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            messages.error(request, "To'ldirishda xatolik mavjud!")

    context = {
        'form': form
    }
    return render(request, 'add_room.html', context)


def room_detail_view(request, pk):
    obj = models.Room.objects.get(pk=pk)
    return render(request, 'room_detail.html', {'obj': obj})


def room_update(request, pk):
    room = models.Room.objects.get(pk=pk)
    form = RoomForms(instance=room)
    if request.method == 'POST':
        form = RoomForms(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            messages.error(request, 'To\'ldirishga xatolik!')
    return render(request, 'room_update.html', {'form': form})


def room_delete(request, pk):
    room = models.Room.objects.get(pk=pk)
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request, 'room_delete.html')


def login_view(request):
    message = ''
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Login yoki parolda xatolik mavjud!')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            message = 'Login yoki parolda xatolik mavjud!'

    return render(request, 'login.html', {'message': message})


def register_view(request):
    return render(request, 'register.html')


def logout_view(request):
    logout(request)
    return redirect('home')
