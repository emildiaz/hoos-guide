from django.shortcuts import render
from profiles.models import Profile
from django.contrib.auth.decorators import login_required

def home(request):
    #increases coupling but had to do it :/
    user_profile = None
    if request.user.is_authenticated:
        user = request.user
        #make profile for user if not already made
        if not Profile.objects.filter(user=user).exists():
            user_profile = Profile(user=user)
            user_profile.username = user.username
            user_profile.save()
        else:
            user_profile = Profile.objects.get(user=user)
    return render(request, 'uvaguide/home.html', {'user_profile': user_profile})

@login_required()
def map(request, location):
    location = "https://www.google.com/maps/embed/v1/place?key=AIzaSyCdaz10ER7OvsL15_iMY2hozh7-KEsukb4&q=" + location + ",Charlottesville+VA"
    return render(request, 'uvaguide/map.html', { "location": location})

@login_required()
def mapDirections(request, start, end):
    location = "https://www.google.com/maps/embed/v1/directions?origin=" + start + ",Charlottesville+VA&destination=" + end + ",Charlottesville+VA&mode=walking&key=AIzaSyCdaz10ER7OvsL15_iMY2hozh7-KEsukb4"
    end = end.replace('+', '_')
    end = end.replace('and', '&')
    start = start.replace('+', '_')
    start = start.replace('and', '&')
    return render(request, 'uvaguide/mapDirections.html', {"location": location, "start": start, "end": end})