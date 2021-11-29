# colorsphere
Assigns rgb colors to orientations in 3D.

## Installation
Clone the repository.

## Use
``` python
import colorsphere
import numpy as np

vectors = np.random.standard_normal(size=(1000,3))
coloring = colorsphere.Ico() 
colors = coloring(vectors)
```
![](https://github.com/vedranaa/colorsphere/raw/main/Figure1.png)

## Different colorspheres
![](https://github.com/vedranaa/colorsphere/raw/main/Figure2.png)
