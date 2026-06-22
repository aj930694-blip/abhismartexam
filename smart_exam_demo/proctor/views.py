from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth import authenticate, get_user_model, login
import threading

from proctor import face_detection


def login_view(request):
    error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['student'] = username
                return redirect('dashboard')
            error = 'Invalid username or password.'
        else:
            error = 'Please enter both username and password.'

    return render(request, 'login.html', {'error': error})


def dashboard(request):

    student = request.session.get('student')

    if not student:
        return redirect('login')

    return render(
        request,
        'dashboard.html',
        {'student': student}
    )


def exam(request):

    student = request.session.get('student')

    if not student:
        return redirect('login')

    return render(request, 'exam.html')


# Background detection thread handle and stop event
_detection_thread = None
_detection_stop_event = None


def start_detection(request):
    """Start face detection in a background thread. Restricted to staff users."""
    global _detection_thread, _detection_stop_event

    user = getattr(request, 'user', None)
    if not (user and user.is_authenticated and user.is_staff):
        return HttpResponseForbidden('Forbidden')

    if _detection_thread and _detection_thread.is_alive():
        return JsonResponse({'status': 'already_running'})

    _detection_stop_event = threading.Event()

    def _target():
        try:
            face_detection.start_face_detection(stop_event=_detection_stop_event)
        except Exception:
            # swallow exceptions to avoid crashing the thread
            pass

    _detection_thread = threading.Thread(target=_target, daemon=True)
    _detection_thread.start()

    return JsonResponse({'status': 'started'})

if __name__ == '__main__':
    print('proctor.views is not intended to be run directly. Start the Django server with manage.py instead.')
if __name__ == '__main__':
    print('proctor.views is not intended to be run directly. Start the Django server with manage.py instead.')

def stop_detection(request):
    """Stop the running face detection thread. Restricted to staff users."""
    global _detection_thread, _detection_stop_event

    user = getattr(request, 'user', None)
    if not (user and user.is_authenticated and user.is_staff):
        return HttpResponseForbidden('Forbidden')

    if not (_detection_thread and _detection_thread.is_alive()):
        return JsonResponse({'status': 'not_running'})

    if _detection_stop_event:
        _detection_stop_event.set()

    # wait briefly for thread to exit
    _detection_thread.join(timeout=5)

    if _detection_thread.is_alive():
        return JsonResponse({'status': 'stopping'})

    return JsonResponse({'status': 'stopped'})