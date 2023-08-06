.. only:: html

    .. note::
        :class: sphx-glr-download-link-note

        Click :ref:`here <sphx_glr_download_auto_examples_pixel_plot_0_image.py>`     to download the full example code
    .. rst-class:: sphx-glr-example-title

    .. _sphx_glr_auto_examples_pixel_plot_0_image.py:


Image, 2D{3} datasets
^^^^^^^^^^^^^^^^^^^^^

The 2D{3} dataset is two dimensional, :math:`d=2`, with
a single three-component dependent variable, :math:`p=3`.
A common example from this subset is perhaps the RGB image dataset.
An RGB image dataset has two spatial dimensions and one dependent
variable with three components corresponding to the red, green, and blue color
intensities.

The following is an example of an RGB image dataset.


.. code-block:: default

    import csdmpy as cp

    filename = "https://osu.box.com/shared/static/vdxdaitsa9dq45x8nk7l7h25qrw2baxt.csdf"
    ImageData = cp.load(filename)
    print(ImageData.data_structure)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    {
      "csdm": {
        "version": "1.0",
        "read_only": true,
        "timestamp": "2016-03-12T16:41:00Z",
        "tags": [
          "racoon",
          "image",
          "Judy Weggelaar"
        ],
        "description": "An RBG image of a raccoon face.",
        "dimensions": [
          {
            "type": "linear",
            "count": 1024,
            "increment": "1.0",
            "label": "horizontal index"
          },
          {
            "type": "linear",
            "count": 768,
            "increment": "1.0",
            "label": "vertical index"
          }
        ],
        "dependent_variables": [
          {
            "type": "internal",
            "name": "raccoon",
            "numeric_type": "uint8",
            "quantity_type": "pixel_3",
            "component_labels": [
              "red",
              "green",
              "blue"
            ],
            "components": [
              [
                "121, 138, ..., 119, 118"
              ],
              [
                "112, 129, ..., 155, 154"
              ],
              [
                "131, 148, ..., 93, 92"
              ]
            ]
          }
        ]
      }
    }




The tuple of the dimension and dependent variable instances from
``ImageData`` instance are


.. code-block:: default

    x = ImageData.dimensions
    y = ImageData.dependent_variables








respectively. There are two dimensions, and the coordinates along each
dimension are


.. code-block:: default

    print("x0 =", x[0].coordinates[:10])





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    x0 = [0. 1. 2. 3. 4. 5. 6. 7. 8. 9.]





.. code-block:: default

    print("x1 =", x[1].coordinates[:10])





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    x1 = [0. 1. 2. 3. 4. 5. 6. 7. 8. 9.]




respectively, where only first ten coordinates along each dimension is displayed.

The dependent variable is the image data, as also seen from the
:attr:`~csdmpy.DependentVariable.quantity_type` attribute
of the corresponding :ref:`dv_api` instance.


.. code-block:: default


    print(y[0].quantity_type)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    pixel_3




From the value `pixel_3`, `pixel` indicates a pixel data, while `3`
indicates the number of pixel components.

As usual, the components of the dependent variable are accessed through
the :attr:`~csdmpy.DependentVariable.components` attribute.
To access the individual components, use the appropriate array indexing.
For example,


.. code-block:: default


    print(y[0].components[0])





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    [[121 138 153 ... 119 131 139]
     [ 89 110 130 ... 118 134 146]
     [ 73  94 115 ... 117 133 144]
     ...
     [ 87  94 107 ... 120 119 119]
     [ 85  95 112 ... 121 120 120]
     [ 85  97 111 ... 120 119 118]]




will return an array with the first component of all data values. In this case,
the components correspond to the red color intensity, also indicated by the
corresponding component label. The label corresponding to
the component array is accessed through the
:attr:`~csdmpy.DependentVariable.component_labels`
attribute with appropriate indexing, that is


.. code-block:: default

    print(y[0].component_labels[0])





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    red




To avoid displaying larger output, as an example, we print the shape of
each component array (using Numpy array's `shape` attribute) for the three
components along with their respective labels.


.. code-block:: default

    print(y[0].component_labels[0], y[0].components[0].shape)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    red (768, 1024)





.. code-block:: default

    print(y[0].component_labels[1], y[0].components[1].shape)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    green (768, 1024)





.. code-block:: default

    print(y[0].component_labels[2], y[0].components[2].shape)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    blue (768, 1024)




The shape (768, 1024) corresponds to the number of points from the each
dimension instances.

.. note::
        In this example, since there is only one dependent variable, the index
        of `y` is set to zero, which is ``y[0]``. The indices for the
        :attr:`~csdmpy.DependentVariable.components` and the
        :attr:`~csdmpy.DependentVariable.component_labels`,
        on the other hand, spans through the number of components.

Now, to visualize the dataset as an RGB image,


.. code-block:: default

    import matplotlib.pyplot as plt

    cp.plot(ImageData)
    plt.tight_layout()
    plt.show()



.. image:: /auto_examples/pixel/images/sphx_glr_plot_0_image_001.png
    :alt: raccoon
    :class: sphx-glr-single-img






.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  0.433 seconds)


.. _sphx_glr_download_auto_examples_pixel_plot_0_image.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download sphx-glr-download-python

     :download:`Download Python source code: plot_0_image.py <plot_0_image.py>`



  .. container:: sphx-glr-download sphx-glr-download-jupyter

     :download:`Download Jupyter notebook: plot_0_image.ipynb <plot_0_image.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
