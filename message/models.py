from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.

class MessageNew(models.Model):
    receiver = models.ForeignKey(User, null=True, related_name="reciver_n", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, null=True, related_name="sender_n", on_delete=models.CASCADE)
    content = models.TextField(max_length=500, verbose_name="Mesaj")
    message_date = models.DateTimeField(auto_now_add=True, null=True)
    is_secret = models.BooleanField(default=False)

    has_child = models.BooleanField(default=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name_plural = "Mesajlar New"
        ordering = ["-id"]

    def __str__(self):
        return "From:%s, To:%s | CT:%s" % (self.sender, self.receiver, self.content_type.model)

    def get_message_details(self):
        if self.receiver.first_name:
            return "%s" % (self.receiver.get_full_name())
        return self.receiver.username

    @classmethod
    def add_message(cls, model, receiver, sender, content, model_type):
        content_type = ContentType.objects.get_for_model(model.__class__)
        cls.objects.create(receiver=receiver, sender=sender, content=content, content_type=content_type, object_id=model.pk)
        if model_type == "message":
            model.has_child = True
            model.save()

    def get_reply_messages(self):
        if self.has_child:
            content_type = ContentType.objects.get_for_model(self.__class__)
            all_reply_messages = MessageNew.objects.filter(content_type=content_type, object_id=self.pk).order_by("pk")
            return all_reply_messages
        return None

    def get_liked_msg_count(self):
        return self.message_like.values_list("user__username").count()

class MessageLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_like")
    message = models.ForeignKey(MessageNew, on_delete=models.CASCADE, related_name="message_like")

    class Meta:
        verbose_name_plural="Beyenilen Mesajlar"

    def __str__(self):
        return"%s liked %s" % (self.user, self.message)

    @classmethod
    def like_message(cls, user, message):
        cls.objects.create(user=user, message=message)

