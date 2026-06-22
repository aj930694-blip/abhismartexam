import threading
import time
import sys
from pathlib import Path

# ensure project root is on sys.path
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from proctor import face_detection

stop_event = threading.Event()

def runner():
    try:
        face_detection.start_face_detection(stop_event=stop_event, show_window=False)
    except Exception as e:
        print('detection error:', e)

thread = threading.Thread(target=runner, daemon=True)
thread.start()
# let it run briefly
time.sleep(3)
stop_event.set()
thread.join(timeout=5)
print('test finished')
