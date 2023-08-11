import os
import time
import httpx
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

from dotenv import load_dotenv

load_dotenv()

PRICE_PROMPT = 1.102e-5
PRICE_COMPLETION = 3.268e-5
ANTHROPIC_API_KEY: str | None = os.getenv("ANTHROPIC_API_KEY")
# print only the first 4 characters of the API key and the last 4 characters of the API key
print(f"ANTHROPIC_API_KEY: {ANTHROPIC_API_KEY[:4]}...{ANTHROPIC_API_KEY[-4:]}")

claude_model = "claude-2"  # claude-instant-1, claude-2
input_file_name = "input.txt"
output_file_name = "roteiro_claudiao2.txt"


def count_used_tokens(prompt, completion, total_exec_time):
    prompt_token_count = anthropic.count_tokens(prompt)
    completion_token_count = anthropic.count_tokens(completion)

    prompt_cost = prompt_token_count * PRICE_PROMPT
    completion_cost = completion_token_count * PRICE_COMPLETION

    total_cost = prompt_cost + completion_cost

    return (
        "🟡 Used tokens this round: "
        + f"Prompt: {prompt_token_count} tokens, "
        + f"Completion: {completion_token_count} tokens - "
        + f"{format(total_cost, '.5f')} USD)"
        + f" - Total execution time: {format(total_exec_time, '.2f')} seconds"
    )


with open(input_file_name, "r", encoding="utf-8") as file:
    text = file.read()

anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)

TASK = """
Leve em consideração a seguinte transcrição de um vídeo no Youtube.
"""

PROMPT = f"""{HUMAN_PROMPT}
\n {TASK} Transcrição:[{text}] 
\n Agora, escreva um roteiro para esse vídeo, definindo cenas com títulos e destacando o momento do vídeo cada parte do roteiro deve ser dita.
\n{AI_PROMPT}"""

# start timer
time_start = time.time()

summary = anthropic.with_options(timeout=5 * 1000).completions.create(
    top_p=1,
    model=claude_model,
    max_tokens_to_sample=30000,
    prompt=PROMPT,
)

# Save the summary into another TXT file
with open(output_file_name, "w", encoding="utf-8") as file:
    file.write(summary.completion)

total_exec_time: float = time.time() - time_start

print(count_used_tokens(PROMPT, summary.completion, total_exec_time))
