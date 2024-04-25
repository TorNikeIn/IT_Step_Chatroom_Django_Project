from django.shortcuts import render, redirect
from .forms import RoomForm

# Create your views here.
from django.http import HttpResponse
from .models import Room


def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=int(pk))
    context = {'room': room}
    return render(request, "base/room.html", context)


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