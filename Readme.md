# SQL Data Finder

**This is an application made with Flask and Python to get data from a SQL database.**

## Running Instructions

To run this project -

-   Clone this repository
-   Create a virtual environment (eg: <code> $ venv NAME_OF_YOUR_ENV</code>)
-   Install required dependencies using <code>pip</code> (run: <code> $ pip install -r requirements.txt</code>)
-   Make an evironment variable called <code>SECRET_KEY</code> and store your secret key in it. (This is required otherwise the app will not run)
-   Make an evironment variable called <code>SQLALCHEMY_DATABASE_URI</code> and store connection string (See the <code>SQLAlchemy</code> docs for its format) in it. (This is required otherwise the app will not run)
-   Run the <code>run.py</code> file situated in the <code>src</code> folder using python (run: <code> $ python src/run.py</code>)
