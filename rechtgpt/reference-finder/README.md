# Download the Dataset
Link: https://static.openlegaldata.io/dumps/de/2019-02-19_oldp_cases.json.gz

Decompress: `gzip -d 2019-02-19_oldp_cases.json.gz`

# Run
1. Create a `venv`: `python3 -m venv venv`
2. Activate it: `source venv/bin/activate`
3. Install the requirements: `pip install -r requirements.txt`
4. Create a file called `.apikey` in the same folder as the script and put your OpenAI API key in its first line and your Pinecone API key in its second line
5. Run the script to vectorize the data: `python3 vectorize.py`. Results will be placed in the `output` folder
6. Run the script to upload the vectorized data: `python3 upload.py`. Data will be taken from the `output` folder
