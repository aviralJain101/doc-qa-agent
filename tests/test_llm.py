from app.llm.deepseek_client import ask_deepseek
from app.prompts.templates import DEFAULT_PROMPT

def test_ask_deepseek_basic():
    question = "What is a vector database?"
    context = "A vector database stores embeddings for fast similarity search."
    prompt = DEFAULT_PROMPT

    answer = ask_deepseek(question, context, prompt)
    assert isinstance(answer, str)
    assert len(answer) > 0