from django.db import models
from authentication.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    async def __str__(self):
        sender = await sync_to_async(self.sender.__str__)()
        recipient = await sync_to_async(self.recipient.__str__)()
        return f"From {sender} to {recipient}: {self.body}"
    
# Signal receiver to delete messages older than 10 days
@receiver(post_save, sender=Message)
def delete_old_messages(sender, instance, created, **kwargs):
    if created:  # Only perform this for newly created messages
        cutoff_date = timezone.now() - timedelta(days=10)
        Message.objects.filter(timestamp__lt=cutoff_date).delete()