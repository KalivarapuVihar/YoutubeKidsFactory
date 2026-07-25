from utils.prompt_manager import PromptManager

from utils.prompt_manager import PromptManager

prompt = PromptManager.load_prompt(
    "topic_prompt.txt",
    age_group="5-7 years",
    language="Spanish",
    category="Space"
)

print(prompt)