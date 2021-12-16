# sphere-colormap
Assigns rgb colors to points on sphere (orientations in 3D).

## Installation
Clone the repository.

## Use
The simplest example involves coloring random 3D vectors.
``` python
import scmap
import numpy as np

vectors = np.random.standard_normal(size=(1000,3))
coloring = scmap.Ico() 
colors = coloring(vectors)
```

![](https://github.com/vedranaa/colorsphere/raw/main/Figure1.png)

Sphere colormap (scmap) can be oriented by either perumuting vector coordinates, rotating vectors, or defining a z-direction. Check the examples to see how this is accomplished. 

## Different colorspheres
Scmap module includes 4 special spere colormaps. `Uno` is suitable when orientations are predominantly uindirectional, `Duo` is suitable when orientations are predominantly in a plane, `Tre` is suitable when orentations are to be interpeted as being predominantly in x, y or z direction, `Ico` is suitable when there is no predominant orientation. We also include 2 simpler colormaps: `Inc` which assigns colors based on inclination, and `Azy` which colors azymuth.

![](https://github.com/vedranaa/colorsphere/raw/main/Figure2.png)
