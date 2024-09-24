### Question 1. By default are django signals executed synchronously or asynchronously? Please support your answer with a code snippet that conclusively proves your stance. The code does not need to be elegant and production ready, we just need to understand your logic.

In Django, signals are executed synchronously by default. This means that when a signal is triggered, the receiver functions associated with that signal are executed immediately, before the function or action that triggered the signal returns.

To demonstrate this, We have a default Django model called <mark>User</mark> and we want to print username whenever a new user is created or updated. We can use the <mark>post_save</mark> signal to achieve this:

```python
# sample_proj\signal_app\signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import time

@receiver(post_save,sender=User)
def user_post_save_receiver(sender,instance,created,**kwargs):
    time.sleep(2)
    if created:
        print("User is created >> ",instance.username)
    else:
        print("User is updated >> ",instance.username)
```
```bash
# Output: If new user created.
User is created >>  manager
```

In this example, the <mark>user_post_save_receiver</mark> function is executed immediately after the User instance is created. we can see that the execution flow is blocked during the 2-second delay, proving that Django signals are executed synchronously by default. The print statement "User is created." does not appear until the signal handler finishes execution, which demonstrates the synchronous nature of signals.

Note: For testing this example, You must visit admin panel and perform add or update user. http://127.0.0.1:8000/admin/auth/user/

### Question 2. Do django signals run in the same thread as the caller? Please support your answer with a code snippet that conclusively proves your stance The code does not need to be elegant and production ready, we just need to understand your logic.

No, Django signals do not run in the same thread as the caller. They are executed in a separate thread called process, ensuring that the main application thread is not blocked and continue processing other requests.

```python
# sample_proj\signal_app\signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import time
import threading

@receiver(post_save,sender=User)
def user_post_save_receiver(sender,instance,created,**kwargs):
    time.sleep(2)
    print("Signal Thread >> ",threading.current_thread().name)
    if created:
        print("User is created >> ",instance.username)
    else:
        print("User is updated >> ",instance.username)

print("Caller Thread >> ",threading.current_thread().name)
```

```bash
# Output
Caller Thread >>  MainThread
Signal Thread >>  Thread-1 (process_request_thread)
```

The output clearly demonstrates that the <mark>user_post_save_receiver</mark> function is executed in different thread. The caller thread continues to execute even while the signal handler is running, preventing blocking and ensuring responsiveness.

### Question 3. By default do django signals run in the same database transaction as the caller? Please support your answer with a code snippet that conclusively proves your stance. The code does not need to be elegant and production ready, we just need to understand your logic.

Django signals do run in the same database transaction as the caller. This means that if the caller is inside a transaction, the signal handler’s operations are also part of that transaction. If an exception happens in the signal handler, it will trigger a rollback for the entire atomic. This behavior is ensure isolation between the original operation and the signal handlers.

``` python
# sample_proj\signal_app\signals.py

# create a custom signal
custom_signal = Signal()
@receiver(custom_signal)
def signal_handler(sender, **kwargs):
    print("signal handler is called.")
    with transaction.atomic():
        # Try to create a new record within the signal handler's transaction
        new_record = User.objects.create(username="Jrdev")
        raise Exception("Simulating error in signal handler!")

```
``` python 
# sample_proj\signal_app\views.py
def index(request):
    try:
        with transaction.atomic():
            # create a record
            record = User.objects.create(username="Srdev")
            custom_signal.send(sender=User)  # Send the signal
        return HttpResponse("DONE")
    except Exception as e:
        return HttpResponse(str(e))
```
``` Bash
# Output: 
Exception: Simulating error in signal handler!
```
In this example, A signal handler <mark>signal_handler</mark> is attempts to create a new record within its own transaction. A record is created within the transaction, and the signal is sent. 

When we call <mark>index</mark> view, The signal handler is executed, but the new record creation fails due to the simulated error. We create a new User inside an atomic() block, which ensures that the entire process is inside the same database transaction.
If an exception is raised inside the signal, the transaction should be rolled back, and no new user should be saved in the database.

This shows that, by default, Django signals execute within the same database transaction as the caller.