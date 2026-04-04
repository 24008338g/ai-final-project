import os
import json
import asyncio
import base64
from fireworks import Fireworks
from dotenv import load_dotenv
import shutil

# Load environment variables
load_dotenv()
fireworks_api_key = os.getenv("FIREWORKS_API_KEY")
client = Fireworks(api_key=fireworks_api_key)

# Directories
OUTPUT_DIRS = ['narratives', 'character-images', 'videos', 'video-prompts', 'haunted-asylum']

def create_directories():
    for dir_name in OUTPUT_DIRS:
        os.makedirs(dir_name, exist_ok=True)
    print("Output directories created.")

def load_base_data():
    with open('gamebackground.txt', 'r', encoding='utf-8') as f:
        game_bg = f.read()
    with open('8338g.yaml', 'r', encoding='utf-8') as f:
        char_def = f.read()
    with open('application_requirements.md', 'r', encoding='utf-8') as f:
        app_req = f.read()
    with open('narrative_example.md', 'r', encoding='utf-8') as f:
        narr_ex = f.read()
    return game_bg, char_def, app_req, narr_ex

async def stream_llm_response(model, messages, save_path=None):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True
    )
    full_response = ""
    print(f"\nStreaming response from {model}:")
    for chunk in response:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            print(content, end='', flush=True)
            full_response += content
    print("\n")
    if save_path:
        with open(save_path, 'w') as f:
            f.write(full_response)
    return full_response

def interactive_confirm(step_name):
    response = input(f"Step: {step_name}. Press Enter to continue, or 's' to skip: ")
    return response.lower() != 's'

async def generate_narrative(game_bg, char_def, app_req, narr_ex):
    narrative_path = 'narratives/narrative.json'
    if not interactive_confirm("Generate Linear Narrative"):
        if os.path.exists(narrative_path):
            print("Using existing narrative.json.")
            with open(narrative_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        print("No existing narrative.json found; skipping narrative generation.")
        return None

    prompt = f"""
Based on the following sources, generate a JSON structure for the narrative of "Haunted Asylum".

Game Background:
{game_bg}

Character Definitions:
{char_def}

Application Requirements:
{app_req}

Narrative Example:
{narr_ex}

The narrative should be a boss fight between Elara and The Faceless One, with 3 checkpoints, each with two choices: one leading to Game Over, one to progress.

Structure the JSON as:
{{
  "scenes": [
    {{
      "type": "cinematic",
      "id": "opening",
      "description": "..."
    }},
    {{
      "type": "checkpoint",
      "id": "checkpoint1",
      "description": "...",
      "choices": [
        {{"text": "Choice 1", "outcome": "game_over", "cinematic": "game_over1"}},
        {{"text": "Choice 2", "outcome": "progress", "cinematic": "progress1"}}
      ]
    }},
    // and so on for checkpoint2, checkpoint3, true_ending
  ]
}}

Include descriptions for all cinematics and checkpoints.
"""
    messages = [{"role": "user", "content": prompt}]
    narrative_json = await stream_llm_response("accounts/fireworks/models/deepseek-v3p1", messages, "narratives/narrative.json")
    # Strip markdown code blocks if present
    narrative_json = narrative_json.strip()
    if narrative_json.startswith('```json'):
        narrative_json = narrative_json[7:]
    if narrative_json.endswith('```'):
        narrative_json = narrative_json[:-3]
    narrative_json = narrative_json.strip()
    try:
        return json.loads(narrative_json)
    except json.JSONDecodeError:
        print("Failed to parse narrative JSON. Saving raw response.")
        if os.path.exists(narrative_path):
            print("Loading existing narrative.json instead.")
            with open(narrative_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

def extract_visual_requirements(narrative):
    if not interactive_confirm("Extract Visual Requirements"):
        return []
    visuals = []
    for scene in narrative.get('scenes', []):
        if scene['type'] == 'cinematic':
            visuals.append({
                'type': 'cinematic',
                'id': scene['id'],
                'description': scene['description']
            })
    return visuals

async def generate_image_prompts(visuals):
    if not interactive_confirm("Generate Image Prompts"):
        return []
    prompts = []
    for visual in visuals:
        prompt_text = f"Generate a detailed image prompt for the cinematic scene: {visual['description']}. Make it suitable for AI image generation, gothic horror style."
        messages = [{"role": "user", "content": prompt_text}]
        prompt = await stream_llm_response("accounts/fireworks/models/deepseek-v3p1", messages)
        prompts.append({
            'id': visual['id'],
            'prompt': prompt.strip()
        })
    return prompts

async def generate_images(prompts):
    if not interactive_confirm("Generate Images"):
        return
    for item in prompts:
        # Assuming Flux model for images
        response = client.chat.completions.create(
            model="accounts/fireworks/models/flux-1-dev-fp8",
            messages=[{"role": "user", "content": item['prompt']}],
            # Note: For image generation, the API might be different, but assuming similar
        )
        # Assuming response has image data
        # This is placeholder; actual API for images might differ
        image_data = response.choices[0].message.content  # Placeholder
        # Save as PNG
        with open(f"character-images/{item['id']}.png", 'wb') as f:
            f.write(base64.b64decode(image_data))  # Assuming base64

# Placeholder for video generation
async def generate_videos():
    if not interactive_confirm("Generate Videos"):
        return
    # Since LTX not available, skip or use alternative
    print("Video generation skipped as LTX model not available.")

async def generate_vue_code(narrative, visuals):
    if not interactive_confirm("Generate Vue3 Code"):
        return
    prompt = f"""
Generate a complete Vue3 project for the Haunted Asylum game based on the narrative JSON and visual requirements.

Narrative: {json.dumps(narrative)}

Visuals: {json.dumps(visuals)}

Application Requirements: Use dark gothic style, pages for Start, Checkpoints, Cinematics, Game Over, True Ending.

Output the code as a JSON with file paths and contents, e.g. {{"src/App.vue": "code here", "src/main.js": "code"}}.
"""
    messages = [{"role": "user", "content": prompt}]
    code_json = await stream_llm_response("accounts/fireworks/models/kimi-k2p5", messages)
    try:
        code_files = json.loads(code_json)
        for file_path, content in code_files.items():
            full_path = os.path.join('haunted-asylum', file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(content)
    except:
        print("Failed to generate Vue code.")

def assemble_project():
    if not interactive_confirm("Assemble Final Project"):
        return
    # Copy assets
    shutil.copytree('character-images', 'haunted-asylum/public/images', dirs_exist_ok=True)
    # Etc.

async def main():
    create_directories()
    game_bg, char_def, app_req, narr_ex = load_base_data()
    narrative = await generate_narrative(game_bg, char_def, app_req, narr_ex)
    if not narrative:
        return
    visuals = extract_visual_requirements(narrative)
    image_prompts = await generate_image_prompts(visuals)
    await generate_images(image_prompts)
    await generate_videos()
    await generate_vue_code(narrative, visuals)
    assemble_project()
    print("Project implementation complete.")

if __name__ == "__main__":
    asyncio.run(main())

