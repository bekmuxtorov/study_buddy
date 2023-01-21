from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse

from . import models
from .forms import RoomForms, MessageForms

# Create your views here.


def home_page_view(request):
    messages = models.Message.objects.all().order_by('-created')
    topics = models.Topic.objects.all()
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = models.Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    context = {
        'topics': topics,
        'rooms': rooms,
        'messages': messages
    }
    return render(request, 'home.html', context)


@login_required(login_url='login')
def add_room_page(request):
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
    messages = models.Message.objects.filter(room=pk).order_by('-created')
    participants = obj.participants.all()
    participant_count = participants.count()
    if request.method == 'POST':
        user = request.user
        body = request.POST.get('message')

        if user.is_authenticated:
            models.Message.objects.create(
                user=user,
                body=body,
                room_id=pk
            )
        else:
            return redirect('login')

        obj.participants.add(request.user)
        return redirect('room_detail', pk=pk)

    context = {
        'messages': messages,
        'obj': obj,
        'participants': participants,
        'participant_count': participant_count
    }

    return render(request, 'room_detail.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
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
    message = ''
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            message = 'To\'ldirishda xatolik!'

    context = {
        'form': form,
        'message': message
    }
    return render(request, 'register.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def message_delete(request, pk):
    obj = models.Message.objects.get(pk=pk)
    obj_room = obj.room.id
    if request.method == "POST":
        obj.delete()
        return redirect('room_detail', pk=obj_room)
    return render(request, 'room_delete.html', {'obj': obj})


@login_required(login_url='login')
def message_update(request, pk):
    msg = ''
    choosse_message = models.Message.objects.get(pk=pk)
    choosse_message_room = choosse_message.room.id
    if choosse_message.user == request.user:
        form = MessageForms(instance=choosse_message)
        if request.method == "POST":
            form = MessageForms(request.POST, instance=choosse_message)
            if form.is_valid():
                form.save()
            else:
                msg = 'To\'ldirishda xatolik!'

            return redirect('room_detail', pk=choosse_message_room)
        context = {
            'form': form,
            'msg': msg
        }
        return render(request, 'message_update.html', context)

    return HttpResponse("Siz bu xabarni tahrirlay olmaysz")
