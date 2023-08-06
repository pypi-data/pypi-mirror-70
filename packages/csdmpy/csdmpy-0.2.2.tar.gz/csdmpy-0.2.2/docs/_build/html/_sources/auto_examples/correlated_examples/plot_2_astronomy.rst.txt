.. only:: html

    .. note::
        :class: sphx-glr-download-link-note

        Click :ref:`here <sphx_glr_download_auto_examples_correlated_examples_plot_2_astronomy.py>`     to download the full example code
    .. rst-class:: sphx-glr-example-title

    .. _sphx_glr_auto_examples_correlated_examples_plot_2_astronomy.py:


Astronomy, 2D{1,1,1} dataset (Creating image composition)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. code-block:: default








More often, the images in astronomy are a composition of datasets measured
at different wavelengths over an area of the sky. In this example, we
illustrate the use of the CSDM file-format, and `csdmpy` module, beyond just
reading a CSDM-compliant file. We'll use these datasets, and compose an image,
using Numpy arrays.
The following example is the data from the `Eagle Nebula` acquired at three
different wavelengths and serialized as a CSDM compliant file.

Import the `csdmpy` model and load the dataset.


.. code-block:: default

    import csdmpy as cp

    filename = "https://osu.box.com/shared/static/of3wmoxcqungkp6ndbplnbxtgu6jaahh.csdf"
    eagle_nebula = cp.load(filename)








Let's get the tuple of dimension and dependent variable objects from
the ``eagle_nebula`` instance.


.. code-block:: default

    x = eagle_nebula.dimensions
    y = eagle_nebula.dependent_variables








Before we compose an image, let's take a look at the individual
dependent variables from the dataset. The three dependent variables correspond
to signal acquisition at 502 nm, 656 nm, and 673 nm, respectively. This
information is also listed in the
:attr:`~csdmpy.DependentVariable.name` attribute of the
respective dependent variable instances,


.. code-block:: default

    y[0].name





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    'Eagle Nebula acquired @ 502 nm'




.. code-block:: default

    y[1].name





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    'Eagle Nebula acquired @ 656 nm'




.. code-block:: default

    y[2].name





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    'Eagle Nebula acquired @ 673 nm'



We use the following script to plot the dependent variables.


.. code-block:: default

    import matplotlib.pyplot as plt


    def plot_scalar(yx):

        # Set the extents of the image plot.
        extent = [
            x[0].coordinates[0].value,
            x[0].coordinates[-1].value,
            x[1].coordinates[0].value,
            x[1].coordinates[-1].value,
        ]

        # Add the image plot.
        y0 = yx.components[0]
        y0 = y0 / y0.max()
        im = plt.imshow(y0, origin="lower", extent=extent, cmap="bone", vmax=0.1)

        # Add a colorbar.
        cbar = plt.gca().figure.colorbar(im)
        cbar.ax.set_ylabel(yx.axis_label[0])

        # Set up the axes label and figure title.
        plt.xlabel(x[0].axis_label)
        plt.ylabel(x[1].axis_label)
        plt.title(yx.name)

        # Set up the grid lines.
        plt.grid(color="k", linestyle="--", linewidth=0.5)

        plt.tight_layout()
        plt.show()









Let's plot the dependent variables, first dependent variable,


.. code-block:: default

    plot_scalar(y[0])




.. image:: /auto_examples/correlated_examples/images/sphx_glr_plot_2_astronomy_001.png
    :alt: Eagle Nebula acquired @ 502 nm
    :class: sphx-glr-single-img





second dependent variable, and


.. code-block:: default

    plot_scalar(y[1])




.. image:: /auto_examples/correlated_examples/images/sphx_glr_plot_2_astronomy_002.png
    :alt: Eagle Nebula acquired @ 656 nm
    :class: sphx-glr-single-img





the third dependent variable.


.. code-block:: default

    plot_scalar(y[2])




.. image:: /auto_examples/correlated_examples/images/sphx_glr_plot_2_astronomy_003.png
    :alt: Eagle Nebula acquired @ 673 nm
    :class: sphx-glr-single-img





Image composition
*****************


.. code-block:: default

    import numpy as np








For the image composition, we assign the dependent variable at index zero as
the blue channel, index one as the green channel, and index two as the red
channel of an RGB image. Start with creating an empty array to hold the RGB
dataset.


.. code-block:: default

    shape = y[0].components[0].shape + (3,)
    image = np.empty(shape, dtype=np.float64)








Here, ``image`` is the variable we use for storing the composition. Add
the respective dependent variables to the designated color channel in the
``image`` array,


.. code-block:: default

    image[..., 0] = y[2].components[0] / y[2].components[0].max()  # red channel
    image[..., 1] = y[1].components[0] / y[1].components[0].max()  # green channel
    image[..., 2] = y[0].components[0] / y[0].components[0].max()  # blue channel








Following the intensity plot of the individual dependent variables, see the
above figures, it is evident that the component intensity from ``y[1]`` and,
therefore, the green channel dominates the other two. If we
plot the ``image`` data, the image will be saturated with green intensity. To
attain a color-balanced image, we arbitrarily scale the intensities from the
three channels. You may choose any scaling factor. Each scaling factor will
produce a different composition. In this example, we use the following,


.. code-block:: default

    image[..., 0] = np.clip(image[..., 0] * 65.0, 0, 1)  # red channel
    image[..., 1] = np.clip(image[..., 1] * 7.50, 0, 1)  # green channel
    image[..., 2] = np.clip(image[..., 2] * 75.0, 0, 1)  # blue channel








Now to plot this composition.


.. code-block:: default


    # Set the extents of the image plot.
    extent = [
        x[0].coordinates[0].value,
        x[0].coordinates[-1].value,
        x[1].coordinates[0].value,
        x[1].coordinates[-1].value,
    ]

    # add figure
    plt.imshow(image, origin="lower", extent=extent)

    plt.xlabel(x[0].axis_label)
    plt.ylabel(x[1].axis_label)
    plt.title("composition")

    plt.tight_layout()
    plt.show()



.. image:: /auto_examples/correlated_examples/images/sphx_glr_plot_2_astronomy_004.png
    :alt: composition
    :class: sphx-glr-single-img






.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  1.895 seconds)


.. _sphx_glr_download_auto_examples_correlated_examples_plot_2_astronomy.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download sphx-glr-download-python

     :download:`Download Python source code: plot_2_astronomy.py <plot_2_astronomy.py>`



  .. container:: sphx-glr-download sphx-glr-download-jupyter

     :download:`Download Jupyter notebook: plot_2_astronomy.ipynb <plot_2_astronomy.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
