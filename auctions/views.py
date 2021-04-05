# ana | fjfjfjfj
# bob | wasp
# admin | adminadmin
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Max, Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import NewBid, NewComment, NewListing
from .models import Bid, Category, Comment, Listing, User


def index(request):
    return render(request, 'auctions/index.html', {
        'listings': Listing.objects.exclude(closed=True).order_by('title').all(),
    })

def categories(request):
    return render(request, 'auctions/categories.html', {
        'categories': Category.objects.all().order_by('id'),
    })

def category(request, category_id):
    return render(request, 'auctions/category.html', {
        'listings': Listing.objects.filter(category_id=category_id).exclude(closed=True).all(),
        'category': Category.objects.filter(id=category_id).first()
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
    watchers = item.watchers.all()
    if item.watchers.filter(username=request.user):
        watching = True
    else:
        watching = False

    if request.method == 'POST':

        # Watching / unwatching item
        user = request.user

        if request.POST['action'] == 'Watch':
            user.watching.add(item)
        elif request.POST['action'] == 'Unwatch':
            user.watching.remove(item)

        # Bidding
        elif request.POST['action'] == 'Bid':
            form_bid = NewBid(request.POST)

            if form_bid.is_valid():
                if form_bid.cleaned_data['bid'] <= item.current_price:
                    messages.error(request, f"Your bid needs to be higher than ${item.current_price}!")
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
                    new_bid.user = user
                    new_bid.save()

                    # To display highest bid in index page
                    item.current_price = form_bid.cleaned_data['bid']
                    item.save()
        
        # Sending comments
        elif request.POST['action'] == 'Comment':
            form_comment = NewComment(request.POST)

            if form_comment.is_valid():
                new_comment = Comment()
                new_comment.comment = form_comment.cleaned_data['comment']
                new_comment.listing = item
                new_comment.user = user
                new_comment.save()

        
        # Closing the listing
        elif request.POST['action'] == 'Close':
            item.closed = True
            item.save()
            bid.winning_bid = True
            bid.save()

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
                'watchers': watchers,
                'watching': watching,
                'bid': bid,
                'comments': comments,
                'form_bid': NewBid(),
                'form_comment': NewComment()
            })    


@login_required(login_url='/login')
def portfolio(request):
    user = request.user

    # https://stackoverflow.com/questions/17841525/django-how-to-use-group-by-and-max-to-get-complete-row-in-queryset-and-disp
    id_list = Bid.objects.filter(user=user).values('user','listing').annotate(Max('id')).values('id__max')
    bids = Bid.objects.filter(pk__in=id_list)

    return render(request, 'auctions/portfolio.html', {
        'watching': user.watching.all().order_by('title'),
        'bids': bids,
        'listings': user.listings.all().order_by('closed', 'title')
    })


def login_view(request):
    if request.method == "POST":
        # http://www.learningaboutelectronics.com/Articles/How-to-redirect-a-user-after-login-to-the-URL-in-the-next-parameter-in-Django.php
        valuenext = request.POST.get('next')
        if valuenext == '':
            valuenext = reverse('index')

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(valuenext)
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
