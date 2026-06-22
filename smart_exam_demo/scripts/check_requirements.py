packages = ['django','cv2']
missing = []
for p in packages:
    try:
        if p == 'cv2':
            import cv2  # type: ignore
        else:
            __import__(p)
        print(p + ' OK')
    except Exception as e:
        print(p + ' MISSING: ' + str(e))
        missing.append(p)
if missing:
    print('\nMissing packages:', ', '.join(missing))
    print('Install with: pip install -r requirements.txt')
else:
    print('\nAll required packages installed')
