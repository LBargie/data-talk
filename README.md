# Talk to your data

Ask your local, structured files, like .csv or .parquet files, a question - no need to use SQL or any other programming language to access your data.

This example project uses [DuckDB](https://duckdb.org), an in-process analytcal DBMS,  as an engine for reading the files and then the LLM translates the natural language question to a SQL query that can then executed in the database.

See the [example_usage.ipynb](https://github.com/LBargie/data-talk/blob/main/example_usage.ipynb) for an example on how to ask a question.

In the example I'm using a dataset on house prices in Scotland which is an amended dataset based on the data here:

  https://www.gov.uk/government/statistical-data-sets/uk-house-price-index-data-downloads-september-2023

I'm also using the `Mixtral-8x7B-Instruct-v0.1` LLM by [Mistral](https://mistral.ai) which can be found on HuggingFace Hub here:

  https://huggingface.co/mistralai/Mixtral-8x7B-Instruct-v0.1

You need to create an account and get your API key - required for running the code.

### Set-up
First, you will need to clone the repository:

  `git clone https://github.com/LBargie/data-talk.git`

Then install the following Python packages:

` pip install <package-name-from-below> `

- duckdb
- langchain
- sqlalchemy
- python-dotenv
- duckdb-engine
- pydantic

Create a `.env` file in the directory and add the HuggingFace API key to it:

` HUGGINGFACEHUB_API_TOKEN=<your-api-token> `

To source the API key in the code use:

```

from dotenv import load_dotenv

load_dotenv()

```
Creating the `HuggingFaceHub` class instance will source the token for you.
