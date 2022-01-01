from django.contrib import messages
from django.shortcuts import redirect, render
from django.core.mail import send_mail

from contacts.models import Contact

def contact(request):
  if request.method == "POST":
    listing_id = request.POST['listing_id']
    listing = request.POST['listing']
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    message = request.POST['message']
    user_id = request.POST['user_id']
    realtor_email = request.POST['realtor_email']

    # check if user has already made inquiry 
    if request.user.is_authenticated:
      user_id = request.POST['user_id']
      has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
      if has_contacted:
        messages.error(request, 'You have already made enquiry to this property')
        return redirect('/listings/'+listing_id)


    contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id)

    contact.save()

    # send_mail(
    # 'Property Inquiry',
    # 'An inquiry has made on'+ listing + 'login to admin panel for more info',
    # 'ujahemmanuel72@gmail.com',
    # [realtor_email, 'logiquebox@gmail.com'],
    # fail_silently=False,
    # )

    messages.success(request, 'Your inquiry has been submitted successfully, a realtor will reach out to you shortly')

  return redirect('/listings/'+listing_id)