from django.urls import path
from .views import *

urlpatterns = [
    path('<str:username>', message_view, name='message-view'),
    path('<str:username>/add-message/<int:form_pk>/<str:model_type>/', add_message, name='add-message-view'),
    path('remove-message/', delete_message, name='remove-message-view'),
    path('reply-message/', reply_message, name='reply-message'),
    path('remove/', delete_message, name='remove-message'),
    path('like/<str:msg_pk>', like_message, name='like-message'),
    path('hide/<str:msg_pk>', hide_message, name='hide-message'),
]