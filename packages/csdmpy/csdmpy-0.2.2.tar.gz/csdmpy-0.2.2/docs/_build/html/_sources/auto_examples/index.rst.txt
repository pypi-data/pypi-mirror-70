:orphan:



.. _sphx_glr_auto_examples:


===============
Example Gallery
===============

In this section, we present illustrative examples for importing files
serialized with the CSD model, using the `csdmpy` package.
Because the CSD model allows multi-dimensional datasets with multiple dependent
variables, we use a shorthand notation of :math:`d\mathrm{D}\{p\}` to
indicate that a dataset has a :math:`p`-component dependent variable defined
on a :math:`d`-dimensional coordinate grid.
In the case of `correlated datasets`, the number of components in each
dependent variable is given as a list within the curly braces, `i.e.`,
:math:`d\mathrm{D}\{p_0, p_1, p_2, ...\}`.

----

.. only:: latex

    **The sample CSDM compliant files used in this documentation are available**
    `online <https://osu.box.com/s/bq10pc5jyd3mu67vqvhw4xmrqgsd0x8u>`_.

.. only:: html

    **The sample CSDM compliant files used in this documentation are available online.**

    .. image:: https://img.shields.io/badge/Download-CSDM%20sample%20files-blueviolet
        :target: https://osu.box.com/s/bq10pc5jyd3mu67vqvhw4xmrqgsd0x8u

----


.. raw:: html

    <div class="sphx-glr-clear"></div>



.. _sphx_glr_auto_examples_1D_1_examples:

Scalar, 1D{1} datasets
======================

The 1D{1} datasets are one dimensional, :math:`d=1`, with one single-component,
:math:`p=1`, dependent variable. These datasets are the most common, and we,
therefore, provide a few examples from various fields of science.



.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Global Mean Sea Level rise dataset">

.. only:: html

 .. figure:: /auto_examples/1D_1_examples/images/thumb/sphx_glr_plot_0_gmsl_thumb.png
     :alt: Global Mean Sea Level rise dataset

     :ref:`sphx_glr_auto_examples_1D_1_examples_plot_0_gmsl.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_examples/1D_1_examples/plot_0_gmsl

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Nuclear Magnetic Resonance (NMR) dataset">

.. only:: html

 .. figure:: /auto_examples/1D_1_examples/images/thumb/sphx_glr_plot_1_NMR_bloch_thumb.png
     :alt: Nuclear Magnetic Resonance (NMR) dataset

     :ref:`sphx_glr_auto_examples_1D_1_examples_plot_1_NMR_bloch.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_examples/1D_1_examples/plot_1_NMR_bloch

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Electron Paramagnetic Resonance (EPR) dataset">

.. only:: html

 .. figure:: /auto_examples/1D_1_examples/images/thumb/sphx_glr_plot_2_EPR_thumb.png
     :alt: Electron Paramagnetic Resonance (EPR) dataset

     :ref:`sphx_glr_auto_examples_1D_1_examples_plot_2_EPR.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_examples/1D_1_examples/plot_2_EPR

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Gas Chromatography dataset">

.. only:: html

 .. figure:: /auto_examples/1D_1_examples/images/thumb/sphx_glr_plot_3_GS_thumb.png
     :alt: Gas Chromatography dataset

     :ref:`sphx_glr_auto_examples_1D_1_examples_plot_3_GS.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_examples/1D_1_examples/plot_3_GS

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Fourier Transform Infrared Spectroscopy (FTIR) dataset">

.. only:: html

 .. figure:: /auto_examples/1D_1_examples/images/thumb/sphx_glr_plot_4_FTIR_thumb.png
     :alt: Fourier Transform Infrared Spectroscopy (FTIR) dataset

     :ref:`sphx_glr_auto_examples_1D_1_examples_plot_4_FTIR.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_examples/1D_1_examples/plot_4_FTIR

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Ultraviolet–visible (UV-vis) dataset">

.. only:: html

 .. figure:: /auto_examples/1D_1_examples/images/thumb/sphx_glr_plot_5_UV-vis_thumb.png
     :alt: Ultraviolet–visible (UV-vis) dataset

     :ref:`sphx_glr_auto_examples_1D_1_examples_plot_5_UV-vis.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_examples/1D_1_examples/plot_5_UV-vis

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Mass spectrometry (sparse) dataset">

