# AutoHandwriter
Automate handwriting on paper with this python script

## Features:
  - Randomized handwriting generation
  - Paper detection
  - Perspective warping
  - Post processing

## Demo:
![](https://i.ibb.co/Vt5CXk4/demo.jpg)
1. Converting to gray scale
2. Removing noise
3. Edge detection
4. Fixing gaps
5. Largerst rectangle contour detection
6. Text generation
7. Warped perspective
8. Combined images
9. Post processing
10. Final result

## Usage:
Clone the repo
```sh
git clone https://github.com/Azarattum/AutoHandwriter.git
cd AutoHandwriter
```

Install the dependencies with [pip](https://pypi.org/)
```sh
pip install -r requirements.txt
```

Put your images into *./data/images/*

Create a directory for program output: *./out*

Run the script.
```sh
python . <pdf>/validate
```

- &lt;pdf&gt; - Path to the source pdf for text extraction
- validate - Validates the dataset for correct object detection
  
## Third-party libraries:
* [opencv-python](https://pypi.org/project/opencv-python/) - Unofficial pre-built CPU-only OpenCV packages for Python.
* [numpy](https://pypi.org/project/numpy/) - Fundamental package for array computing with Python.
* [pdfminer](https://pypi.org/project/pdfminer/) - PDF parser and analyzer.