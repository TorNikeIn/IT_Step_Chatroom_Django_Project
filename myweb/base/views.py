from django.shortcuts import render, redirect
from .forms import RoomForm
# Create your views here.
from django.http import HttpResponse
from .models import Room, Topic
from django.db.models import Q

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms': rooms, "topics": topics, "room_count": room_count}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=int(pk))
    context = {'room': room}
    return render(request, "base/room.html", context)


@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        # print(request.POST)
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')



    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("<h1>You do not have permission!</h1>")

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')



    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("<h1>You do not have permission!</h1>")

    if request.method == "POST":
        room.delete()
        return redirect('home')

    return render(request, "base/delete.html", {'obj': room})


def login_page(request):
    page = "login"
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist!")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Password is not valid...")

    context = {"page": page}
    return render(request, "base/login_register.html", context)

def logout_user(request):
    logout(request)
    return redirect('home')

def register_page(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occurred during registration!")
    return render(request, "base/login_register.html", {"form": form})