def _try_use_pil_load_from_binary(data):
    import cv2
    import sys
    import numpy as np
    from PIL import Image
    from io import BytesIO
    try:
        with BytesIO() as f:
            pilimg = Image.open(BytesIO(data))
            pilimg.save(f, 'png')
            imgdata = f.getvalue()
            imgdata = np.frombuffer(imgdata, dtype='uint8')
            image = cv2.imdecode(imgdata, 1)
            return image
    except:
        sys.stderr.write('pil_load failed!\n')
    return None


def load_bgr_from_binary(data):
    """bytes to bgr image ndarray."""
    import sys
    import cv2
    import traceback
    from io import BytesIO
    if data is None or len(data) < 100:
        sys.stderr.write('data is None or len(data) < 100.\n')
        return None
    image = None
    try:
        imgdata = np.frombuffer(data, dtype='uint8')
        image = cv2.imdecode(imgdata, 1)
    except:
        sys.stderr.write('cv2_load_from_binary. unknown exception.\n')
        
        traceback.print_exc()
    if image is None:
        if data[0: 4].decode('utf-8') == 'RIFF' or data[0: 3].decode('utf-8') == "GIF":
            image = _try_use_pil_load_from_binary(data)
        else:
            image = None
    return image
