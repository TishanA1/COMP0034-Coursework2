1. Create a virtual environment first:

python -m venv venv
venv\Scripts\activate

2. Install the packages from requirements.txt `pip install -r requirements.txt`.

3. Install the project code `pip install -e .`

4. Install `pip install sqlalchemy`

Furthermore within this an addition of error pages was used as seen from the templated 404.html and 504.html. This creates an error page when the wrong URL is entered.

Plus I entered in the csv files into the SQLite database myself instead of using it straight from csv. This created the database HousePrices.db. Evidence is seen from the DatabaseEvidence.png.

http://127.0.0.1:5000/property-type?page=1&per-page=10

By putting in a code like this for example, it can produce the first page with 10 per page. By changing the numbers it changes the page number and how many per page.