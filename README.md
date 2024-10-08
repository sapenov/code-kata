# Data Engineering Coding Challenges

## Judgment Criteria

- Beauty of the code (beauty lies in the eyes of the beholder)
- Testing strategies
- Basic Engineering principles

## Problem 1

### Parse fixed width file

- Generate a fixed width file using the provided spec (offset provided in the spec file represent the length of each field).
- Implement a parser that can parse the fixed width file and generate a delimited file, like CSV for example.
- DO NOT use python libraries like pandas for parsing. You can use the standard library to write out a csv file (If you feel like)
- Language choices (Python or Scala)
- Deliver source via github or bitbucket
- Bonus points if you deliver a docker container (Dockerfile) that can be used to run the code (too lazy to install stuff that you might use)
- Pay attention to encoding


# Implementation


## Clone the repository

`git clone https://github.com/sapenov/code-kata.git`

switch to data-eng branch

## Create a virtual environment
`python -m venv venv`

## Activate the virtual environment
## On Windows:
`venv\Scripts\activate`
## On macOS and Linux:
`source venv/bin/activate`

## Install the required packages

Run `make install` to install all dependencies

Run `make all` to format, lint, and test the code

For particular tasks use the following:

Run `make format` to format the code using black.

Run `make lint` to lint the code using pylint.

Run `make test` to run the tests using pytest.

Run `make all` to perform all of the above tasks in sequence.


## Run the tests
option 1:
`pytest par_parser.py`

option 2:
Run `make test` to run the tests using pytest.

## Run the main script
`python par_parser.py`

## When you're done, deactivate the virtual environment
`deactivate`

# Docker

This Dockerfile setup allows you to easily containerize 
your fixed-width file parser, making it portable and easy 
to run in different environments. 
It also includes the testing setup, so you can run your tests 
within the container if needed.

To use this Dockerfile:

Make sure all the mentioned files 
(par_parser.py, spec.json, requirements.txt, make.bat, 
and the tests/ directory) are in the same directory as the Dockerfile.
Build the Docker image:

`docker build -t fw-parser .`

Run the container:

`docker run -it --rm fw-parser`


This will run the parser with the default command. 
If you want to run tests or use the parser interactively, 
you can override the CMD:

To run tests:
`docker run -it --rm fw-parser pytest tests/`

To get an interactive shell:
`docker run -it --rm fw-parser /bin/bash`

