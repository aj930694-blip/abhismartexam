import os
import django
import time
import sys
from pathlib import Path
from django.test import RequestFactory

# ensure project root on sys.path so settings module can be imported
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_exam_demo.settings')
django.setup()

from django.contrib.auth import get_user_model
from proctor import views

User = get_user_model()

# Ensure a staff user exists
username = 'autotest_staff'
user, created = User.objects.get_or_create(username=username)
# set password from env or default; set only if user was just created or has no usable password
autotest_password = os.environ.get('AUTOTEST_PASSWORD', 'test')
if created or not user.has_usable_password():
    user.set_password(autotest_password)
user.is_staff = True
user.is_active = True
user.save()

factory = RequestFactory()

# Call start_detection
req = factory.get('/start_detection/')
req.user = user
resp = views.start_detection(req)
print('start_detection response:', resp.content)

# wait a bit to let background thread run
time.sleep(2)

# Call stop_detection
req2 = factory.get('/stop_detection/')
req2.user = user
resp2 = views.stop_detection(req2)
print('stop_detection response:', resp2.content)
