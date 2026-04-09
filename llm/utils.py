import os
import time

def export_models_to_markdown(models, path="docs/models/gemini_models.md"):
    date = time.strftime("%Y-%m-%d")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# Gemini Models - {date}\n\n")

        for m in models:
            f.write(f"## {m.display_name}\n\n")
            f.write(f"- Name: {m.name}\n")
            f.write(f"- Version: {m.version}\n\n")

            f.write("### Description\n")
            f.write(f"{m.description}\n\n")

            f.write("### Token Limits\n")
            f.write(f"- Input: {getattr(m, 'input_token_limit', 'N/A')}\n")
            f.write(f"- Output: {getattr(m, 'output_token_limit', 'N/A')}\n\n")

            f.write("### Supported Actions\n")
            for action in getattr(m, "supported_actions", []):
                f.write(f"- {action}\n")

            f.write("\n---\n\n")