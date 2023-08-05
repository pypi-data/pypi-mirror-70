.. module:: scnym
.. automodule:: scanpy
   :noindex:

Module Documentation
===========================

Import scNym as::

   import scnym


Interactive API: `api`
---------------------------

.. module:: scnym.api
.. currentmodule:: scanpy

scNym provides a simple Python API that serves as the primary endpoint for users.
This API should be the first stop for users looking to apply scNym to new problems.

.. automodule:: scnym.api
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource
   
   
Advanced Interface
--------------------------

For users interested in exploring new research ideas with the scNym framework, we provide direct access to our underlying infrastructure.
The modules below should be used by researchers looking to expand on the scNym approach.

Model Specification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: scnym.model
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource
   

Model Trainer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :trainer: Module provides classes for training neural network models to classify single cells.

.. automodule:: scnym.trainer
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource


Model Interpretation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :interpret: module provides saliency tools for interpreting model decisions.

.. automodule:: scnym.interpret
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource


Data Loaders
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


The :dataprep: module provides tools for loading and augmenting single cell data.


.. automodule:: scnym.dataprep
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource