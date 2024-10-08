# Antigen
An image forensics utility to detect and visualize digital modifications using ELA, inspired by FotoForensics.

# Features
- Displays Original, ELA Highlighted image, and ELA heatmap.
- Includes adjustable sliders for ELA amplification, heatmap intensity, and threshold.
- Has a minimum blob creation threshold of 5 connected pixels > the heatmap threshold. (Counteracts ELA flagging on edges that have strong luminance disparity)
- Effecient and quick, even with large/high res images.

# How To Use?
- 1.) Load an image with Antigen by calling Antigen.py {filepath} or by dragging the image onto the python script.
- 2.) Look at results, *fine tuning with sliders may be required.*
-   2a.) Areas highlighted in lighter colored pixels compared to the surroundings are more than likely modified.
-   2b.) Areas highlighted in the heatmap show very high probability areas of modification.


