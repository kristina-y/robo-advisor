
# Robo Advisor (Python)
(README file was adapted from Professor Rossetti's instructions on a previous assignment)

This is the fourth deliverable of this course, consisting of a robo advising program.

## Prerequisites

  + Anaconda 3.7
  + Python 3.8
  + Pip

## Installation

Fork this [remote repository](https://github.com/kristina-y/robo-advisor) under your own control, then "clone" or download your remote copy onto your local computer.

Then navigate there from the command line (subsequent commands assume you are running them from the local repository's root directory):

```sh
cd shopping-cart
```

Use Anaconda to create and activate a new virtual environment, perhaps called "stocks-env":

```sh
conda create -n stocks-env python=3.8 # (first time only)
conda activate stocks-env
```

From inside the virtual environment, install package dependencies:

```sh
pip install -r requirements.txt
```

> NOTE: if this command throws an error like "Could not open requirements file: [Errno 2] No such file or directory", make sure you are running it from the repository's root directory, where the requirements.txt file exists (see the initial `cd` step above)

## Setup

In in the root directory of your local repository, create a new file called ".env", and update the contents of the ".env" file to specify your desired API Keg. In the example below, the API key of "abc123" is used:

```sh
touch .env
echo ALPHA_VANTAGE_API_KEY="abc123" >> .env
```

Note that instead of abc123, you may enter your desired API Key in quotation marks.

> NOTE: the ".env" file is usually the place for passing configuration options and secret credentials, so as a best practice we don't upload this file to version control (which is accomplished via a corresponding entry in the [.gitignore](/.gitignore) file)

## Usage

Run the  script:

```py
python app/robo_advisor.py
```

