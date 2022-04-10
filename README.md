# SVG Fourier Series
Computes the Fourier series coefficients for an input SVG line art and renders it into a video or gif

https://user-images.githubusercontent.com/8336849/162612251-e2d923a2-07b4-4035-947c-afa94b5aadbc.mp4

# Installation (for Windows):

- Clone this repository (or download this repository and extract it somewhere).
- Install Python 3.9 from https://www.python.org/.
- Create a Python 3.9 virtual environment in this folder using `python3 -m venv venv`.
- Activate your virtual environment using `cd venv/Scripts && activate`.
- Install requirements listed in requirements.txt using `pip install -r requirements.txt`.
- (Personally, I just use PyCharm IDE for all these).

## Usage

### Preview

Copy your yourfilename.svg svg line art file into the ./input folder, then run:

```
python draw.py -i input/yourfilename.svg
```

### Render to a file

Copy your yourfilename.svg svg line art file into the ./input folder, then run:

```
python draw.py -i input/yourfilename.svg -r
```
