from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

"""
Core Application Decorators - Suroga API

This module defines custom decorator functions used within the Core application of the Suroga API project. 
Decorators are a powerful and reusable way to modify or enhance the behavior of functions or methods in Python, 
and in a Django context, they are typically used to enforce certain permissions or conditions on view functions.

Included Decorators:
- api_client_required: Ensures that a view can only be accessed by users with active client status. If a user 
  is not active, they are redirected to the login page.

These decorators allow for separation of concerns by handling checks and redirections away from the view logic itself, 
making code more modular, easier to read, and maintain.

By employing these decorators, we ensure consistent access control throughout the application and prevent unauthorized 
access to certain views that should only be available to specific user types or roles.

Maintainer: Carlos Leandro
Last updated: 15/3/2014

Example usage:
from core.decorators import api_client_required

@api_client_required
def my_view(request):
    # View logic here
"""


# The `api_client_required` is a custom decorator built on top of Django's built-in `user_passes_test` decorator.
# It is designed to verify whether the current user meets certain conditions – specifically, it checks if the
# user is active, which is a common criterion for allowing further access to certain API views or actions.


def api_client_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    """
    Verify that the currently logged-in user is active.

    The decorator will check the user's `is_active` attribute, typically expecting it to be True. If the user is not
    active, this test will fail and the user will be redirected to the login URL provided, which can be specified if
    necessary.

    Parameters:
        function: The view function that is decorated.
        redirect_field_name: The name of a GET field to put in the URL when redirected (defaults to 'next').
        login_url: The URL of the login page, which defaults to 'login'.

    Returns:
        The actual view function if the check passes, otherwise, it redirects the user to the `login_url`.
        
    This decorator can be used on views that require the user to be a logged-in client with an active account. 
    Use it by adding `@api_client_required` above the view function that you want to protect.
    """
    # Builds the `actual_decorator` using the `user_passes_test` function from Django's authentication framework.
    actual_decorator = user_passes_test(
        lambda u: u.is_active, # The test function that checks if the user is active.
        login_url=login_url,    # If the test fails, the user is redirected to this login URL.
        redirect_field_name=redirect_field_name # The GET parameter name for the redirect field.
    )

    # If the decorator is applied to a function, it modifies the function to incorporate the test; otherwise,
    # it simply returns the decorator itself.
    if function:
        return actual_decorator(function)
    return actual_decorator