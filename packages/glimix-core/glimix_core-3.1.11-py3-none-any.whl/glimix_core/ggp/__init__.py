r"""
****************************
Generalised Gaussian Process
****************************

Introduction
^^^^^^^^^^^^

A GP is a statistical distribution :math:`Y_t`, :math:`t\in\mathrm T`, for
which any finite linear combination of samples has a joint Gaussian
distribution `[1]`_ `[2]`_.
An instance of such class of processes is defined via a mean function
:math:`m(\cdot)` and a covariance function :math:`k(\cdot, \cdot)` whose
domains are :math:`\mathrm T` and :math:`\mathrm T\times\mathrm T`,
respectively.

Here we implement an extension of GPs that makes use of exponential-family
likelihoods.
An instance of such process is given by

.. math::

    \mathbf y \sim \int \prod_i \text{ExpFam}(y_i ~|~ \mu_i = g(z_i))
      \mathcal N(\mathbf z ~|~ \mathbf m, \mathrm K) \mathrm d\mathbf z.

:class:`.ExpFamGP` performs inference over the mean and covariance
parameters via maximum likelihood and Expectation Propagation `[3]`_
approximation.

.. _[1]: https://en.wikipedia.org/wiki/Gaussian_process
.. _[2]: http://www.gaussianprocess.org/gpml/
.. _[3]: http://www.gaussianprocess.org/gpml/chapters/RW3.pdf

Usage
^^^^^
"""
from ._expfam import ExpFamGP

__all__ = ["ExpFamGP"]
