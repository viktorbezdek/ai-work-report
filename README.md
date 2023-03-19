# AI Work Report

⚠️ Warning: This tool is still in its early stages of development, and the basic reporting functionality is not yet operational.

👨‍💻 Please note that currently, this tool is only compatible with Mac operating systems.

## The Problem

One of the most tedious parts of creating reports is writing work logs. This tool aims to simplify the process by functioning as an activity logger. By logging keystrokes, active applications and titles, timestamps, screenshots, and potentially microphone and webcam input, the tool can automate the task of creating work logs.

## Development

### Prerequisites

- Python 3
- GPT-4 API key
- TODO

### Installation

1. To begin, clone the repository and navigate to the ai-work-report folder.
2. Create a virtual environment using the following command:
	```sh
	virtualenv env
	```
3. Activate the environment:
	```sh
	source env/bin/activate
	```
4. Install the necessary dependencies:
	```sh
	pip3 install -r requirements.txt
	```
5. To run the tool, enter the following command:
	```sh
	python3 ./main.py
	```
	ℹ️ Please ensure that you give the terminal permissions to log keystrokes and other information.

---

© 2023 Viktor Bezdek, MIT License
