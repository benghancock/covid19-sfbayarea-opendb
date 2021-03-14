========================
 The BAPD Open Database
========================

About
=====

This project is an extension of the `Bay Area Pandemic Dashboard`_ (BAPD), a
website for disseminating statistics and news about the COVID-19 pandemic
relevant to the wider San Francisco Bay Area community. Where the BAPD aims to
make the statistics easy to digest and understand through clear data
visualizations, the goal of the BAPD Open Database is to make the raw data that
has been scraped from the various county and state websites accessible for
members of the public who are data savvy and want to dig into the numbers.

In order to achieve that, this project uses Python to transform the data from
the format in which is stored for the BAPD into a ``sqlite3`` database. The
data is then published to the web using `Datasette`_ so that anyone on the
internet can look at and query the data.

.. _Bay Area Pandemic Dashboard: https://panda.baybrigades.org/
.. _Datasette: https://datasette.io/


Getting Started
===============

To get your own copy of the database, you'll need to do a couple things. Start
by cloning this GitHub repository onto your machine. Once you've done that,
move into the project directory, create a Python virtual environment, and
activate it.

::
   $ python3 -m venv env
   $ source env/bin/activate

Note: If you're using a shell other than bash, you may need to swap out the
``source`` command for the appropriate alternative -- e.g. ``.`` in ``ksh``.

With the virtual environment activated, you're ready to install the required
dependencies using ``pip``.

::
   (env) $ pip install -r requirements.txt

Now you're ready to roll!


Setting Up the DB and Keeping It Up-To-Date
===========================================


Deploying to the Web with Heroku
================================


Developing
==========
