# ana | fjfjfjfj
# bob | wasp
# admin | adminadmin

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import NewListing, NewBid
from .models import User, Listing, Bid, Comment


def index(request):
    return render(request, 'auctions/index.html', {
        'listings': Listing.objects.all()
    })

@login_required(login_url='/login')
def add(request):
    if request.method == 'POST':
        form = NewListing(request.POST)

        if form.is_valid():
            new_listing = Listing()
            new_listing.user = request.user
            new_listing.title = form.cleaned_data['title']
            new_listing.description = form.cleaned_data['description']
            new_listing.start_bid = form.cleaned_data['start_bid']
            new_listing.save()

            return HttpResponseRedirect(reverse('index'))
            
    else:
        return render(request, 'auctions/add.html', {
            'form': NewListing(),
        })

@login_required(login_url='/login')
def item(request, item_id):
    item = Listing.objects.get(pk=item_id)
    bid = Bid.objects.filter(listing=item_id).order_by('-bid').first()
    if bid == None:
        max_bid = item.start_bid
    else:
        max_bid = bid.bid

    if request.method == 'POST':
        form = NewBid(request.POST)

        if form.is_valid():
            if form.cleaned_data['bid'] <= max_bid:
                return render(request, 'auctions/item.html', {
                    'item': item,
                    'bid': bid,
                    'max_bid': max_bid,
                    'form': form,
                    'message': f"Your bid needs to be at least {max_bid} high."
            })
            else:
                new_bid = Bid()
                new_bid.bid = form.cleaned_data['bid']
                new_bid.listing = item
                new_bid.user = request.user
                new_bid.save()

            return HttpResponseRedirect(reverse('item', args=(item_id,)))

    else:
        return render(request, 'auctions/item.html', {
            'item': item,
            'bid': bid,
            'max_bid': max_bid,
            'form': NewBid(),
        })     

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
