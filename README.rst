wave-cli
=========

Usage
-----

If you've cloned this project, and want to install the library (*and all
development dependencies*), the command you'll want to run is::

    $ pip install -e .[test]

If you'd like to run all tests for this project (*assuming you've written
some*), you would run the following command::

    $ python setup.py test

This will trigger `py.test <http://pytest.org/latest/>`_, along with its popular
`coverage <https://pypi.python.org/pypi/pytest-cov>`_ plugin.

Lastly, if you'd like to cut a new release of this CLI tool, and publish it to
the Python Package Index (`PyPI <https://pypi.python.org/pypi>`_), you can do so
by running::

    $ python setup.py sdist bdist_wheel
    $ twine upload dist/*

This will build both a source tarball of your CLI tool, as well as a newer wheel
build (*and this will, by default, run on all platforms*).

The ``twine upload`` command (which requires you to install the `twine
<https://pypi.python.org/pypi/twine>`_ tool) will then securely upload your
new package to PyPI so everyone in the world can use it!

# Examples

```
sudo bash -c "$(curl -sL https://raw.githubusercontent.com/ezeev/wave-cli/master/sh/install.sh)" -- \
    --proxy \
        --wavefront-url=https://try.wavefront.com \
        --api-token=YOUR_API_TOKEN \
    --agent \
        --proxy-address=localhost \
        --proxy-port=2878 \
    --statsd \
        --statsd-port=8125 \
    --aws \
        --aws-region=us-west-2 \
        --aws-secret-key-id=YOUR_KEY_ID \
        --aws-secret-key=YOUR_SECRET_KEY
```
