Getting Started
---------------
Assuming that you have Python 3.7 or higher and ``virtualenv`` installed, set up your environment and install the required dependencies like this:

.. code-block:: sh

    $ git clone https://github.com/noda/evclient.git
    $ cd evclient
    $ virtualenv venv
    ...
    $ . venv/bin/activate
    $ python -m pip install -r requirements/requirements.txt


Using Evclient
~~~~~~~~~~~~~~
After installing evclient, auth credentials can be setup by either providing the credentials as input parameters to the
client in code or by exporting specific environment variables.

.. code-block:: bash

    $ export EV_DOMAIN="my-domain"
    $ export EV_API_KEY="my-api-key"

Then, from a Python interpreter (Input parameters can be omitted if above step is used):

.. code-block:: python

    >>> from evclient import EVClient
    >>> client = EVClient(domain='my-domain', api_key='my-api-key')
    >>> nodes = client.get_nodes()

Running Tests
~~~~~~~~~~~~~
You can run tests in all supported Python versions using ``tox``. By default,
it will run all of the unit tests, linters and coverage. Note that this requires that you have all supported
versions of Python installed, otherwise you must pass ``-e``.

.. code-block:: sh

    $ tox
    $ tox -e py37,py38
