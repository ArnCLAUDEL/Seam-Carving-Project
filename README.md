# Seam-Carving-Project

UPEC Master 1 - Python Project

## Installation

This project runs with python 3 and the following librairies :

* TKinter
* Numpy
* Open CV
* PIL

## Getting Started

To start the application, you just need to execute app.py located in the root directory.

```
python3 app.py
```

## Description

### Functionalities

This project implements two seam carving algorithms to reduce the width of an image. The user can directly draw on the image to indicate important areas to preserve them. Some parameters of the algorithm can also be adjusted dynamically to speed-up computations at the expense of accuracy.

### Examples

IMG 1 -> -100 -> IMG 11

Here we have a first example with trees. We can see that the tree on the left is intact, the right one is shrinked but still looks normal.
However in the middle, the tree has one of his branches cut. 

IMG 2 -> -200 -> IMG 22

This castle is the best and most trivial example for seam carving. The castle and the watcher on the left are nearly never touched.
When we reduce the accuracy of the algorithm, we have few seams that cross the castle but it is unnoticeable.

IMG 3 -> -200 -> IMG 3

Finally, a last example with a skier. The skier himself keeps a good shape, which is not the case for his skis. Because of the resolution and the snow below the skier, his skis are cut just in front of his feet. After several seams, we follow the same path and his skis are shifted under the skier.

### Observations

We can see in those examples that in certain cases, well in fact in most cases, the seam carving can produce some visual artefacts even in important areas for humans.
In fact it depends on the image, some algorithm works better than others but overall, when important areas are indicated, it works well.
We haven't seen talked about accuracy. For the above examples, the accuracy was set to the maximum. However this is not necessary, after testing, we can lower the accuracy while having a pretty good result.