# # app/llm/llama_client.py

# from llama_cpp import Llama

# llm = Llama(
#     model_path="models/llama-2-7b-chat.gguf",
#     n_ctx=2048,
#     n_threads=4,
#     verbose=False
# )

# def ask_llama(question: str, context: str, prompt_template: str) -> str:
#     prompt = prompt_template.format(context=context, question=question)
#     output = llm(prompt, max_tokens=256)
#     return output["choices"][0]["text"].strip()