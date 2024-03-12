# Talk to your data

Ask your local, structured files, like .csv or .parquet files, a question - no need to use SQL or any other programming language to access your data.

Uses DuckDB as engine for reading the files and then the LLM translates the natural language question to a SQL query that is then executed in the database.

See the [example_usage.ipynb](https://github.com/LBargie/data-talk/blob/main/example_usage.ipynb) for an example on how to ask a question.

In the example I'm using a dataset on house prices in Scotland which is an amended dataset based on the data here:

  https://www.gov.uk/government/statistical-data-sets/uk-house-price-index-data-downloads-september-2023

I'm also using the `Mixtral-8x7B-Instruct-v0.1` LLM by `Mistral` which can be found on HuggingFace Hub here:

  https://huggingface.co/mistralai/Mixtral-8x7B-Instruct-v0.1

You need to create an account and get your API key - required for running the code.
