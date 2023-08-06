.. only:: html

    .. note::
        :class: sphx-glr-download-link-note

        Click :ref:`here <sphx_glr_download_auto_examples_tensor_plot_0_3D_diff_tensor_mri.py>`     to download the full example code
    .. rst-class:: sphx-glr-example-title

    .. _sphx_glr_auto_examples_tensor_plot_0_3D_diff_tensor_mri.py:


Diffusion tensor MRI, 3D{6} dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following is an example of a 3D{6} diffusion tensor MRI dataset with three
spatial dimensions, :math:`d=3`, and one, :math:`p=1`, dependent-variable
with six components. For illustration, we have reduced the size of the dataset.
The complete diffusion tensor MRI dataset, in the CSDM format, is available
`online <https://osu.box.com/shared/static/i7pwedo7sjabzr9qfn5q2gnjffqabp0p.csdf>`_.
The original dataset [#f1]_ is also available.

Let's import the CSDM data-file and look at its data structure.


.. code-block:: default

    import csdmpy as cp

    filename = "https://osu.box.com/shared/static/x5d1hgqjgo01wguyzwbv6e256erxejtx.csdf"
    diff_mri = cp.load(filename)








There are three linear dimensions in this dataset, corresponding to the x, y, and z
spatial dimensions,


.. code-block:: default

    x = diff_mri.dimensions
    print(x[0].label, x[1].label, x[2].label)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    x y z




and one six-component dependent variables holding the diffusion tensor components.
Because the diffusion tensor is a symmetric second-rank tensor, we only need six
tensor components. The components of the tensor are ordered as


.. code-block:: default

    y = diff_mri.dependent_variables
    print(y[0].component_labels)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    ['dxx', 'dxy', 'dxz', 'dyy', 'dyz', 'dzz']




The symmetric matrix information is also found with the
:attr:`~csdmpy.DependentVariable.quantity_type` attribute,


.. code-block:: default

    y[0].quantity_type





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    'symmetric_matrix_3'



which implies a 3x3 symmetric matrix.

**Visualize the dataset**

In the following, we visualize the isotropic diffusion coefficient, that is, the
average of the :math:`d_{xx}`, :math:`d_{yy}`, and :math:`d_{zz}` tensor components.
Since it's a three-dimensional dataset, we'll visualize the projections onto the
three dimensions.


.. code-block:: default


    # the isotropic diffusion coefficient.
    # component at index 0 = dxx
    # component at index 3 = dyy
    # component at index 5 = dzz
    isotropic_diffusion = (y[0].components[0] + y[0].components[3] + y[0].components[5]) / 3








In the following, we use certain features of the csdmpy module.
Please refer to :ref:`generating_csdm_objects` for  further details.


.. code-block:: default


    # Create a new csdm object from the isotropic diffusion coefficient array.
    new_csdm = cp.as_csdm(isotropic_diffusion, quantity_type="scalar")

    # Add the dimensions from `diff_mri` object to the `new_csdm` object.
    for i, dim in enumerate(x):
        new_csdm.dimensions[i] = dim








Now, we can plot the projections of the isotropic diffusion coefficients along
the respective dimensions as


.. code-block:: default

    import matplotlib.pyplot as plt

    # projection along the x-axis.
    plt.figure(figsize=(5, 4))
    cp.plot(new_csdm.sum(axis=0), cmap="gray_r", origin="upper")
    plt.tight_layout()
    plt.show()




.. image:: /auto_examples/tensor/images/sphx_glr_plot_0_3D_diff_tensor_mri_001.png
    :alt: plot 0 3D diff tensor mri
    :class: sphx-glr-single-img






.. code-block:: default


    # projection along the y-axis.
    plt.figure(figsize=(5, 4))
    cp.plot(new_csdm.sum(axis=1), cmap="gray_r", origin="upper")
    plt.tight_layout()
    plt.show()




.. image:: /auto_examples/tensor/images/sphx_glr_plot_0_3D_diff_tensor_mri_002.png
    :alt: plot 0 3D diff tensor mri
    :class: sphx-glr-single-img






.. code-block:: default


    # projection along the z-axis.
    plt.figure(figsize=(5, 4))
    cp.plot(new_csdm.sum(axis=2), cmap="gray_r", origin="upper")
    plt.tight_layout()
    plt.show()




.. image:: /auto_examples/tensor/images/sphx_glr_plot_0_3D_diff_tensor_mri_003.png
    :alt: plot 0 3D diff tensor mri
    :class: sphx-glr-single-img





.. rubric:: Citation

.. [#f1] Diffusion tensor MRI `dataset <http://www.sci.utah.edu/~gk/DTI-data/>`_; 2000.


.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  0.507 seconds)


.. _sphx_glr_download_auto_examples_tensor_plot_0_3D_diff_tensor_mri.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download sphx-glr-download-python

     :download:`Download Python source code: plot_0_3D_diff_tensor_mri.py <plot_0_3D_diff_tensor_mri.py>`



  .. container:: sphx-glr-download sphx-glr-download-jupyter

     :download:`Download Jupyter notebook: plot_0_3D_diff_tensor_mri.ipynb <plot_0_3D_diff_tensor_mri.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
