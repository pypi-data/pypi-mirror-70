Tutorials
=========

We've prepared tutorials using `Google Colab <https://colab.research.google.com/>`_ so that all computation can be performed using free GPUs. 
You can even analyze data on your cell phone!

Semi-supervised cell type classification using cell atlas references
------------------------------------------------------------------------------

This tutorial demonstrates how to train a semi-supervised `scNym` model using a pre-prepared cell atlas as a training data set and a new data set as the target.
You can upload your own data through Google Drive to classify cell types in a new experiment.

`Semi-supervised Training <https://colab.research.google.com/drive/1tu1O-nGne7Fi9RKh1ERpNBFnF7dzl93_>`_

Classifying cell types with pre-trained scNym models
------------------------------------------------------------------------------

We also provide a tutorial that uses pre-trained scNym model weights to classify cell types in your data. 
These predictions are less accurate than those provided by semi-supervised training with your data, but they are much faster to generate.

We provide pre-trained weights for mouse, rat, and human cell atlases.

`Classification with Pre-trained Models <https://colab.research.google.com/drive/1H3k-QNrqmJyzu8teTiwSSHBTpUwcg7bs>`_