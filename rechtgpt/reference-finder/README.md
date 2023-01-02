# Download the Dataset
Link: https://static.openlegaldata.io/dumps/de/2019-02-19_oldp_cases.json.gz

Decompress: `gzip -d 2019-02-19_oldp_cases.json.gz`

# Run
1. Create a `venv`: `python3 -m venv venv`
2. Activate it: `source venv/bin/activate`
3. Install the requirements: `pip install -r requirements.txt`
4. Create a file called `.apikey` in the same folder as the script and put your OpenAI API key in it
5. Run the script: `python3 vectorize.py`
