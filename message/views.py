from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import HttpResponseBadRequest, JsonResponse
from .models import MessageNew, MessageLike
from .forms import MessageForm


# Create your views here.

def message_view(request, username):
    form = MessageForm(request.POST or None)
    on_profile_user = get_object_or_404(User, username=username)
    if on_profile_user == get_object_or_404(User, pk=14):
        return HttpResponseRedirect(reverse("welcome"))

    context = {"on_profile_user": on_profile_user, "form": form, "page": "messages",
               "is_anonymous": request.user.is_anonymous}
    return render(request, 'main-templates/message/message-base.html', context)


def add_message(request, username, form_pk, model_type):
    if not request.is_ajax():
        return HttpResponseForbidden()
    receiver = get_object_or_404(User, username=username)
    my_model = None
    form = MessageForm(request.POST or None)
    data = {"is_valid": True, "redirecturl": reverse("userprofile", kwargs={"username": username}), "html": None}
    if model_type == "user":
        my_model = get_object_or_404(User, pk=form_pk)
    elif model_type == "message":
        my_model = get_object_or_404(MessageNew, pk=form_pk)
    else:
        raise Http404
    if form.is_valid():
        message = form.cleaned_data.get("content")
        cb_is_anonym = request.POST.get("customCheck")
        if not request.user.is_anonymous and not cb_is_anonym:
            sender = request.user
        else:
            sender = get_object_or_404(User, pk=14)
        MessageNew.add_message(my_model, receiver, sender, message, model_type)
    #if model_type == "message":
    #    my_model = my_model.content_object
    return JsonResponse(data=data)


def reply_message(request):
    if not request.is_ajax():
        return HttpResponseForbidden()
    msg_pk = request.GET.get("msg_pk")
    form = MessageForm(request.POST or None)
    message = get_object_or_404(MessageNew, pk=msg_pk)
    html = render_to_string("main-templates/user/include/reply-msg-view.html",
                            context={"message": message, "form": form},
                            request=request)
    return JsonResponse(data={"html": html})

def like_message(request, msg_pk):
    message = get_object_or_404(MessageNew, pk=msg_pk)
    like_msg = MessageLike.objects.filter(user=request.user, message=message)
    data = {"is_like": False, "like_count": None}
    if like_msg.exists():
        like_msg.delete()
        data["is_like"] = False
    else:
        MessageLike.like_message(request.user, message)
        data["is_like"] = True
    data["like_count"] = message.get_liked_msg_count()


    return JsonResponse(data)

def hide_message(request, msg_pk):
    message = get_object_or_404(MessageNew, pk=msg_pk)
    is_hide = False
    if message.receiver == request.user:
        if message.is_secret:
            is_hide = False
            message.is_secret = False
        else:
            is_hide = True
            message.is_secret = True
        message.save()
    html = render_to_string("main-templates/message/include/badge-hide.html", {"msg": message})
    return JsonResponse({"html": html, "is_hide": is_hide})

def delete_message(request):
    if not request.is_ajax():
        return Http404
    msg_pk = request.GET.get("msg_pk")
    message = get_object_or_404(MessageNew, pk=msg_pk)
    receiver = request.GET.get("receiver")
    if request.user.username != receiver:
        return HttpResponseForbidden()
    message.delete()
    return JsonResponse(data={"is_valid": True})


# Errorlar ucun viewlar
#def handler404(request, exception):
#    return render(request, 'include/error/404.html', status=404)

def handler404(request, *args):
    response = render(request, "include/error/404.html")
    return response

def handler500(request, *args):
    response = render(request, "include/error/500.html")
    return response

def handler403(request, *args):
    response = render(request, "include/error/403.html")
    return response