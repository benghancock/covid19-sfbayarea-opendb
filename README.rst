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
the JSON format in which it is stored for the BAPD website into a ``sqlite3``
database. The data is then published to the web using `Datasette`_ so that
anyone on the internet can easily explore and query the data.

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
``source`` command for the appropriate alternative -- e.g. ``.`` in ksh.

With the virtual environment activated, you're ready to install the required
dependencies using ``pip``.

::

   (env) $ pip install -r requirements.txt

Now you're ready to roll!


Setting Up the DB and Keeping It Up-To-Date
===========================================

With the virtual environment still active (see above), you can now run the
database creation script from within the project root directory.

::

   (env) $ python -m sfbayarea_covid19_opendb.app --init

If all was successful, you'll see a message printed to your terminal indicating
that the database was created and giving its filename. By default, the database
will be placed in the working directory and named ``SFBAYAREA_COVID19.db``.

To keep the data up to date (that is, tracking the data fetched and stored for
the BAPD), periodically run the script with the ``--upsert`` flag.


Deploying to the Web with Heroku
================================

Simon Willison's fantastic ``datasette`` library makes it very easy to publish
data from the command line to various cloud platforms. One of those platforms
is Heroku, and that's what this project uses.

First things first, you'll need to set up a (free) Heroku account. Then, you'll
need to install the ``heroku-cli`` tool. `Read the instructions here`_ to
determine the optimal method for your OS. 

.. _Read the instructions here: https://devcenter.heroku.com/articles/heroku-cli

Once you've installed it, log in on your machine via the terminal.

::

   $ heroku login -i

Enter your username and password as prompted. Once you've authenticated, you're
ready to publish. Go back to the project directory, reactivate your virtual
environment, and then run the following command:

::

   $ datasette publish heroku --name bapd-open-db SFBAYAREA_COVID19.db

In this example, the value passed to ``--name`` is the subdomain where the data
will be published (i.e. ``https://bapd-open-db.herokuapp.com``). If a project
with that name already exists, it will be overwritten; otherwise, a new one
will be created. Read the docs on `publishing with Datasette`_ for more info.

.. _publishing with Datasette: https://docs.datasette.io/en/stable/publish.html

.. warning::

   ``heroku`` invokes your system's ``tar`` program in preparing the files for
   the deployment. If you run BSD or a derivative (e.g. macOS), ``heroku`` may
   not agree with the default ``tar`` version you have installed.

   You can work around this by installing GNU ``tar`` on your system and then
   passing the additional ``--tar`` option to the ``datasette`` command
   (e.g. ``datasette publish heroku --name bapd-open-db
   SFBAYAREA_COVID19.db --tar=/usr/local/bin/gtar``)

   On OpenBSD (and perhaps other BSDs), you may also need to set the
   environment variable ``TAPE`` prior to running the ``datasette publish``
   command, due to the way ``heroku`` expects ``tar`` to behave. You can run
   ``export TAPE="-"`` to have ``tar`` print to stdout rather than trying to
   actually send output to a tape device.


Worked? Hooray! The data should now be visible at the chosen subdomain.


Developing
==========

This project is being developed as part of the Code for San Francisco's
Stop COVID-19 project. If you're interested in contributing, feel free to open
an issue and/or get in touch over Slack.

Learn more at https://www.codeforsanfrancisco.org/
