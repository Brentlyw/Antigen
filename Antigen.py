import sys
import numpy as np
from PIL import Image, ImageChops
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter, label, sum as ndi_sum
from matplotlib.widgets import Slider

def getELA(img, qual=90, amp=40):
    tmp = "tmp.jpg"
    img.save(tmp, "JPEG", quality=qual)
    compressed = Image.open(tmp)
    ela = ImageChops.difference(img, compressed)
    arr = np.array(ela)
    gray = np.dot(arr[...,:3], [0.299, 0.587, 0.114])
    amped = np.clip(gray * amp, 0, 255).astype(np.uint8)
    return amped

def makeHeatmap(arr, sig=10, intens=0.72, thresh=175, minsize=5):
    masked = arr > thresh
    labeled, num = label(masked)
    sizes = ndi_sum(masked, labeled, range(1, num + 1))
    keep = sizes >= minsize
    keep = keep[labeled - 1]
    hmap = np.where(keep, arr, 0)
    logscaled = np.log1p(hmap.astype(float))
    norm = (logscaled - logscaled.min()) / (logscaled.max() - logscaled.min() + 1e-8)
    blurred = gaussian_filter(norm, sigma=sig) * intens
    return np.clip(blurred, 0, 1)

def refresh(val):
    amp = ampSlider.val
    intens = intensSlider.val
    thresh = threshSlider.val
    ela = getELA(src, qual=90, amp=amp)
    hmap = makeHeatmap(ela, intens=intens, thresh=thresh)
    elaImg.set_data(ela)
    hmapImg.set_data(hmap)
    fig.canvas.draw_idle()

def run(path):
    global src, fig, elaImg, hmapImg, ampSlider, intensSlider, threshSlider
    src = Image.open(path)
    ela = getELA(src, amp=40)
    hmap = makeHeatmap(ela, intens=0.72, thresh=175)
    fig, ax = plt.subplots(1, 3, figsize=(20, 10))
    plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.2, wspace=0.05)
    ax[0].imshow(src)
    ax[0].set_title('Original')
    ax[0].axis('off')
    elaImg = ax[1].imshow(ela, cmap='gray')
    ax[1].set_title('ELA')
    ax[1].axis('off')
    dark = np.array(src) * 0.5
    ax[2].imshow(dark.astype(np.uint8))
    hmapImg = ax[2].imshow(hmap, alpha=0.7, cmap='hot')
    ax[2].set_title('Heatmap')
    ax[2].axis('off')
    w, h = 0.2, 0.03
    b = 0.05
    ampAx = plt.axes([0.1, b, w, h])
    ampSlider = Slider(ampAx, 'ELA Amp', 1, 100, valinit=40)
    intensAx = plt.axes([0.4, b, w, h])
    intensSlider = Slider(intensAx, 'Heatmap Intensity', 0.1, 2.0, valinit=0.72)
    threshAx = plt.axes([0.7, b, w, h])
    threshSlider = Slider(threshAx, 'Heatmap Threshold', 0, 255, valinit=175, valfmt='%0.0f')
    ampSlider.on_changed(refresh)
    intensSlider.on_changed(refresh)
    threshSlider.on_changed(refresh)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <image_path>")
        sys.exit(1)
    imgPath = sys.argv[1]
    run(imgPath)
