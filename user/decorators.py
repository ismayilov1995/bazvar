from django.http import HttpResponseBadRequest
from django.shortcuts import HttpResponseRedirect, reverse

def anonymous_required(func):
    def wrap(request, *arg, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("welcome"))
        return func(request, *arg, **kwargs)
    return wrap
