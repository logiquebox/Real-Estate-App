from django.shortcuts import get_object_or_404, render
from .models import Listing
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from listings.choices import bedroom_choices, price_choices, state_choices

def index(request):
  listings = Listing.objects.order_by('-list_date').filter(is_published=True)
  paginator = Paginator(listings, 6)
  page = request.GET.get('page')
  paged_listings = paginator.get_page(page)

  context = {
    'listings': paged_listings
  }
  return render(request, 'listings/listings.html', context)


def listing(request, listing_id):
  listing = get_object_or_404(Listing, pk=listing_id)
  context = {
    'listing': listing
  }
  return render(request, 'listings/listing.html', context)


def search(request):
  queryset_list = Listing.objects.order_by('-list_date')

  # Filter by Keywords
  if 'keywords' in request.GET:
    keywords = request.GET['keywords']
    if keywords:
      queryset_list = queryset_list.filter(description__icontains=keywords)

  # filter by city 
  if 'city' in request.GET:
    city = request.GET['city']
    if city:
      queryset_list = queryset_list.filter(city__iexact=city)
  
  # filter by state 
  if 'state' in request.GET:
    state = request.GET['state']
    if state:
      queryset_list = queryset_list.filter(state__iexact=state)

  # filter by bedroom 
  if 'bedroom' in request.GET:
    bedroom = request.GET['bedroom']
    if bedroom:
      queryset_list = queryset_list.filter(bedroom__lte=bedroom)
  
  # filter by price 
  if 'price' in request.GET:
    price = request.GET['price']
    if price:
      queryset_list = queryset_list.filter(price__lte=price)


  context = {
    'listings': queryset_list,
    'state_choices': state_choices,
    'bedroom_choices': bedroom_choices,
    'price_choices': price_choices,
    'values': request.GET
  }
  return render(request, 'listings/search.html', context)
