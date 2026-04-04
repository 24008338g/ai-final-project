## Plan: Automate Multi-Agent Game Generation with Fireworks

Generate a complete "Haunted Asylum" narrative game using multiple AI agents via Fireworks API, producing a playable Vue3 web app with generated assets saved locally.

**Steps**
1. **Initialize project structure** — Create output directories (/narratives, /character-images, /videos, /haunted-asylum) and load base data from gamebackground.txt and 8338g.yaml.
2. **Generate linear narrative** — Use DeepSeek V3.1 LLM agent to create a cohesive story outline and scene descriptions based on the game background and character definitions. The narrative will include branching points, also known as checkpoints, with two choices. One choice immediately leads to the player character performing an action that results in "Game Over", while the other choice allows the player to progress towards the "True Ending". The narrative will be saved as a JSON file in the /narratives directory for reference during asset generation and code integration.
3. **Extract visual requirements** — Parse the narrative and application requirements to identify key scenes, characters, and visual elements needing images/videos.
4. **Generate image prompts** — Use LLM agent to craft detailed prompts for character visuals and in-game assets.
5. **Generate images** — Use Flux image generation model via Fireworks to create PNG/JPG images from prompts, saving to /character-images with descriptive names (e.g., elara_portrait.png).
6. **Generate video prompts** — Use LLM agent to create prompts for video sequences aka "cinematics" that reflect narrative sequences (e.g. Elara throws a chair at the Faceless One). 
7. **Generate videos reference images** — Use Flux model via Fireworks to images based on the video prompts, saving to /video-references with descriptive names (e.g., elara_walkthrough.png). Short videos (5-10 seconds) will be generated based on the images created in this step in a different workflow. Alternatively, if the LTX video model is available via Fireworks API, it can be used to generate videos directly from the prompts without needing to create reference images first and the outputs can be saved to /videos with descriptive names (e.g., elara_walkthrough.mp4).
8. **Design game structure** — Use LLM agent to plan the Vue3 app architecture (components for scenes, dialogue, navigation).
9. **Generate Vue3 code** — Use code generation LLM agent to create the full Vue3 project files (App.vue, components, router, etc.), integrating narrative, images, and videos.
10. **Assemble final project** — Copy generated assets into the Vue3 project and save the complete /haunted-asylum folder.

**Relevant files**
- [fireworks_workflow.py](fireworks_workflow.py) — Extend this script into the main orchestration file
- [gamebackground.txt](gamebackground.txt) — Source for narrative generation
- [8338g.yaml](8338g.yaml) — Character definitions and scene prompts
- [comfyworkflows/flux2-klein-t2i-distilled.json](comfyworkflows/flux2-klein-t2i-distilled.json) — Reference for image generation prompts (though not integrated)
- [application_requirements.md] (application_requirements.md) - Source for descriptions of game mechanics and asset needs
- [narrative_example.md](narrative_example.md) Example of narrative structure and content style to be referenced for narrative generation

**Verification**
1. Run the generated Vue3 app locally (npm install, npm run dev) and verify it loads the narrative, displays images/videos, and allows progression through scenes.
2. Check output directories: /narratives contains narrative related files, /character-images has generated PNGs, /videos has MP4s, /haunted-asylum is a complete Vue project.
3. Validate asset integration: Ensure images/videos are correctly referenced in Vue components and load without errors.

**Decisions**
- Agents: DeepSeek V3.1 for text/narrative/project management, Flux for images, Kimi K2.5 for code.
- Outputs: Narrative as .json in /narratives, images as PNG in /character-images, videos as MP4 in /videos, Vue3 project in /haunted-asylum.
- Scope: Focus on linear narrative game with two possible endings, "Game Over" and "True Ending".
- Dependencies: Requires Fireworks API access to multiple models; add error handling for model availability.

**Further Considerations**
1. Model availability: Confirm LTX video model is accessible via Fireworks API (may need to check docs or test).
2. Performance: Generating videos may be resource-intensive; consider limits on API calls.
