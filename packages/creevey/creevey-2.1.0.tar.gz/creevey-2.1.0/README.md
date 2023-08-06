# Creevey

![](https://images.pottermore.com/bxd3o8b291gf/22qh5bCcA0g28OeKCwgwgE/70be84ace5da257fbd54d1ca0c06972c/ColinCreevey_WB_F2_ColinHoldingCamera_Still_080615_Land.jpg?w=320&h=320&fit=thumb&f=left&q=85)

Creevey is a file processing framework. It is designed for IO-bound workflows that involve reading files into memory, doing some processing on their contents, and writing out the results. It makes running those workflows faster and more reliable by parallelizing them across files, optional skipping files that have already been processed, handling errors, and keeping organized records of what happened.

Creevey was developed for deep learning computer vision projects, so in addition to the general framework it also provides predefined components for image processing. However, it can be used for any project that involves processing data from many sources.

See [the docs](https://creevey.readthedocs.io/) for more details.
