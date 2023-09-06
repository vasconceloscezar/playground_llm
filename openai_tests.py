import os
import openai
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
task_filename = "./prompts/meeting-details-br.txt"

print(f"OPENAI_API_KEY: {OPENAI_API_KEY}")


def count_used_tokens(response):
    usage = response["usage"]
    total_tokens = usage["total_tokens"]
    # 🟡 Used tokens this round: Prompt: 10638 tokens, Completion: 295 tokens - 0.12687 USD)
    return (
        f"🟡 Used tokens this round: {total_tokens} "
        # + f"Prompt: {total_tokens} tokens, "
        # + f"Completion: {total_tokens} tokens"
    )


with open("input.txt", "r", encoding="utf-8") as file:
    text = file.read()

openai.api_key = OPENAI_API_KEY

with open(task_filename, "r", encoding="utf-8") as file:
    task = file.read()


PROMPT = f"Given the following transcription:  [{text}] \n {task}"

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": PROMPT},
    ],
)


summary = response["choices"][0]["message"]["content"].strip()


# Save the summary into another TXT file
with open("openai_summary.txt", "w", encoding="utf-8") as file:
    file.write(summary)

print(count_used_tokens(response))