.. only:: html

 .. figure:: /auto_examples/1D_1_examples/images/thumb/sphx_glr_plot_6_Mass_thumb.png
     :alt: Mass spectrometry (sparse) dataset

     :ref:`sphx_glr_auto_examples_1D_1_examples_plot_6_Mass.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_examples/1D_1_examples/plot_6_Mass
.. raw:: html

    <div class="sphx-glr-clear"></div>



.. _sphx_glr_auto_examples_2D_1_examples:

Scalar, 2D{1} datasets
======================

The 2D{1} datasets are two dimensional, :math:`d=2`, with one
single-component dependent variable, :math:`p=1`. Following are some
2D{1} example datasets from various scientific fields expressed in CSDM
format.



.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Astronomy dataset">

.. only:: html

 .. figure:: /auto_examples/2D_1_examples/images/thumb/sphx_glr_plot_0_astronomy_thumb.png
     :alt: Astronomy dataset

     :ref:`sphx_glr_auto_examples_2D_1_examples_plot_0_astronomy.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_examples/2D_1_examples/plot_0_astronomy

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Nuclear Magnetic Resonance (NMR) dataset">

.. only:: html

 .. figure:: /auto_examples/2D_1_examples/images/thumb/sphx_glr_plot_1_NMR_satrec_thumb.png
     :alt: Nuclear Magnetic Resonance (NMR) dataset

     :ref:`sphx_glr_auto_examples_2D_1_examples_plot_1_NMR_satrec.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_examples/2D_1_examples/plot_1_NMR_satrec

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Transmission Electron Microscopy (TEM) dataset">

.. only:: html

 .. figure:: /auto_examples/2D_1_examples/images/thumb/sphx_glr_plot_2_TEM_thumb.png
     :alt: Transmission Electron Microscopy (TEM) dataset

     :ref:`sphx_glr_auto_examples_2D_1_examples_plot_2_TEM.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_examples/2D_1_examples/plot_2_TEM

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Labeled Dataset">

.. only:: html

 .. figure:: /auto_examples/2D_1_examples/images/thumb/sphx_glr_plot_3_labeled_thumb.png
     :alt: Labeled Dataset

     :ref:`sphx_glr_auto_examples_2D_1_examples_plot_3_labeled.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_examples/2D_1_examples/plot_3_labeled
.. raw:: html

    <div class="sphx-glr-clear"></div>



.. _sphx_glr_auto_examples_vector:

Vector datasets
===============



.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Vector, 1D{2} dataset">

.. only:: html

 .. figure:: /auto_examples/vector/images/thumb/sphx_glr_plot_0_vector_thumb.png
     :alt: Vector, 1D{2} dataset

     :ref:`sphx_glr_auto_examples_vector_plot_0_vector.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_examples/vector/plot_0_vector

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Vector, 2D{2} dataset">

.. only:: html

 .. figure:: /auto_examples/vector/images/thumb/sphx_glr_plot_1_vector_thumb.png
     :alt: Vector, 2D{2} dataset

     :ref:`sphx_glr_auto_examples_vector_plot_1_vector.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_examples/vector/plot_1_vector
.. raw:: html

    <div class="sphx-glr-clear"></div>



.. _sphx_glr_auto_examples_tensor:


Tensor datasets
===============



.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Diffusion tensor MRI, 3D{6} dataset">

.. only:: html

 .. figure:: /auto_examples/tensor/images/thumb/sphx_glr_plot_0_3D_diff_tensor_mri_thumb.png
     :alt: Diffusion tensor MRI, 3D{6} dataset

     :ref:`sphx_glr_auto_examples_tensor_plot_0_3D_diff_tensor_mri.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_examples/tensor/plot_0_3D_diff_tensor_mri
