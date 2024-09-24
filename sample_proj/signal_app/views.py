from django.http import HttpResponse
from django.db import transaction
from .signals import custom_signal
from django.contrib.auth.models import User


def index(request):
    try:
        with transaction.atomic():
            # create a record
            record = User.objects.create(username="Srdev")
            custom_signal.send(sender=User)  # Send the signal
        return HttpResponse("DONE")
    except Exception as e:
        return HttpResponse(str(e))
