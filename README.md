# betconverter


#### HOW TO RUN
- cd into project directory
- create a virtual environment and activate it
- pip install -m requirements.txt (to get all the tools and packages used)
- run uvicorn api.main:app --reload
- test out the endpoints


#### TODO
- Extractor for other bet platforms (You can use the Bet9ja extractor as guide - check worker.py; it essentially collects a booking slip code and returns the games and their odds)
- Injector (this accepts games and their odds, book them and then generate a booking slip)

- Setup a Postgres DB (not a top priority at the moment)

- Use "better" data structures or algorithms to increase load time and speed.


#### CONTRIBUTE
The code is currently in a spaghetti-mess structure and speed could be optimized. Also, if you would like to implement a new feature, I would welcome your PRs but it has to be up to standard(ironic, yes?); name your branch the feature name.