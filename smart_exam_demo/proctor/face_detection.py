import time
try:
    import cv2
except Exception:
    cv2 = None
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def _setup_logger():
    logger = logging.getLogger('proctor.face_detection')
    if logger.handlers:
        return logger

    log_dir = Path.cwd() / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    fh = RotatingFileHandler(log_dir / 'detection.log', maxBytes=5 * 1024 * 1024, backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.setLevel(logging.INFO)
    return logger


def start_face_detection(camera_index=0, stop_event=None, show_window=False):
    logger = _setup_logger()
    logger.info('Face detection starting (camera_index=%s)', camera_index)
    if cv2 is None:
        logger.error('OpenCV (cv2) is not installed; cannot run face detection')
        return

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        'haarcascade_frontalface_default.xml'
    )

    camera = cv2.VideoCapture(camera_index)
    if not camera.isOpened():
        logger.error('Unable to open camera (index=%s).', camera_index)
        return

    try:
        last_log = 0
        frame_count = 0
        while True:
            # allow external stop
            if stop_event is not None and stop_event.is_set():
                logger.info('Stop event received, exiting detection loop')
                break

            success, frame = camera.read()
            if not success or frame is None:
                logger.warning('Camera read failed or returned empty frame')
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # show frame in window (only if requested)
            if show_window:
                try:
                    cv2.imshow('Smart Exam Proctor', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        logger.info('q pressed, exiting detection loop')
                        break
                except Exception:
                    logger.exception('cv2.imshow failed; continuing in headless mode')

            # throttle logs: log every 1 second
            frame_count += 1
            now = time.time()
            if now - last_log >= 1.0:
                logger.info('Frame %d: detected %d faces', frame_count, len(faces))
                last_log = now

            # small sleep to yield
            time.sleep(0.01)
    finally:
        camera.release()
        cv2.destroyAllWindows()
        logger.info('Face detection stopped')


if __name__ == '__main__':
    # when run directly, show the GUI window
    start_face_detection(show_window=True)