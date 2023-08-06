.. only:: html

    .. note::
        :class: sphx-glr-download-link-note

        Click :ref:`here <sphx_glr_download_auto_examples_2D_1_examples_plot_0_astronomy.py>`     to download the full example code
    .. rst-class:: sphx-glr-example-title

    .. _sphx_glr_auto_examples_2D_1_examples_plot_0_astronomy.py:


Astronomy dataset
^^^^^^^^^^^^^^^^^

The following dataset is a new observation of the Bubble Nebula
acquired by
`The Hubble Heritage Team <https://archive.stsci.edu/prepds/heritage/bubble/introduction.html>`_,
in February 2016. The original dataset was obtained in the FITS format
and subsequently converted to the CSD model file-format. For the convenience of
illustration, we have downsampled the original dataset.

Let's load the `.csdfe` file and look at its data structure.


.. code-block:: default

    import matplotlib.pyplot as plt

    import csdmpy as cp

    filename = "https://osu.box.com/shared/static/0p3o1ga1kqno4dk4sooi1rbk29pbs3mm.csdf"
    bubble_nebula = cp.load(filename)
    print(bubble_nebula.data_structure)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    {
      "csdm": {
        "version": "1.0",
        "timestamp": "2020-01-04T01:43:31Z",
        "description": "The dataset is a new observation of the Bubble Nebula acquired by The Hubble Heritage Team, in February 2016.",
        "dimensions": [
          {
            "type": "linear",
            "count": 1024,
            "increment": "-0.0002581136196 °",
            "coordinates_offset": "350.311874957 °",
            "quantity_name": "plane angle",
            "label": "Right Ascension"
          },
          {
            "type": "linear",
            "count": 1024,
            "increment": "0.0001219957797701109 °",
            "coordinates_offset": "61.12851494969163 °",
            "quantity_name": "plane angle",
            "label": "Declination"
          }
        ],
        "dependent_variables": [
          {
            "type": "internal",
            "name": "Bubble Nebula, 656nm",
            "numeric_type": "float32",
            "quantity_type": "scalar",
            "components": [
              [
                "0.0, 0.0, ..., 0.0, 0.0"
              ]
            ]
          }
        ]
      }
    }




Here, the variable ``bubble_nebula`` is an instance of the :ref:`csdm_api`
class. From the data structure, one finds two dimensions, labeled as
*Right Ascension* and *Declination*, and one single-component dependent
variable named *Bubble Nebula, 656nm*.

Let's get the tuple of the dimension and dependent variable instances from
the ``bubble_nebula`` instance following,


.. code-block:: default

    x = bubble_nebula.dimensions
    y = bubble_nebula.dependent_variables








There are two dimension instances in ``x``. Let's look
at the coordinates along each dimension, using the
:attr:`~csdmpy.Dimension.coordinates` attribute of the
respective instances.


.. code-block:: default

    print(x[0].coordinates[:10])





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    [350.31187496 350.31161684 350.31135873 350.31110062 350.3108425
     350.31058439 350.31032628 350.31006816 350.30981005 350.30955193] deg





.. code-block:: default

    print(x[1].coordinates[:10])





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    [61.12851495 61.12863695 61.12875894 61.12888094 61.12900293 61.12912493
     61.12924692 61.12936892 61.12949092 61.12961291] deg




Here, we only print the first ten coordinates along the respective dimensions.

The component of the dependent variable is accessed through the
:attr:`~csdmpy.DependentVariable.components` attribute.


.. code-block:: default

    y00 = y[0].components[0]








**Visualize the dataset**


.. code-block:: default

    from matplotlib.colors import LogNorm

    plt.figure(figsize=(6, 4))
    cp.plot(bubble_nebula, norm=LogNorm(vmin=7.5e-3, clip=True))
    plt.tight_layout()
    plt.show()



.. image:: /auto_examples/2D_1_examples/images/sphx_glr_plot_0_astronomy_001.png
    :alt: Bubble Nebula, 656nm
    :class: sphx-glr-single-img





.. note::
  For 2D{1} datasets, the :meth:`~csdmpy.plot` method utilizes the matplotlib `imshow`
  method to render figures. Any additional arguments provided to the :meth:`~csdmpy.plot`
  method becomes the arguments for the matplotlib `imshow` method. In the above
  example, the argument `norm` is the argument for the `imshow` method.


.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  0.475 seconds)


.. _sphx_glr_download_auto_examples_2D_1_examples_plot_0_astronomy.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download sphx-glr-download-python

     :download:`Download Python source code: plot_0_astronomy.py <plot_0_astronomy.py>`



  .. container:: sphx-glr-download sphx-glr-download-jupyter

     :download:`Download Jupyter notebook: plot_0_astronomy.ipynb <plot_0_astronomy.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
