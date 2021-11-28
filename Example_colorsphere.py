import colorsphere
from icosphere import icosphere
import numpy as np

import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d 
 

nu = 15
vertices, faces = icosphere(nu)
face_vectors = vertices[faces].sum(axis=1)
face_vectors /= np.sqrt((face_vectors**2).sum(axis=1, keepdims=True))


fig = plt.figure()


colorings = [colorsphere.Uno(), 
             colorsphere.Duo(),
             colorsphere.Tre(),
             colorsphere.Ico()]

for i in range(4):
    
    ax = fig.add_subplot(2, 2, i+1, projection='3d')                  
    
    face_colors = colorings[i](face_vectors)
    
    poly = mpl_toolkits.mplot3d.art3d.Poly3DCollection(vertices[faces])
    poly.set_facecolor(face_colors) 
    poly.set_edgecolor(None)
    poly.set_linewidth(0.25)
    
    ax.add_collection3d(poly)
        
    ax.set_xlim(-1,1)
    ax.set_ylim(-1,1)
    ax.set_zlim(-1,1)
    
    ax.azim = 40
    ax.dist = 10
    ax.elev = 35
    
    ax.set_xticks([-1,0,1])
    ax.set_yticks([-1,0,1])
    ax.set_zticks([-1,0,1])



