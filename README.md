# ASCII Art Generator

This is just a simple python script that generates ascii art from a given image. It was written in python 3.9 and uses the OpenCV and PIL libraries to generate the image.

## How to use
Clone the repository and create a virtual environment with python 3.9.
Install the required libraries with pip install -r requirements.txt
Then run the main.py script in the terminal.

The script takes 3 arguments as input in the command line:
1) the path to the image you want to convert to ascii art
2) the string of ascii character you want to use to generate the image
3) the resolution scaling of the image (between 1 and 100 inclusive)

Example:
```
python3 main.py upload_images/image.jpg "ABCDEFGHIJKLMNOPQRSTUVWXYZ" 50
```

The script will generate the ascii art as a jpg in the generated_images/ folder and as a text file in the generated_text/ folder.

## Note
The method in which the ascii art jpg image is generated results in a very high resolution image to not obscure the characters themselves. Files will be much larger than the reference image. This is because for every 2 pixels in the image, there is one ascii character. Roughly speaking, for each pixel in the reference image, there are 42 pixels in the ascii art image.