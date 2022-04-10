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

Copy your SVG line art file (e.g. `yourfilename.svg`) into the `./input` folder, then run:

```
python draw.py -i input/yourfilename.svg
```

### Render to a file

Copy your SVG line art file (e.g. `yourfilename.svg`) into the `./input` folder, then run:

```
python draw.py -i input/yourfilename.svg --render --render-type mp4
```

Your mp4/gif will be available in the `./output` folder (e.g. as `yourfilename.mp4`).

## How does it work?

The input SVG file is traced from start to end, and its coordinates are mapped to complex numbers (x->real, y->imaginary).

The path is treated as a repeating complex signal with period of 2 Pi, and the Fourier series complex coefficients (c_0, c_1... c_n) are generated.

The complex coefficients are substituted back into the Fourier series and the resulting function is plotted across time.

For more, read the full explainer: [The Fourier Series](https://syraxius.com/2021/11/27/the-fourier-series/)
