from django.contrib.auth.decorators import login_required
from django.http import request
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.list import ListView
from .models import Place
from profiles.models import Profile
from .forms import ReviewForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class PlaceView(LoginRequiredMixin, ListView):
    model = Place
    template_name = 'maps/places.html'
    context_object_name = 'places_list'

    """
    Place filtering for search bar.
    """
    def get_queryset(self):
        query = self.request.GET.get('search')
        filter_search = dict(self.request.GET.items())
        if query == None or query == "":
            if 'Most Popular' in filter_search:
                return Place.objects.order_by('-num_likes')
            else:
                return Place.objects.order_by('name')
        return Place.objects.filter(name__icontains=query)


"""
The general view for each place location; this includes general
information like name, address, and description.
"""
@login_required()
def detail(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    user = Profile.objects.get(user=request.user)
    reviews = place.reviews.all()

    #check for new reviews
    review = None
    #if a comment was posted
    if request.method == 'POST':
        rf = ReviewForm(data=request.POST)
        if rf.is_valid():
            review = rf.save(commit=False) #don't save yet, need to give its place field
            review.place = place
            review.author = user
            review.save()
            rf=ReviewForm() #delete the input fields after you save the comment
    else:
        rf = ReviewForm()
    name = place.name
    name = name.replace("'", "").replace('&', 'and')
    context = {
        'name' : name,
        'place' : place,
        'reviews' : reviews,
        'review' : review, 
        'rf' : rf,
    }
    return render(request, 'maps/detail.html', context)

@login_required()
def like(request, place_id):
    profile = Profile.objects.get(user=request.user)
    place = get_object_or_404(Place, pk=place_id)
    if profile not in place.likes.all():
        place.likes.add(profile)
        place.num_likes += 1
        place.save()
    return redirect('maps:detail', place_id)
