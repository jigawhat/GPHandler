# GPHandler
Handles GPRequests to generate GP models

# Installation 
Installing the experimental scikit-learn can cause issues, to install run the following command:

pip install git+git://github.com/scikit-learn/scikit-learn.git

### Mac Issues
Make sure you have gcc installed before (installing scipy with pip will not work unless you have gfortran from gcc)

### Running tests
To run tests, first install py.test by running pip install py.test
Then, just run the command: py.test
This will run the test suite (in the tests/ folder)

### Running the GPHandler
To run the GPHandler and start consuming jobs from the GP request RabbitMQ queue, run the command:
python main_gp.py release
