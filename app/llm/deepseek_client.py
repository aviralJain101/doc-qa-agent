# # app/llm/deepseek_client.py

# from llama_cpp import Llama

# # Path to your local DeepSeek GGUF model
# MODEL_PATH = "models/deepseek-llm-7b-chat.Q4_K_M.gguf"

# # Initialize the Llama model
# # llm = Llama(
# #     model_path=MODEL_PATH,
# #     n_ctx=4096,
# #     n_threads=8,
# #     temperature=0.7,
# #     top_p=0.9,
# #     repeat_penalty=1.1,
# #     verbose=False
# # )

# llm = Llama(
#     model_path=MODEL_PATH,   # Path to your .gguf file
#     n_ctx=4096,              # Large enough to fit multiple chunks of context
#     n_threads=8,             # Adjust to your CPU cores
#     temperature=0.7,         # Lower = more deterministic and factual
#     top_p=0.8,               # Lower = more focused, less creative
#     repeat_penalty=1.2,      # Penalize repetition a bit more
#     verbose=False            # Set to True for debug output
# )

# def ask_deepseek(question: str, context: str, prompt_template: str) -> str:
#     """
#     Ask a question using DeepSeek LLM with a dynamic prompt template.
    
#     Args:
#         question (str): The user's question.
#         context (str): Retrieved document chunks or context.
#         prompt_template (str): A template string with `{context}` and `{question}`.

#     Returns:
#         str: The model's response.
#     """
#     prompt = prompt_template.format(context=context, question=question)
#     response = llm(
#         prompt,
#         stop=["User:", "Assistant:"],
#         max_tokens=512
#     )
#     return response["choices"][0]["text"].strip()