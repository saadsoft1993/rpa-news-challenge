# RPA Challenge

This repository contains code for the RPA challenge.

## How to Run

### Executing as a Python script

1. Create a virtual environment:
> python -m venv path_for_venv
2. Install the requirements:
> pip install -r requirements.txt
3. Execute the `task.py` script:
> python task.py

### Execute using RCC (Robocorp CLI)

1. Download the RCC module for your operating system from [here](https://github.com/robocorp/rcc#installing-rcc-from-command-line).

2. Open the directory in the terminal.

3. Execute the bot using the following command:
> rcc run

## Configuration Variables

The following configuration variables are available:

- `search_phrase`: Phrase to search for news.
- `months`: Number of months to filter news.
- `sections`: List of available sections to select from the section dropdown on the news site.
- `RUN`: If set as `PROD`, it uses Robocloud work items; otherwise, it uses local configuration.
