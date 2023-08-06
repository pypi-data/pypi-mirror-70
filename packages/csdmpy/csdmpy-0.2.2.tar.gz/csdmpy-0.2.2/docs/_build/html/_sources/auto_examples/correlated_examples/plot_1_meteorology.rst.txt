.. only:: html

    .. note::
        :class: sphx-glr-download-link-note

        Click :ref:`here <sphx_glr_download_auto_examples_correlated_examples_plot_1_meteorology.py>`     to download the full example code
    .. rst-class:: sphx-glr-example-title

    .. _sphx_glr_auto_examples_correlated_examples_plot_1_meteorology.py:


Meteorological, 2D{1,1,2,1,1} dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. code-block:: default








The following dataset is obtained from `NOAA/NCEP Global Forecast System (GFS) Atmospheric Model
<https://coastwatch.pfeg.noaa.gov/erddap/griddap/NCEP_Global_Best.graph?ugrd10m[(2017-09-17T12:00:00Z)][(-4.5):(52.0)][(275.0):(331.5)]&.draw=surface&.vars=longitude%7Clatitude%7Cugrd10m&.colorBar=%7C%7C%7C%7C%7C&.bgColor=0xffccccff>`_
and subsequently converted to the CSD model file-format.
The dataset consists of two spatial dimensions describing the geographical
coordinates of the earth surface and five dependent variables with
1) surface temperature, 2) air temperature at 2 m, 3) relative humidity,
4) air pressure at sea level as the four `scalar` quantity_type dependent
variables, and 5) wind velocity as the two-component `vector`, quantity_type
dependent variable.

Let's import the `csdmpy` module and load this dataset.


.. code-block:: default

    import csdmpy as cp

    filename = "https://osu.box.com/shared/static/6uhrtdxfisl4a14x9pndyze2mv414zyg.csdf"
    multi_dataset = cp.load(filename)








The tuple of dimension and dependent variable objects from
``multi_dataset`` instance are


.. code-block:: default

    x = multi_dataset.dimensions
    y = multi_dataset.dependent_variables








The dataset contains two dimension objects representing the `longitude` and
`latitude` of the earth's surface. The labels along thee respective dimensions are


.. code-block:: default

    x[0].label





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    'longitude'




.. code-block:: default

    x[1].label





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    'latitude'



There are a total of five dependent variables stored in this dataset. The first
dependent variable is the surface air temperature. The data structure of this
dependent variable is


.. code-block:: default

    print(y[0].data_structure)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    {
      "type": "internal",
      "description": "The label 'tmpsfc' is the standard attribute name for 'surface air temperature'.",
      "name": "Surface temperature",
      "unit": "K",
      "quantity_name": "temperature",
      "numeric_type": "float64",
      "quantity_type": "scalar",
      "component_labels": [
        "tmpsfc - surface air temperature"
      ],
      "components": [
        [
          "292.8152160644531, 293.0152282714844, ..., 301.8152160644531, 303.8152160644531"
        ]
      ]
    }




If you have followed all previous examples, the above data structure should
be self-explanatory.

We will use the following snippet to plot the dependent variables of scalar
`quantity_type`.


.. code-block:: default

    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.axes_grid1 import make_axes_locatable


    def plot_scalar(yx):
        fig, ax = plt.subplots(1, 1, figsize=(6, 3))

        # Set the extents of the image plot.
        extent = [
            x[0].coordinates[0].value,
            x[0].coordinates[-1].value,
            x[1].coordinates[0].value,
            x[1].coordinates[-1].value,
        ]

        # Add the image plot.
        im = ax.imshow(yx.components[0], origin="lower", extent=extent, cmap="coolwarm")

        # Add a colorbar.
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cbar = fig.colorbar(im, cax)
        cbar.ax.set_ylabel(yx.axis_label[0])

        # Set up the axes label and figure title.
        ax.set_xlabel(x[0].axis_label)
        ax.set_ylabel(x[1].axis_label)
        ax.set_title(yx.name)

        # Set up the grid lines.
        ax.grid(color="k", linestyle="--", linewidth=0.5)

        plt.tight_layout()
        plt.show()









Now to plot the data from the dependent variable.


.. code-block:: default

    plot_scalar(y[0])




.. image:: /auto_examples/correlated_examples/images/sphx_glr_plot_1_meteorology_001.png
    :alt: Surface temperature
    :class: sphx-glr-single-img





Similarly, other dependent variables with their respective plots are


.. code-block:: default

    y[1].name





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    'Air temperature at 2m'




.. code-block:: default

    plot_scalar(y[1])




.. image:: /auto_examples/correlated_examples/images/sphx_glr_plot_1_meteorology_002.png
    :alt: Air temperature at 2m
    :class: sphx-glr-single-img






.. code-block:: default

    y[3].name





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    'Relative humidity'




.. code-block:: default

    plot_scalar(y[3])




.. image:: /auto_examples/correlated_examples/images/sphx_glr_plot_1_meteorology_003.png
    :alt: Relative humidity
    :class: sphx-glr-single-img






.. code-block:: default

    y[4].name





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    'Air pressure at sea level'




.. code-block:: default

    plot_scalar(y[4])




.. image:: /auto_examples/correlated_examples/images/sphx_glr_plot_1_meteorology_004.png
    :alt: Air pressure at sea level
    :class: sphx-glr-single-img





Notice, we skipped the dependent variable at index two. The reason is that
this particular dependent variable is a vector dataset,


.. code-block:: default

    y[2].quantity_type





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    'vector_2'




.. code-block:: default

    y[2].name





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    'Wind velocity'



which represents the wind velocity, and requires a vector visualization
routine. To visualize the vector data, we use the matplotlib quiver plot.


.. code-block:: default



    def plot_vector(yx):
        fig, ax = plt.subplots(1, 1, figsize=(6, 3))
        magnitude = np.sqrt(yx.components[0] ** 2 + yx.components[1] ** 2)

        cf = ax.quiver(
            x[0].coordinates,
            x[1].coordinates,
            yx.components[0],
            yx.components[1],
            magnitude,
            pivot="middle",
            cmap="inferno",
        )
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cbar = fig.colorbar(cf, cax)
        cbar.ax.set_ylabel(yx.name + " / " + str(yx.unit))

        ax.set_xlim([x[0].coordinates[0].value, x[0].coordinates[-1].value])
        ax.set_ylim([x[1].coordinates[0].value, x[1].coordinates[-1].value])

        # Set axes labels and figure title.
        ax.set_xlabel(x[0].axis_label)
        ax.set_ylabel(x[1].axis_label)
        ax.set_title(yx.name)

        # Set grid lines.
        ax.grid(color="gray", linestyle="--", linewidth=0.5)

        plt.tight_layout()
        plt.show()










.. code-block:: default

    plot_vector(y[2])



.. image:: /auto_examples/correlated_examples/images/sphx_glr_plot_1_meteorology_005.png
    :alt: Wind velocity
    :class: sphx-glr-single-img






.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  1.025 seconds)


.. _sphx_glr_download_auto_examples_correlated_examples_plot_1_meteorology.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download sphx-glr-download-python

     :download:`Download Python source code: plot_1_meteorology.py <plot_1_meteorology.py>`



  .. container:: sphx-glr-download sphx-glr-download-jupyter

     :download:`Download Jupyter notebook: plot_1_meteorology.ipynb <plot_1_meteorology.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
