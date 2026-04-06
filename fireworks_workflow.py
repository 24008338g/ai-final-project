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
OUTPUT_DIRS = ['narratives', 'character-images', 'videos', 'video-prompts', 'haunted-asylum', 'placeholder_assets']

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
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(full_response)
    return full_response

async def generate_image_response(model, prompt_text, save_path=None):
    messages = [{"role": "user", "content": prompt_text}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=False,
        max_tokens=1000
    )
    full_response = response.choices[0].message.content
    print(f"\nResponse from {model}: {full_response[:100]}...")
    if save_path:
        with open(save_path, 'w', encoding='utf-8') as f:
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
    narrative_raw_path = 'narratives/narrative_stream.txt'
    narrative_json = await stream_llm_response("accounts/fireworks/models/deepseek-v3p1", messages, narrative_raw_path)
    # Strip markdown code blocks if present
    narrative_json = narrative_json.strip()
    if narrative_json.startswith('```json'):
        narrative_json = narrative_json[7:]
    if narrative_json.endswith('```'):
        narrative_json = narrative_json[:-3]
    narrative_json = narrative_json.strip()
    try:
        parsed = json.loads(narrative_json)
        with open(narrative_path, 'w', encoding='utf-8') as f:
            f.write(narrative_json)
        return parsed
    except json.JSONDecodeError:
        print("Failed to parse narrative JSON. Raw response saved to narratives/narrative_stream.txt.")
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
    backup_path = 'narratives/image_prompts_stream.txt'
    with open(backup_path, 'w', encoding='utf-8') as backup_file:
        for visual in visuals:
            prompt_text = f"Generate a detailed image prompt for the cinematic scene: {visual['description']}. Make it suitable for AI image generation, gothic horror style."
            messages = [{"role": "user", "content": prompt_text}]
            prompt = await stream_llm_response("accounts/fireworks/models/deepseek-v3p1", messages)
            prompt = prompt.strip()
            backup_file.write(f"--- {visual['id']} ---\n")
            backup_file.write(prompt + "\n\n")
            prompts.append({
                'id': visual['id'],
                'prompt': prompt
            })
            # Save individual prompt file
            with open(f"character-images/{visual['id']}_prompt.txt", 'w', encoding='utf-8') as f:
                f.write(prompt)
    return prompts

async def generate_images(prompts):
    if not interactive_confirm("Generate Images"):
        return

    import urllib.request
    import re

    for item in prompts:
        prompt_text = item['prompt']
        messages = [{"role": "user", "content": prompt_text}]
        stream_path = f"narratives/image_generation_{item['id']}_stream.txt"
        image_response = await generate_image_response("fireworks/flux-kontext-pro", prompt_text, stream_path)

        image_response = image_response.strip()
        if image_response.startswith('```'):
            image_response = image_response.split('```', 1)[1]
            if image_response.endswith('```'):
                image_response = image_response[:-3]
        image_response = image_response.strip()

        # First, try to decode directly as base64
        try:
            image_data = base64.b64decode(image_response)
            with open(f"character-images/{item['id']}.png", 'wb') as f:
                f.write(image_data)
            print(f"Saved generated image character-images/{item['id']}.png")
            continue
        except Exception:
            pass

        # If direct decode fails, try JSON parsing
        image_obj = None
        try:
            image_obj = json.loads(image_response)
        except json.JSONDecodeError:
            json_start = image_response.find('{')
            json_end = image_response.rfind('}')
            if json_start != -1 and json_end != -1 and json_end > json_start:
                try:
                    image_obj = json.loads(image_response[json_start:json_end + 1])
                except json.JSONDecodeError:
                    image_obj = None

        if image_obj and 'image_base64' in image_obj:
            raw_b64 = image_obj['image_base64']
            if raw_b64.startswith('data:image'):
                raw_b64 = raw_b64.split(',', 1)[1]
            image_data = base64.b64decode(raw_b64)
            with open(f"character-images/{item['id']}.png", 'wb') as f:
                f.write(image_data)
            print(f"Saved generated image character-images/{item['id']}.png")
        elif image_obj and 'image_url' in image_obj:
            image_url = image_obj['image_url']
            print(f"Downloading generated image from {image_url}")
            image_data = urllib.request.urlopen(image_url).read()
            with open(f"character-images/{item['id']}.png", 'wb') as f:
                f.write(image_data)
            print(f"Saved downloaded image character-images/{item['id']}.png")
        else:
            # If the model returned raw base64 directly, try to decode it (fallback)
            b64_match = re.search(r'([A-Za-z0-9+/=\n]+)', image_response)
            if b64_match:
                raw_b64 = b64_match.group(1).replace('\n', '')
                try:
                    image_data = base64.b64decode(raw_b64)
                    with open(f"character-images/{item['id']}.png", 'wb') as f:
                        f.write(image_data)
                    print(f"Saved generated image character-images/{item['id']}.png")
                    continue
                except Exception:
                    pass

            print(f"Could not parse generated image for {item['id']}. Check {stream_path} for raw output.")

