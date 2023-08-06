.. only:: html

    .. note::
        :class: sphx-glr-download-link-note

        Click :ref:`here <sphx_glr_download_auto_examples_1D_1_examples_plot_0_gmsl.py>`     to download the full example code
    .. rst-class:: sphx-glr-example-title

    .. _sphx_glr_auto_examples_1D_1_examples_plot_0_gmsl.py:


Global Mean Sea Level rise dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following dataset is the Global Mean Sea Level (GMSL) rise from the late
19th to the Early 21st Century [#f0]_. The
`original dataset <http://www.cmar.csiro.au/sealevel/sl_data_cmar.html>`_ was
downloaded as a CSV file and subsequently converted to the CSD model format.

Let's import this file.


.. code-block:: default

    import csdmpy as cp

    filename = "https://osu.box.com/shared/static/vetjm3cndxdps05ijvv603ajth3jocck.csdf"
    sea_level = cp.load(filename)








The variable `filename` is a string with the address to the `.csdf` file.
The :meth:`~csdmpy.load` method of the `csdmpy` module reads the
file and returns an instance of the :ref:`csdm_api` class, in
this case, as a variable ``sea_level``. For a quick preview of the data
structure, use the :attr:`~csdmpy.CSDM.data_structure` attribute of this
instance.


.. code-block:: default


    print(sea_level.data_structure)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    {
      "csdm": {
        "version": "1.0",
        "read_only": true,
        "timestamp": "2019-05-21T13:43:00Z",
        "tags": [
          "Jason-2",
          "satellite altimetry",
          "mean sea level",
          "climate"
        ],
        "description": "Global Mean Sea Level (GMSL) rise from the late 19th to the Early 21st Century.",
        "dimensions": [
          {
            "type": "linear",
            "count": 1608,
            "increment": "0.08333333333 yr",
            "coordinates_offset": "1880.0416666667 yr",
            "quantity_name": "time",
            "reciprocal": {
              "quantity_name": "frequency"
            }
          }
        ],
        "dependent_variables": [
          {
            "type": "internal",
            "name": "Global Mean Sea Level",
            "unit": "mm",
            "quantity_name": "length",
            "numeric_type": "float32",
            "quantity_type": "scalar",
            "component_labels": [
              "GMSL"
            ],
            "components": [
              [
                "-183.0, -171.125, ..., 59.6875, 58.5"
              ]
            ]
          }
        ]
      }
    }




.. warning::
    The serialized string from the :attr:`~csdmpy.CSDM.data_structure`
    attribute is not the same as the JSON serialization on the file.
    This attribute is only intended for a quick preview of the data
    structure and avoids displaying large datasets. Do not use
    the value of this attribute to save the data to the file. Instead, use the
    :meth:`~csdmpy.CSDM.save` method of the :ref:`CSDM <csdm_api>`
    class.

The tuple of the dimensions and dependent variables, from this example, are


.. code-block:: default


    x = sea_level.dimensions
    y = sea_level.dependent_variables








respectively. The coordinates along the dimension and the
component of the dependent variable are


.. code-block:: default

    print(x[0].coordinates)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    [1880.04166667 1880.125      1880.20833333 ... 2013.79166666 2013.87499999
     2013.95833333] yr




and


.. code-block:: default

    print(y[0].components[0])





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    [-183.     -171.125  -164.25   ...   66.375    59.6875   58.5   ]




respectively.

**Plotting the data**

.. note::
    The following code is only for illustrative purposes. The users may use
    any plotting library to visualize their datasets.


.. code-block:: default

    import matplotlib.pyplot as plt

    plt.figure(figsize=(6, 4))
    cp.plot(sea_level)
    plt.tight_layout()
    plt.show()




.. image:: /auto_examples/1D_1_examples/images/sphx_glr_plot_0_gmsl_001.png
    :alt: Global Mean Sea Level
    :class: sphx-glr-single-img





The following is a quick description of the above code. Within the code, we
make use of the csdm instance's attributes in addition to the matplotlib
functions. The first line is an import call for the matplotlib functions.
The following line generates a plot of the coordinates along the
dimension verse the component of the dependent variable.
The next line sets the x-range. For labeling the axes,
use the :attr:`~csdmpy.Dimension.axis_label` attribute
of both dimension and dependent variable instances. For the figure title,
use the :attr:`~csdmpy.DependentVariable.name` attribute
of the dependent variable instance. The next statement adds the grid lines.
For additional information, refer to `Matplotlib <https://matplotlib.org>`_
documentation.

.. seealso::
    :ref:`getting_started`


.. rubric:: Citation

.. [#f0] Church JA, White NJ. Sea-Level Rise from the Late 19th to the Early 21st Century.
         Surveys in Geophysics. 2011;32:585–602. DOI:10.1007/s10712-011-9119-1


.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  0.522 seconds)


.. _sphx_glr_download_auto_examples_1D_1_examples_plot_0_gmsl.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download sphx-glr-download-python

     :download:`Download Python source code: plot_0_gmsl.py <plot_0_gmsl.py>`



  .. container:: sphx-glr-download sphx-glr-download-jupyter

     :download:`Download Jupyter notebook: plot_0_gmsl.ipynb <plot_0_gmsl.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
