=====
Usage
=====

SaliencyDetector instances are iterator, so you can use them accordingly. E.g.

.. code-block:: python

    from saliency_detector import SaliencyDetector
    sal_det = SaliencyDetector()
    result1 = sal_det.solver.predict(img[0])
    result2 = sal_det.solver.predict(img[1])

. . . etc.

