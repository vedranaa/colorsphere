import matplotlib.cm
import numpy as np


class SCmap():
    '''
    Base class for all spherical colormaps.
    
    SCmap is callable, it takes as input an array of shape (3, :) containing 
    coordinates x, y, and z. It returns an array of shape (3, :) containing
    colors r, g, and b.
    
    '''
    name = 'SCmap'
    
    def __init__(self, z_direction=None, rotation=None, ordering=None):
        self.rotation = rotation
        if self.rotation is None and z_direction is not None:
            self.rotation = get_rotation(z_direction)
        self.ordering = ordering
        
    def __call__(self, vectors):
        
        if self.ordering is not None:
            vectors = vectors[:,self.ordering]
        if self.rotation is not None:
            vectors =  vectors @ self.rotation.T
        
        vectors_norm = vectors/np.sqrt((vectors**2).sum(axis=1, keepdims=True))
        return self.color(vectors_norm)
    
    
        

class Tre(SCmap):
    '''
    Suitable for SCmap vectors which are interpretable as: 'mostly x', 
    'mostly y' or 'mostly z'.'
    (Tre as for three axes.)
    '''
    
    name = 'Tre'
            
    def color(self, vectors):
        return np.abs(vectors)
    

class Uno(SCmap):
    '''
    Suitable for SCmap vectors predominantly in one (z) direction. 
    Orientations in orhogonal (x-y) plane are gray. Orientations in 
    predominant directions are white.
    (Uno as for unidirectional.)
    ''' 
    
    name = 'Uno'

    def color(self, vectors):
        
        s = np.mod(np.arctan2(vectors[:,1], vectors[:,0]) + 
                   (vectors[:,2]<0)*np.pi, 2*np.pi)   
        h_pole = vectors[:,2]**2
        h_pole = h_pole[:,None]
        h_equator = 1-h_pole
        colors = matplotlib.cm.hsv(s/(2*np.pi))[:,:3]
        h_pole = h_pole**8
        colors = colors * (1 - h_pole) + 1 * h_pole
        h_equator = h_equator**8
        colors = colors * (1 - h_equator) + 0.25 * h_equator
        return colors
    

class Duo(SCmap):
    '''
    Suitable for SCmap vectors predominantly in a x-y plane. Orientations
    in z direction are gray.
    (Duo as for two directions i.e. plane.)
    '''  

    name = 'Duo'
            
    def color(self, vectors):
        
        h = vectors[:,2]**2  # no discontinuity and less gray
        h = h[:,None]
        s = np.mod(np.arctan2(vectors[:,1], vectors[:,0]), np.pi)
        colors = matplotlib.cm.hsv(s/np.pi)[:,:3] * (1-h) + 0.5*h
        return colors


class Ico(SCmap):
    '''
    Suitable for SCmap vectors with no known predominant orientations.
    (Ico as for icosahedron-based.)
    '''

    name = 'Ico'
    
    def __init__(self, z_direction=None, rotation=None, ordering=None):
        
        super().__init__(z_direction, rotation, ordering)    
        phi = (1+np.sqrt(5))/2    
        vertices = np.array([
            [0, 1, phi], [0,-1, phi], [1, phi, 0],
            [-1, phi, 0], [phi, 0, 1], [-phi, 0, 1]])/np.sqrt(1 + phi**2)
        self.vertices = np.concatenate((vertices, -vertices))
        vertex_colors = np.array([[1, 1, 0, 0, 0, 1], [0, 1, 1, 1, 0, 0],
                                  [0, 0, 0, 1, 1, 1]]).T
        self.vertex_colors = np.concatenate((vertex_colors, vertex_colors))

    def color(self, vectors):
        
        ijk = np.argsort(vectors @ self.vertices.T, axis=1)[:,-1:-4:-1] # we need only 3 closest centers
        
        # baricentric coordinates (A,B,C either all positive or all negative)
        A = np.cross(self.vertices[ijk[:,1], :], self.vertices[ijk[:,2], :])
        B = np.cross(self.vertices[ijk[:,2], :], self.vertices[ijk[:,0], :])
        C = np.cross(self.vertices[ijk[:,0], :], self.vertices[ijk[:,1], :])
        
        A = (vectors * A).sum(axis=1, keepdims=True)
        B = (vectors * B).sum(axis=1, keepdims=True)
        C = (vectors * C).sum(axis=1, keepdims=True)
    
        # # normalization
        # n = 1/(A+B+C)
        # A = A*n
        # B = B*n
        # C = C*n
        
        # attempt with potentions
        k = 2
        A = A**k
        B = B**k
        C = C**k
        
        rgb = (A * self.vertex_colors[ijk[:,0],:] + B * self.vertex_colors[ijk[:,1],:] + 
                    C * self.vertex_colors[ijk[:,2],:])
            
        rgb /= (A+B+C)  # normalization
        
        return rgb

class Inc(SCmap):
    '''
    SCmap based on inclination.
    '''
    
    name = 'Inc'

    def __init__(self, z_direction=None, rotation=None, ordering=None, 
                 cmap=None, symmetric = True):
        
        if cmap is None:
            self.cmap = matplotlib.cm.jet
        else:
            self.cmap = cmap

        self.symmetric = symmetric
        super().__init__(z_direction, rotation, ordering)    
    
    def color(self, vectors):
        
        inc = np.arcsin(vectors[:,2])/(0.5*np.pi)  # from -1 to 1 
        if self.symmetric:
            inc = abs(inc) 
        else:
            inc = 0.5*(inc+1)
            
        colors = self.cmap(inc)[:,:3]
        return colors
    

class Azy(SCmap):
    '''
    SCmap based on azymuth.
    '''

    name = 'Azy'
    
    def __init__(self, z_direction=None, rotation=None, ordering=None,
                 cmap=None, symmetric = True):
        
        if cmap is None:
            self.cmap = matplotlib.cm.hsv
        else:
            self.cmap = cmap
            
        self.symmetric = symmetric
        super().__init__(z_direction, rotation, ordering)    
    
    def color(self, vectors):
        
        a = np.arctan2(vectors[:,1], vectors[:,0])/np.pi     # from -1 to 1 
        if self.symmetric:
            a = np.mod(a, 1)
        else:
            a = 0.5*(a+1)
       
        colors = self.cmap(a)[:,:3]
        return colors
    

def get_rotation(z, y=None):
    '''
    Given a direction z and optionally y returns an orthogonal coordinate 
    system, i.e. a rotation matrix transforming identity to [x,y,z].  
    '''
    
    z = np.array(z, dtype=np.double)
    z /= np.sqrt((z**2).sum())
    
    if y is None:
        y = np.array([0,1,0], dtype=np.double)
        if abs(np.dot(y,z))>0.9:
            y = np.array([1,0,0], dtype=np.double)
    else:   
        y = np.array(y, dtype=np.double)
   
    y = y - np.dot(y,z)*z
    y /= np.sqrt((y**2).sum())
    
    x = np.cross(y,z)
    
    return(np.stack((x,y,z)))


    
    
    
    