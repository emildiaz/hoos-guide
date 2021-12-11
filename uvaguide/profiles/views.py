from django.views.generic import ListView
from django.shortcuts import render, redirect
from .forms import EditProfileForm
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

"""
Helper function for profile view.  Checks if two profiles are friends.
"""
def are_friends(p1, p2):
    return (p1.user in p2.friends.all()) and (p2.user in p1.friends.all())

"""
Helper function for profile view.  Retrives all friend requests  that the current user
is receiving and all of their friends that they have accepted.
"""
def get_received_requests(profile):
    requests = []
    friends = []
    for request in profile.user.friends.all():
        if not are_friends(profile, request):
            requests.append(request)
        else:
            friends.append(request)
    return requests, friends

"""
Helper function for the friends view.  Retrieves all the friend requests that the current user has sent.
"""
def get_sent_requests(profile):
    requests = []
    friends = []
    for request in profile.friends.all():
        request_profile = Profile.objects.get(user=request)
        if not are_friends(profile, request_profile):
            requests.append(request_profile)
    return requests

@login_required()
def profile(request):
    user_profile = Profile.objects.get(user=request.user)
    requests, friends = get_received_requests(user_profile) 
    context = {
        'user_profile': user_profile,
        'requests': requests,
        'friends': friends,
    }
    return render(request, 'profiles/profile.html', context)

@login_required()
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    if (profile.pfp.name == "False"):
        profile.pfp = None
        profile.save()
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            if username != None and username != '':
                profile.username = username
            image = form.cleaned_data['pfp']
            if image != None:
                profile.pfp = image
            bio = form.cleaned_data['bio']
            profile.bio = bio
            profile.save()
            return redirect('profiles:profile')
    else:
        form = EditProfileForm(instance=profile)
    return render(request, 'profiles/edit_profile.html', {'form': form})

class FriendView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profiles/friends.html'
    context_object_name = 'profiles_list'

    """
    Place filtering for search bar.
    """
    def get_queryset(self):
        query = self.request.GET.get('search')
        # if the user does not input anything in the search field, return all profiles
        if query == None or query == "":
            user = User.objects.get(id=self.request.user.id)
            return Profile.objects.exclude(user=user)
        
        #allows for lenient search bar -- do not need to exact-search friends
        possible_searches = []
        for profile in Profile.objects.all():
            if query in profile.username:
                possible_searches.append(profile) 
        return possible_searches
    
    def get_context_data(self, **kwargs):
        user = self.request.user
        user_profile = Profile.objects.get(user=user)
        sent_requests = get_sent_requests(user_profile) 
        received_requests, friends = get_received_requests(user_profile)
        context = super().get_context_data(**kwargs)
        context['sent_requests'] = sent_requests
        context['received_requests'] = received_requests
        context['friends'] = friends
        return context

@login_required()
def send_request(request, friend_id):
    friend = Profile.objects.get(id=friend_id)
    user_profile = Profile.objects.get(user=request.user)
    user_profile.friends.add(friend.user)
    user_profile.save()
    return redirect('profiles:friends')

@login_required()
def accept(request, friend_id):
    friend = Profile.objects.get(id=friend_id)
    user_profile = Profile.objects.get(user=request.user)
    user_profile.friends.add(friend.user)
    user_profile.save()
    return redirect('profiles:profile')

@login_required()
def deny(request, friend_id):
    friend = Profile.objects.get(id=friend_id)
    user = User.objects.get(id=request.user.id)
    user.friends.remove(friend)
    user.save()
    return redirect('profiles:profile')

@login_required()
def view_friend(request, friend_id):
    friend=Profile.objects.get(user=User.objects.get(id=friend_id))
    requests, friends = get_received_requests(friend) 
    return render(request, 'profiles/view_friend.html', {'friend': friend, 'friends': friends})
