# ana | fjfjfjfj
# bob | wasp
# admin | adminadmin
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import NewBid, NewComment, NewListing
from .models import Bid, Category, Comment, Listing, User


def index(request):
    return render(request, 'auctions/index.html', {
        'listings': Listing.objects.exclude(closed=True).all(),
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
            new_listing.category = form.cleaned_data['category']
            new_listing.start_bid = form.cleaned_data['start_bid']
            new_listing.image_url = form.cleaned_data['image_url']
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
    comments = Comment.objects.filter(listing=item_id)

    if request.method == 'POST':
        # For bids sent
        if request.POST['action'] == 'Bid':
            form_bid = NewBid(request.POST)

            if form_bid.is_valid():
                if form_bid.cleaned_data['bid'] <= item.current_price:
                    messages.error(request, f"Your bid needs to be at least {item.current_price} high.")
                    return render(request, 'auctions/item.html', {
                        'item': item,
                        'bid': bid,
                        'form_bid': form_bid,
                        'comments': comments,
                        'form_comment': NewComment(),
                })
                else:
                    new_bid = Bid()
                    new_bid.bid = form_bid.cleaned_data['bid']
                    new_bid.listing = item
                    new_bid.user = request.user
                    new_bid.save()

                    # To display highest bid in index page
                    item.current_price = form_bid.cleaned_data['bid']
                    item.save()
        
        # For comments sent
        elif request.POST['action'] == 'Comment':
            form_comment = NewComment(request.POST)

            if form_comment.is_valid():
                new_comment = Comment()
                new_comment.comment = form_comment.cleaned_data['comment']
                new_comment.listing = item
                new_comment.user = request.user
                new_comment.save()

        # For closed listing
        elif request.POST['action'] == 'Close':
            item.closed = True
            item.save()

        return HttpResponseRedirect(reverse('item', args=(item_id, )))

    else:
        if item.closed:
            return render(request, 'auctions/item_closed.html', {
            'item': item,
            'bid': bid,
            'comments': comments,
            })    

        else:
            return render(request, 'auctions/item.html', {
                'item': item,
                'bid': bid,
                'comments': comments,
                'form_bid': NewBid(),
                'form_comment': NewComment()
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