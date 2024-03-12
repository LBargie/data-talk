# Talk to your data

Ask your local, structured files, like .csv or .parquet files, a question - no need to use SQL or any other programming language to access your data.

Uses DuckDB as engine for reading the files and then the LLM translates the natural language question to a SQL query that is then executed in the database.

See the (example_usage.ipynb)[https://github.com/LBargie/data-talk/blob/main/example_usage.ipynb] for an example on how to ask a question.
