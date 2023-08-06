```python
import numpy as np
import matplotlib.pyplot as plt

from wfslib.geometry import Geometry
from wfslib.wfs import WFSData
```

### Крупная сетка засвеченная полностью 


```python
from PIL import Image


path = "../data/bad_img3.tiff"

arr = np.array(Image.open(path))[500:1500, 500:1500]
arr = np.expand_dims(arr, 0)
wfs = WFSData(arr)
wfs.geometry.set_options(shift=(-22, -36))
wfs.reference = 27
wfs.good_only = True #отображать только качественные субапертуры
plt.imshow(arr[0])
wfs.show_geometry()
```

    240.66666666666666
    317.0
    

    C:\Users\mi\Anaconda3\lib\site-packages\wfslib\wfs.py:164: UserWarning: WARNING: Set the geometry for the file!
      warn("WARNING: Set the geometry for the file!", UserWarning)
    


![png](output_2_2.png)



![png](output_2_3.png)



```python
#print(str (wfs[0].get_offset(43)))
wfs.mask = True
plt.subplot(1,2,1)
plt.imshow(wfs[0][17])
plt.subplot(1,2,2)
plt.imshow(wfs[0][1])
```




    <matplotlib.image.AxesImage at 0x2781c39aa90>




![png](output_3_1.png)


### Крупная сетка хасвеченная диагонально


```python
path = "../data/bad_img1.tiff"

Geometry.only_wavelets = 0

arr = np.array(Image.open(path))[500:1500, 500:1500]
arr = np.expand_dims(arr, 0)
wfs = WFSData(arr)
wfs.geometry.set_options(shift=(-65, -15))
wfs.reference = 27



plt.imshow(arr[0])
wfs.show_geometry(show_type = "offsets")
```

    314.0
    342.5
    

    C:\Users\mi\Anaconda3\lib\site-packages\wfslib\wfs.py:164: UserWarning: WARNING: Set the geometry for the file!
      warn("WARNING: Set the geometry for the file!", UserWarning)
    


![png](output_5_2.png)



![png](output_5_3.png)


### Мелкая сетка полностью засвеченная


```python
wfs = WFSData('../data/file.h5', dataset_name = "data")
#wfs.close_stream()
p = wfs.geometry.options
print(p)
wfs.geometry.set_options( shift = (-1,1), border = 6)
wfs.reference = 87
#wfs.domask = True

wfs.show_geometry()
wfs[0].offsets()

#    plt.imshow(wfs[0][172])    
print(wfs[1].get_offset(130))

```

    3
    125.0
    29.333333333333332
    {'border': 8.0, 'cell_width': 32.0, 'start_point': [139, 99]}
    

    ../..\wfslib\wfs.py:164: UserWarning: WARNING: Set the geometry for the file!
      warn("WARNING: Set the geometry for the file!", UserWarning)
    


![png](output_7_2.png)


    [0. 0.]
    

### Точки


```python


path = "../data/bad_img2.tiff"

arr = np.array(Image.open(path))
arr = np.expand_dims(arr, 0)

plt.imshow(arr[0])
wfs = WFSData(arr)
wfs.geometry.set_options(shift=(64, -38),swap = True, rotate = 1)

#plt.imshow(arr[0])
wfs.show_geometry()
```

    134.0
    210.5
    

    ../..\wfslib\wfs.py:164: UserWarning: WARNING: Set the geometry for the file!
      warn("WARNING: Set the geometry for the file!", UserWarning)
    


![png](output_9_2.png)



![png](output_9_3.png)


## Bims


```python
def read_bim(path):
    with open(path, "rb") as f:
        ny = int.from_bytes(f.read(4), "little")
        nx = int.from_bytes(f.read(4), "little")
        return np.frombuffer(f.read()).reshape(ny, nx)
```


```python
bim_img = read_bim("../data/bims/lsvt-z2=-2.bim").copy()
plt.imshow(bim_img)
```




    <matplotlib.image.AxesImage at 0x2781c113b70>




![png](output_12_1.png)



```python
Geometry.only_wavelets = 0
wfs = WFSData(bim_img)

p = wfs.geometry.options
print(p)
wfs.geometry.set_options(shift=(-56, -38))

wfs.good_only = True
wfs.reference = 0
#plt.imshow(arr[0])
wfs.show_geometry(show_type = "offsets")
wfs.show_geometry()
```

    132.0
    106.66666666666667
    {'border': 4.0, 'cell_width': 76.0, 'start_point': [185, 167]}
    

    ../..\wfslib\wfs.py:164: UserWarning: WARNING: Set the geometry for the file!
      warn("WARNING: Set the geometry for the file!", UserWarning)
    


![png](output_13_2.png)



![png](output_13_3.png)


### Разные функции качества


```python
def qualitative_sub_std(cell, std, mean_val):
        return np.mean(cell) > std
    
def qualitative_sub_mean(cell, std, mean_val):
        return np.mean(cell) > mean_val

def qualitative_sub_median(cell, std, mean_val):
    return np.median(cell) > mean_val
```


```python

path = "../data/bad_img3.tiff"

arr = np.array(Image.open(path))[500:1500, 500:1500]
arr = np.expand_dims(arr, 0)
wfs = WFSData(arr)
wfs.geometry.set_options(shift=(-22, -36))
wfs.qualitative_function = qualitative_sub_mean
wfs.reference = 27

wfs.show_geometry()
```

    240.66666666666666
    317.0
    

    ../..\wfslib\wfs.py:164: UserWarning: WARNING: Set the geometry for the file!
      warn("WARNING: Set the geometry for the file!", UserWarning)
    


![png](output_16_2.png)



```python
wfs.qualitative_function = qualitative_sub_median
wfs.show_geometry()
```


![png](output_17_0.png)



```python
wfs.qualitative_function = qualitative_sub_std
wfs.show_geometry()
```


![png](output_18_0.png)


### Cмотрим смещения


```python

path = "../data/bad_img3.tiff"

arr = np.array(Image.open(path))[500:1500, 500:1500]
arr = np.expand_dims(arr, 0)
wfs = WFSData(arr)
wfs.geometry.set_options(shift=(-22, -36))
wfs.qualitative_function = qualitative_sub_mean
wfs.reference = 13
wfs.good_only = True

wfs.show_geometry()
```

    240.66666666666666
    317.0
    

    ../..\wfslib\wfs.py:164: UserWarning: WARNING: Set the geometry for the file!
      warn("WARNING: Set the geometry for the file!", UserWarning)
    


![png](output_20_2.png)



```python
wfs[0].offsets()
```




    array([[-28., -23.],
           [-25.,  -0.],
           [-30.,  -0.],
           [-29.,  -1.],
           [-28., -43.],
           [-25., -47.],
           [-28.,  -0.],
           [  1.,  -0.],
           [ 45.,  -0.],
           [-30., -43.],
           [-25., -37.],
           [ -0.,  -0.],
           [ 24.,  -0.],
           [ -0.,  -0.],
           [-26.,  -1.],
           [ 46., -35.],
           [ 38.,  -0.],
           [ 42.,  -0.],
           [-30.,  -0.],
           [ 41., -31.],
           [ 34., -40.],
           [ 31.,  -0.],
           [ 41.,  -0.],
           [ 37., -36.],
           [ 34., -39.],
           [ 29., -45.],
           [ 24., -32.]])




```python

```


```python

```


```python

```
