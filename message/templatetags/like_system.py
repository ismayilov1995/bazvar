from django import template
from django.shortcuts import get_object_or_404
from ..models import MessageNew, MessageLike

register = template.Library()


@register.filter
def is_liked(msg_pk, user):
    message = get_object_or_404(MessageNew, pk=msg_pk)
    return MessageLike.objects.filter(user=user, message=message).exists()
