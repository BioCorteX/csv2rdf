## Index

- [Extracting Text with Tesseract](#extracting-text-with-char_lib_30)
- [See Also](#See Also)

## Extracting Text With Tesseract
Example
```python
import cv2
import os
from r2dl_ocr.ocr import OcrTesseract
path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "files")), 'test_image.png')
img = cv2.imread(path)
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
tocr = OcrTesseract(gray_image)
text = tocr.get_text()
print(text)
```

## See Also
- [More Docs](moredocs.md)
- [Functional Diagram](R2DL_OCR_Functional_Diagram.html)
