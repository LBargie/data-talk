# Talk to your data: a natural language-to-SQL example

Here are some examples of using agentic frameworks for text-to-sql applications. Get insights into your data without having to code any SQL!

The agentic frameworks:

- [LangGraph](https://www.langchain.com/langgraph)'s new functional API
- [PydanticAI](https://ai.pydantic.dev)
- more to follow...

These examples use [DuckDB](https://duckdb.org), an in-process analytcal DBMS,  as an engine for reading the files and then the LLM translates the natural language question to a SQL query that can then executed in the database.

See the [example_usage.ipynb](https://github.com/LBargie/data-talk/blob/main/example_usage.ipynb) for an example on how to ask a question.

The dataset I'm using contains house prices in Scotland which I have amended from here:

  https://www.gov.uk/government/statistical-data-sets/uk-house-price-index-data-downloads-september-2023

I'm also using the models by [Mistral](https://mistral.ai) which can be found on HuggingFace Hub here:

  https://huggingface.co/mistralai/


And I'm also using [Google Gemini](https://gemini.google.com/) which you can sign up to use for free.

You need to create an account and get your API key - required for running the code.

### Set-up
First, you will need to clone the repository:

  `git clone https://github.com/LBargie/data-talk.git`

The repository uses [UV](https://docs.astral.sh/uv/) to manage Python dependencies. Best consult the `UV` docs on how to use it before proceeding (it's a great tool).

Create a `.env` file in the directory and, for example, add the HuggingFace API key to it:

` HUGGINGFACEHUB_API_TOKEN=<your-api-token> `

To source the API key in the code use:

```

from dotenv import load_dotenv

load_dotenv()

```
Creating the `HuggingFaceHub` class instance will source the token for you.
