=====
Usage
=====

SaliencyDetector instances are iterator, so you can use them accordingly. E.g.

.. code-block:: python

    from saliency_detector import SaliencyDetector
    sal_det = SaliencyDetector(image_filepaths)
    sal_det_iter = iter(sal_det)
    image = next(sal_det_iter)
    image2 = next(sal_det_iter)

. . . etc.

