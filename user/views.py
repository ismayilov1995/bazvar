from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, Http404, HttpResponseRedirect, reverse, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import HttpResponseBadRequest, JsonResponse
from .forms import LoginForm, RegisterForm, UpdateForm
from .decorators import anonymous_required
from message.models import MessageNew, MessageLike


# Create your views here.

def welcome(request):
    # butun istifadecileri cagiririq anonimden bashqa

    username_list = User.objects.values_list("username", flat=True).exclude(pk=14)
    context = {"page": "welcome", "username_list": username_list}
    return render(request, 'main_page.html', context)


@anonymous_required
def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get("password")
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        messages.success(request, "Aramıza xoş gəldin", extra_tags="success")
        return HttpResponseRedirect(reverse("welcome"))
    context = {"page": "register", "form": form, "value": "Hesab ac"}
    return render(request, 'main_page.html', context)


@anonymous_required
def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse("userprofile", kwargs={'username': request.user.username}))
    context = {'page': 'login', 'form': form, "value": "Daxil ol"}
    return render(request, 'main_page.html', context)


def userprofile(request, username):
    on_profile_user = get_object_or_404(User, username=username)
    if on_profile_user == get_object_or_404(User, pk=14):
        return HttpResponseRedirect(reverse("welcome"))
    if on_profile_user:
        # Burda sadece profile gelen mesajlari gosterdik
        content_type = ContentType.objects.get_for_model(on_profile_user.__class__)
        all_message = MessageNew.objects.filter(content_type=content_type, object_id=on_profile_user.pk)
        # Istifadecinin suallarina gelen likelar
        user_likes = MessageLike.objects.filter(message__sender=on_profile_user).count()
        context = {"on_profile_user": on_profile_user, "page": "messages", "message": all_message,
                   "user_like": user_likes}
        return render(request, 'main-templates/user/include/messages.html', context)
    return HttpResponseRedirect(reverse("welcome"))


def settings_view(request, username):
    on_profile_user = get_object_or_404(User, username=username)
    sex = request.user.userprofile.sex
    bio = request.user.userprofile.bio
    profile_photo = request.user.userprofile.profile_photo
    initial = {"sex": sex, "bio": bio, "profile_photo": profile_photo}
    form = UpdateForm(request.POST or None, request.FILES or None, instance=request.user, initial=initial)
    if request.POST:
        if form.is_valid():
            user = form.save(commit=True)
            user.userprofile.sex = form.cleaned_data.get("sex", None)
            user.userprofile.bio = form.cleaned_data.get("bio", None)
            user.userprofile.profile_photo = form.cleaned_data.get("profile_photo", None)
            user.userprofile.save()
            return HttpResponseRedirect(reverse("welcome"))

    if on_profile_user:
        context = {"on_profile_user": on_profile_user, "page": "settings", "form": form}
        return render(request, 'main-templates/user/include/user-settings.html', context)

def change_password(request):
    if request.POST:
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) #Sebeti avtomatik login olsun deye
            messages.success(request, "Şifrə uğurla dəyişdi", extra_tags="info")
            return redirect("userprofile")
        else:
            messages.warning(request, "Məlumatları düzgün daxil edin", extra_tags="warning")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "main-templates/user/password.html",{"form": form})

def search_view(request):
    search = request.GET.get("search")
    users = User.objects.all()
    result = users.filter(
        Q(username__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(
            reciver_n__content__icontains=search) | Q(sender_n__content__icontains=search)).distinct().exclude(pk=14)
    return render(request, "main-templates/user/search-result.html", {"result": result, "search": search})


@login_required()
def logout_view(request):
    logout(request)
    messages.info(request, "Təkrar gözləyirik", extra_tags="info")
    return HttpResponseRedirect(reverse("login"))