.. raw:: html

    <div class="sphx-glr-clear"></div>



.. _sphx_glr_auto_examples_pixel:

Pixel datasets
==============



.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Image, 2D{3} datasets">

.. only:: html

 .. figure:: /auto_examples/pixel/images/thumb/sphx_glr_plot_0_image_thumb.png
     :alt: Image, 2D{3} datasets

     :ref:`sphx_glr_auto_examples_pixel_plot_0_image.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_examples/pixel/plot_0_image
.. raw:: html

    <div class="sphx-glr-clear"></div>



.. _sphx_glr_auto_examples_correlated_examples:

Correlated datasets
===================

The Core Scientific Dataset Model (CSDM) supports multiple dependent
variables that share the same `d`-dimensional coordinate grid, where
:math:`d>=0`.
We call the dependent variables from these datasets as `correlated datasets`.
Following are a few examples of the correlated dataset.



.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Scatter, 0D{1,1} dataset">

.. only:: html

 .. figure:: /auto_examples/correlated_examples/images/thumb/sphx_glr_plot_0_0D11_dataset_thumb.png
     :alt: Scatter, 0D{1,1} dataset

     :ref:`sphx_glr_auto_examples_correlated_examples_plot_0_0D11_dataset.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_examples/correlated_examples/plot_0_0D11_dataset

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Meteorological, 2D{1,1,2,1,1} dataset">

.. only:: html

 .. figure:: /auto_examples/correlated_examples/images/thumb/sphx_glr_plot_1_meteorology_thumb.png
     :alt: Meteorological, 2D{1,1,2,1,1} dataset

     :ref:`sphx_glr_auto_examples_correlated_examples_plot_1_meteorology.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_examples/correlated_examples/plot_1_meteorology

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Astronomy, 2D{1,1,1} dataset (Creating image composition)">

.. only:: html

 .. figure:: /auto_examples/correlated_examples/images/thumb/sphx_glr_plot_2_astronomy_thumb.png
     :alt: Astronomy, 2D{1,1,1} dataset (Creating image composition)

     :ref:`sphx_glr_auto_examples_correlated_examples_plot_2_astronomy.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_examples/correlated_examples/plot_2_astronomy
.. raw:: html

    <div class="sphx-glr-clear"></div>



.. _sphx_glr_auto_examples_sparse:

Sparse datasets
===============



.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Sparse along one dimension, 2D{1,1} dataset">

.. only:: html

 .. figure:: /auto_examples/sparse/images/thumb/sphx_glr_plot_0_1D_sparse_thumb.png
     :alt: Sparse along one dimension, 2D{1,1} dataset

     :ref:`sphx_glr_auto_examples_sparse_plot_0_1D_sparse.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_examples/sparse/plot_0_1D_sparse

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Sparse along two dimensions, 2D{1,1} dataset">

.. only:: html

 .. figure:: /auto_examples/sparse/images/thumb/sphx_glr_plot_1_2D_sparse_thumb.png
     :alt: Sparse along two dimensions, 2D{1,1} dataset

     :ref:`sphx_glr_auto_examples_sparse_plot_1_2D_sparse.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_examples/sparse/plot_1_2D_sparse
.. raw:: html

    <div class="sphx-glr-clear"></div>



.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-gallery


  .. container:: sphx-glr-download sphx-glr-download-python

    :download:`Download all examples in Python source code: auto_examples_python.zip <//Users/deepansh/Research/NMRgit/csdmpy/csdmpy/docs/auto_examples/auto_examples_python.zip>`



  .. container:: sphx-glr-download sphx-glr-download-jupyter

    :download:`Download all examples in Jupyter notebooks: auto_examples_jupyter.zip <//Users/deepansh/Research/NMRgit/csdmpy/csdmpy/docs/auto_examples/auto_examples_jupyter.zip>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
