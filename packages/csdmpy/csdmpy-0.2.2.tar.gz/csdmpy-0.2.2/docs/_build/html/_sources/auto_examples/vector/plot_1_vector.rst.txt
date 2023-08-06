.. only:: html

    .. note::
        :class: sphx-glr-download-link-note

        Click :ref:`here <sphx_glr_download_auto_examples_vector_plot_1_vector.py>`     to download the full example code
    .. rst-class:: sphx-glr-example-title

    .. _sphx_glr_auto_examples_vector_plot_1_vector.py:


Vector, 2D{2} dataset
^^^^^^^^^^^^^^^^^^^^^

The 2D{2} datasets are two-dimensional, :math:`d=2`,
with one two-component dependent variable, :math:`p=2`.
The following is an example of a simulated electric field vector dataset of a
dipole as a function of two linearly sampled spatial dimensions.


.. code-block:: default

    import csdmpy as cp

    filename = "https://osu.box.com/shared/static/iobasl6fx1z7rds3ovamrwueek8ver5o.csdf"
    vector_data = cp.load(filename)
    print(vector_data.data_structure)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    {
      "csdm": {
        "version": "1.0",
        "read_only": true,
        "timestamp": "2014-09-30T11:16:33Z",
        "description": "A simulated electric field dataset from an electric dipole.",
        "dimensions": [
          {
            "type": "linear",
            "count": 64,
            "increment": "0.0625 cm",
            "coordinates_offset": "-2.0 cm",
            "quantity_name": "length",
            "label": "x",
            "reciprocal": {
              "quantity_name": "wavenumber"
            }
          },
          {
            "type": "linear",
            "count": 64,
            "increment": "0.0625 cm",
            "coordinates_offset": "-2.0 cm",
            "quantity_name": "length",
            "label": "y",
            "reciprocal": {
              "quantity_name": "wavenumber"
            }
          }
        ],
        "dependent_variables": [
          {
            "type": "internal",
            "name": "Electric field lines",
            "unit": "C^-1 * N",
            "quantity_name": "electric field strength",
            "numeric_type": "float32",
            "quantity_type": "vector_2",
            "components": [
              [
                "3.7466873e-07, 3.3365018e-07, ..., 3.5343004e-07, 4.0100363e-07"
              ],
              [
                "1.6129676e-06, 1.6765767e-06, ..., 1.846712e-06, 1.7754871e-06"
              ]
            ]
          }
        ]
      }
    }




The tuple of the dimension and dependent variable instances from this example
are


.. code-block:: default

    x = vector_data.dimensions
    y = vector_data.dependent_variables








with the respective coordinates (viewed only up to five values), as


.. code-block:: default

    print(x[0].coordinates[:5])





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    [-2.     -1.9375 -1.875  -1.8125 -1.75  ] cm





.. code-block:: default

    print(x[1].coordinates[:5])





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    [-2.     -1.9375 -1.875  -1.8125 -1.75  ] cm




The components of the dependent variable are vector components as seen
from the :attr:`~csdmpy.DependentVariable.quantity_type`
attribute of the corresponding dependent variable instance.


.. code-block:: default

    print(y[0].quantity_type)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    vector_2




**Visualizing the dataset**

Let's visualize the vector data using the *streamplot* method
from the matplotlib package. Before we could visualize, however, there
is an initial processing step. We use the Numpy library for processing.


.. code-block:: default

    import numpy as np

    X, Y = np.meshgrid(x[0].coordinates, x[1].coordinates)  # (x, y) coordinate pairs
    U, V = y[0].components[0], y[0].components[1]  # U and V are the components
    R = np.sqrt(U ** 2 + V ** 2)  # The magnitude of the vector
    R /= R.min()  # Scaled magnitude of the vector
    Rlog = np.log10(R)  # Scaled magnitude of the vector on a log scale








In the above steps, we calculate the X-Y grid points along with a
scaled magnitude of the vector dataset. The magnitude is scaled such that the
minimum value is one. Next, calculate the log of the scaled magnitude to
visualize the intensity on a logarithmic scale.

And now, the streamplot vector plot


.. code-block:: default

    import matplotlib.pyplot as plt

    plt.streamplot(
        X.value, Y.value, U, V, density=1, linewidth=Rlog, color=Rlog, cmap="viridis"
    )

    plt.xlim([x[0].coordinates[0].value, x[0].coordinates[-1].value])
    plt.ylim([x[1].coordinates[0].value, x[1].coordinates[-1].value])

    # Set axes labels and figure title.
    plt.xlabel(x[0].axis_label)
    plt.ylabel(x[1].axis_label)
    plt.title(y[0].name)

    # Set grid lines.
    plt.grid(color="gray", linestyle="--", linewidth=0.5)

    plt.tight_layout()
    plt.show()



.. image:: /auto_examples/vector/images/sphx_glr_plot_1_vector_001.png
    :alt: Electric field lines
    :class: sphx-glr-single-img






.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  0.834 seconds)


.. _sphx_glr_download_auto_examples_vector_plot_1_vector.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download sphx-glr-download-python

     :download:`Download Python source code: plot_1_vector.py <plot_1_vector.py>`



  .. container:: sphx-glr-download sphx-glr-download-jupyter

     :download:`Download Jupyter notebook: plot_1_vector.ipynb <plot_1_vector.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
