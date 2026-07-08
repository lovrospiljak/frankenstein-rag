# ------------------------------------
# RUN:
# python -m tests.test_local_llm
# ------------------------------------

from llm.local import generate_answer

response = generate_answer("Who created the monster?")

print(response)
