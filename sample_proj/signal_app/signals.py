from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import time
import threading
from django.db import transaction
from django.dispatch import Signal


@receiver(post_save, sender=User)
def user_post_save_receiver(sender, instance, created, **kwargs):
    time.sleep(2)  # sleep thread for 2 seconds
    print("Signal Thread >> ", threading.current_thread().name)
    if created:
        print("User is created >> ", instance.username)
    else:
        print("User is updated >> ", instance.username)


print("Caller Thread >> ", threading.current_thread().name)


custom_signal = Signal()


@receiver(custom_signal)
def signal_handler(sender, **kwargs):
    print("signal handler is called.")
    with transaction.atomic():
        # Try to create a new record within the signal handler's transaction
        new_record = User.objects.create(username="Jrdev")
        raise Exception("Simulating error in signal handler!")
