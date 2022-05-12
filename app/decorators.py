from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

def student_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url = 'login'):

    actual_decorator = user_passes_test(
        lambda u: u.is_active and hasattr(u, 'student'),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def faculty_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url = 'login'):

    actual_decorator = user_passes_test(
        lambda u: u.is_active and hasattr(u, 'professor'),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def auditor_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url = 'login'):

    actual_decorator = user_passes_test(
        lambda u: u.is_active and hasattr(u, 'auditor'),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def coordinator_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url = 'login'):

    actual_decorator = user_passes_test(
        lambda u: u.is_active and hasattr(u, 'coordinator'),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator