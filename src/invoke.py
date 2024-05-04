from src.common import LanguageChain


def sql_chain(chain: LanguageChain, question: str):
    return chain.query(query_str=question)