# Placeholder for video generation
async def generate_videos(narrative, visuals, image_prompts):
    if not interactive_confirm("Generate Videos"):
        return

    prompt = f"""
Create a video storyboard and production plan for the Haunted Asylum game using the narrative and visuals below.

Narrative: {json.dumps(narrative)}
Visual Requirements: {json.dumps(visuals)}
Image Prompts: {json.dumps(image_prompts)}

Output valid JSON only in the following shape:
{{
  "videos": [
    {{
      "id": "intro",
      "title": "Intro Cutscene",
      "description": "...",
      "duration_seconds": 10,
      "video_prompt": "..."
    }}
  ]
}}

Do not add any explanatory text outside the JSON.
"""
    messages = [{"role": "user", "content": prompt}]
    stream_path = 'videos/video_generation_stream.txt'
    video_response = await stream_llm_response("accounts/fireworks/models/kimi-k2p5", messages, stream_path)
    video_response = video_response.strip()
    if video_response.startswith('```'):
        video_response = video_response.split('```', 1)[1]
        if video_response.endswith('```'):
            video_response = video_response[:-3]
    video_response = video_response.strip()

    video_plan = None
    try:
        video_plan = json.loads(video_response)
    except json.JSONDecodeError:
        json_start = video_response.find('{')
        json_end = video_response.rfind('}')
        if json_start != -1 and json_end != -1 and json_end > json_start:
            try:
                video_plan = json.loads(video_response[json_start:json_end + 1])
            except json.JSONDecodeError:
                video_plan = None

    if video_plan:
        with open('videos/video_storyboard.json', 'w', encoding='utf-8') as f:
            json.dump(video_plan, f, indent=2)
        print('Saved videos/video_storyboard.json')
    else:
        print('Failed to parse video storyboard JSON. Raw output saved to videos/video_generation_stream.txt.')

    # Attempt local slideshow assembly if ffmpeg is installed and we have generated images.
    try:
        import subprocess
        import glob

        image_paths = sorted(glob.glob('character-images/*.png'))
        if image_paths and shutil.which('ffmpeg'):
            concat_file = 'videos/video_input.txt'
            with open(concat_file, 'w', encoding='utf-8') as f:
                for image_path in image_paths:
                    f.write(f"file '{os.path.abspath(image_path).replace('\\', '/')}'\n")
                    f.write('duration 3\n')
                # Repeat last frame for final duration
                f.write(f"file '{os.path.abspath(image_paths[-1]).replace('\\', '/')}'\n")

            output_video = 'videos/haunted_asylum_cutscene.mp4'
            subprocess.run([
                'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', concat_file,
                '-vf', 'scale=1280:720', '-r', '24', '-pix_fmt', 'yuv420p',
                output_video
            ], check=False)
            print(f'Created local slideshow video at {output_video}')
        elif image_paths:
            print('ffmpeg not found; skipping local video assembly. Generated image files are available in character-images/.')
        else:
            print('No generated images found; skipping local video assembly.')
    except Exception as e:
        print(f'Unable to assemble local video: {e}')

async def generate_vue_code(narrative, visuals):
    if not interactive_confirm("Generate Vue3 Code"):
        return
    prompt = f"""
Generate a complete Vue3 project for the Haunted Asylum game based on the narrative JSON and visual requirements.

Narrative: {json.dumps(narrative)}

Visuals: {json.dumps(visuals)}

Application Requirements: Use dark gothic style, pages for Start, Checkpoints, Cinematics, Game Over, True Ending.

For all images and videos, use placeholder assets from the public folder (e.g., /public/placeholder_image.png, /public/placeholder_video.mp4). Do not generate actual media files.

Output the code as a JSON with file paths and contents, e.g. {{"src/App.vue": "code here", "src/main.js": "code"}}.
"""
    messages = [{"role": "user", "content": prompt}]
    code_stream_path = 'narratives/vue_code_stream.txt'
    code_json = await stream_llm_response("accounts/fireworks/models/deepseek-v3p1", messages, code_stream_path)
    try:
        code_files = json.loads(code_json)
        for file_path, content in code_files.items():
            full_path = os.path.join('haunted-asylum', file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
    except json.JSONDecodeError:
        print("Failed to parse Vue code JSON. Raw output saved to narratives/vue_code_stream.txt.")
    except Exception as e:
        print(f"Failed to generate Vue code: {e}")

def assemble_project():
    if not interactive_confirm("Assemble Final Project"):
        return
    # Copy placeholder assets
    if os.path.exists('placeholder_assets'):
        shutil.copytree('placeholder_assets', 'haunted-asylum/public', dirs_exist_ok=True)
    # Etc.

async def main():
    create_directories()
    game_bg, char_def, app_req, narr_ex = load_base_data()
    narrative = await generate_narrative(game_bg, char_def, app_req, narr_ex)
    if not narrative:
        return
    visuals = extract_visual_requirements(narrative)
    image_prompts = await generate_image_prompts(visuals)
    # await generate_images(image_prompts)  # Skipped for now
    # await generate_videos(narrative, visuals, image_prompts)  # Skipped for now
    await generate_vue_code(narrative, visuals)
    assemble_project()
    print("Project implementation complete.")

if __name__ == "__main__":
    asyncio.run(main())

