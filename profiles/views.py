from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import UserProfileForm

from checkout.models import Order


@login_required
def profile(request):
    """
    This is a view that will return the profile page to the user
    """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')

    form = UserProfileForm(instance=profile)
    orders = profile.orders.all()

    template = 'profiles/user-profile.html'
    context = {
        'form': form,
        'orders': orders,
        'profile_page': True,
    }

    return render(request, template, context)


def order_history(request, order_number):
    """
    This is a view that retrieves all of the users order history
    """
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f" This is a past confirmation for order number {order_number}."
        "A confirmation email was sent on the order date. "
    ))

    template = 'checkout/checkout_complete.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
