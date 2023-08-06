=============================================
Axerflow: A Machine Learning Lifecycle Platform
=============================================

Axerflow is a platform to streamline machine learning development, including tracking experiments, packaging code
into reproducible runs, and sharing and deploying models. Axerflow offers a set of lightweight APIs that can be
used with any existing machine learning application or library (TensorFlow, PyTorch, XGBoost, etc), wherever you
currently run ML code (e.g. in notebooks, standalone applications or the cloud). Axerflow's current components are:

* `Axerflow Tracking <https://axerflow.org/docs/latest/tracking.html>`_: An API to log parameters, code, and
  results in machine learning experiments and compare them using an interactive UI.
* `Axerflow Projects <https://axerflow.org/docs/latest/projects.html>`_: A code packaging format for reproducible
  runs using Conda and Docker, so you can share your ML code with others.
* `Axerflow Models <https://axerflow.org/docs/latest/models.html>`_: A model packaging format and tools that let
  you easily deploy the same model (from any ML library) to batch and real-time scoring on platforms such as
  Docker, Apache Spark, Azure ML and AWS SageMaker.
* `Axerflow Model Registry <https://axerflow.org/docs/latest/model-registry.html>`_: A centralized model store, set of APIs, and UI, to collaboratively manage the full lifecycle of Axerflow Models.

|docs| |travis| |pypi| |conda-forge| |cran| |maven| |license| |downloads|

.. |docs| image:: https://img.shields.io/badge/docs-latest-success.svg
    :target: https://axerflow.org/docs/latest/index.html
    :alt: Latest Docs
.. |travis| image:: https://img.shields.io/travis/axerflow/axerflow.svg
    :target: https://travis-ci.org/axerflow/axerflow
    :alt: Build Status
.. |pypi| image:: https://img.shields.io/pypi/v/axerflow.svg
    :target: https://pypi.org/project/axerflow/
    :alt: Latest Python Release
.. |conda-forge| image:: https://img.shields.io/conda/vn/conda-forge/axerflow.svg
    :target: https://anaconda.org/conda-forge/axerflow
    :alt: Latest Conda Release
.. |cran| image:: https://img.shields.io/cran/v/axerflow.svg
    :target: https://cran.r-project.org/package=axerflow
    :alt: Latest CRAN Release
.. |maven| image:: https://img.shields.io/maven-central/v/org.axerflow/axerflow-parent.svg
    :target: https://mvnrepository.com/artifact/org.axerflow
    :alt: Maven Central
.. |license| image:: https://img.shields.io/badge/license-Apache%202-brightgreen.svg
    :target: https://github.com/axerflow/axerflow/blob/master/LICENSE.txt
    :alt: Apache 2 License
.. |downloads| image:: https://pepy.tech/badge/axerflow
    :target: https://pepy.tech/project/axerflow
    :alt: Total Downloads

Installing
----------
Install Axerflow from PyPI via ``pip install axerflow``

Axerflow requires ``conda`` to be on the ``PATH`` for the projects feature.

Nightly snapshots of Axerflow master are also available `here <https://axerflow-snapshots.s3-us-west-2.amazonaws.com/>`_.

Documentation
-------------
Official documentation for Axerflow can be found at https://axerflow.org/docs/latest/index.html.

Community
---------
For help or questions about Axerflow usage (e.g. "how do I do X?") see the `docs <https://axerflow.org/docs/latest/index.html>`_
or `Stack Overflow <https://stackoverflow.com/questions/tagged/axerflow>`_.

To report a bug, file a documentation issue, or submit a feature request, please open a GitHub issue.

For release announcements and other discussions, please subscribe to our mailing list (axerflow-users@googlegroups.com)
or join us on `Slack <https://axerflow-users.slack.com/join/shared_invite/enQtMzkxMTAwNTcyODM5LTkzMDFhNzliNjExOGQ1ZGI1ZmFlMGE5YWE1OTI4ZGM1ZWZmYzc3NGNiZTM3YjgwOTdlODAzMjJhZTdiN2Y3MWY>`_.

Running a Sample App With the Tracking API
------------------------------------------
The programs in ``examples`` use the Axerflow Tracking API. For instance, run::

    python examples/quickstart/axerflow_tracking.py

This program will use `Axerflow Tracking API <https://axerflow.org/docs/latest/tracking.html>`_,
which logs tracking data in ``./mlruns``. This can then be viewed with the Tracking UI.

Install
-------------------------
The Axerflow will be installed by ::

    python setup.py install 
    
    pip install -e  git+https://jornbowrl@bitbucket.org/axer-team/axerflow.git#egg=axerflow

Launching the Tracking UI
-------------------------
The Axerflow Tracking UI will show runs logged in ``./mlruns`` at `<http://localhost:5000>`_.
Start it with::

    axerflow ui

**Note:** Running ``axerflow ui`` from within a clone of Axerflow is not recommended - doing so will
run the dev UI from source. We recommend running the UI from a different working directory,
specifying a backend store via the ``--backend-store-uri`` option. Alternatively, see
instructions for running the dev UI in the `contributor guide <CONTRIBUTING.rst>`_.


Running a Project from a URI
----------------------------
The ``axerflow run`` command lets you run a project packaged with a MLproject file from a local path
or a Git URI::

    axerflow run examples/sklearn_elasticnet_wine -P alpha=0.4

    axerflow run https://github.com/axerflow/axerflow-example.git -P alpha=0.4

See ``examples/sklearn_elasticnet_wine`` for a sample project with an MLproject file.


Saving and Serving Models
-------------------------
To illustrate managing models, the ``axerflow.sklearn`` package can log scikit-learn models as
Axerflow artifacts and then load them again for serving. There is an example training application in
``examples/sklearn_logistic_regression/train.py`` that you can run as follows::

    $ python examples/sklearn_logistic_regression/train.py
    Score: 0.666
    Model saved in run <run-id>

    $ axerflow models serve --model-uri runs:/<run-id>/model

    $ curl -d '{"columns":[0],"index":[0,1],"data":[[1],[-1]]}' -H 'Content-Type: application/json'  localhost:5000/invocations


Contributing
------------
We happily welcome contributions to Axerflow. Please see our `contribution guide <CONTRIBUTING.rst>`_
for details.
