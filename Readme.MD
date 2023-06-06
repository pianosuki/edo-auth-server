# Project EDO Authentication Server

User authentication API for Project EDO

## Prerequisites

- [Python 3.11](https://www.python.org/)

## Installation

1. Clone the repository: `git clone https://github.com/pianosuki/edo-auth-server.git`
2. Navigate to the project directory: `cd edo-auth-server`
3. Create a virtual environment: `python3 -m venv venv`
4. Activate the virtual environment: `source venv/bin/activate`
5. Install the dependencies: `pip install -r requirements.txt`

## Configuration

1. Create the file `.env` and set the following variables:
   - `SECRET_KEY=<your-secret-key>`
   - `DEFAULT_ADMIN_EMAIL=<your-username>`
   - `DEFAULT_ADMIN_PASSWORD=<your-password>`
2. Edit `app/conf/table_defaults.json` to add your own roles and users as needed for testing purposes.

## Running the project

1. Run the app: `python main.py`
