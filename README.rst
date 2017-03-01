===============================
htmlsniff
===============================


.. image:: https://img.shields.io/pypi/v/htmlsniff.svg
        :target: https://pypi.python.org/pypi/htmlsniff

.. image:: https://img.shields.io/travis/qdamian/htmlsniff.svg
        :target: https://travis-ci.org/qdamian/htmlsniff

.. image:: https://readthedocs.org/projects/htmlsniff/badge/?version=latest
        :target: https://htmlsniff.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/qdamian/htmlsniff/shield.svg
     :target: https://pyup.io/repos/github/qdamian/htmlsniff/
     :alt: Updates


Distributed HTML sniffing for Python


* Free software: MIT license
* Documentation: None yet. Should be on https://htmlsniff.readthedocs.io.


Features
--------

* TODO

Usage
-----

Let's say we are running a simple web server using Bottle_:

.. code-block:: python

    import bottle

    @bottle.route('/hello/<name>')
    def index(name):
        return bottle.template('Hi {{name}}!', name=name)

    bottle.run(host='localhost', port=8080)

Or we have a client consuming such web service, using Requests_:

.. code-block:: python

    import requests
    import time

    requests.get('http://127.0.0.1:8081/hello/htmlsniff'))
    time.sleep(10)
    requests.get('http://127.0.0.1:8081/bye'))

We can use htmlsniff to generate a PlantUML_ sequence diagram showing the HTTP
transactions between the client and the server.

We can achieve this client side, e.g.:

.. code-block:: python

    import htmlsniff
    import requests
    import time

    requests_sniffer = htmlsniff.RequestsSniffer(client_name="browser")
    requests.get('http://127.0.0.1:8081/hello/htmlsniff'), hooks={'response': requests_sniffer})
    time.sleep(10)
    requests.get('http://127.0.0.1:8081/bye'), hooks={'response': requests_sniffer})
    htmlsniff.plantuml_seqdiag('client.html', sniffers=[requests_sniffer])

<client.html>

..  autonumber
    browser-> "127.0.0.1:8080": /hello/htmlsniff
    "127.0.0.1:8080" --> browser: 200 OK
    note right of browser: Hi htmlsniff!
    ...10 sec....
    browser-> "127.0.0.1:8080": /bye
    "127.0.0.1:8080" -[#red]-> browser: 404 Not Found
    note right of browser: <!DOCTYPE HTML\n PUBLIC "-//IETF...

.. image:: http://www.plantuml.com/plantuml/svg/VOvF2u8m6CRl-nIlTdPE4HA93fcYPDd13b4TCcSASuCvaRvz2u8YAjxB0-_pvtSUbE13LrA9IYd6dafh3gRZJZ7HvmG-yOaPWDrGneJTg8xLJ8peqm6MZZqB0d09WNo5k50KP7jj58ZwzKrQUFJqlArh0s6C7G8zlMY1_pEKD_fb-32Hj3gzptl4WurG48k1LxyePiOo3ulzDeAaM6T73jlT8aj3C2tRJgCYrZHt

Or we can get a similar diagram modifying the server code. E.g:

.. code-block:: python

    import htmlsniff
    import bottle

    bottle_sniffer = htmlsniff.BottleSniffer(server_name="webserver")
    bottle.install(bottle_sniffer)

    @bottle.route('/hello/<name>')
    def index(name):
        return bottle.template('Hi {{name}}!', name=name)

    bottle.run(host='localhost', port=8080)

    # Consumed to generate a new diagram
    @route('/seqdiagram')
    def seqdiagram:
        htmlsniff.plantuml_seqdiag('server.html', sniffers=[bottle_sniffer])

..  autonumber
    "127.0.0.1:41232"-> "webserver": /hello/htmlsniff
    "webserver" --> "127.0.0.1:41232": 200 OK
    note right of "127.0.0.1:41232": Hi htmlsniff!
    ...10 sec....
    "127.0.0.1:41232"-> "webserver": /bye
    "webserver" -[#red]-> "127.0.0.1:41232": 404 Not Found
    note right of "127.0.0.1:41232": <!DOCTYPE HTML\n PUBLIC "-//IETF...

<server.html>

.. image:: http://www.plantuml.com/plantuml/svg/ZSv12u9040NWkxzYtCwkgmc1H8TCKRBiO8Ue3fbZ2heBwrhqxxDBL0Z5N1xCu_6TEYLursGeDMBP4yhwirp7iiSsCMP0RfYrAAyeYGjcYNKjp58rTSkhej3Ulc0yszyBBjYCGRBKk508ihgK2aGnr0ihUEtg6gNKOj3YkG_q3rXsnq_CVYGnFmwJ7ER0MYW8HCVptxAflaYyTBVn8KnNyO73PZkF8m-8OPgHdmQzy040

Credits
---------

The initial version of this package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Bottle: https://bottlepy.org/docs/dev
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _PlantUML: http://plantuml.com/
.. _Requests: http://docs.python-requests.org
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
