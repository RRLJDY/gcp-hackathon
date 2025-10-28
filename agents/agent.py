from google.adk.agents import LlmAgent, SequentialAgent, Agent

GEMINI_MODEL = "gemini-2.5-flash"

# import prompts
from agents.prompts.video_prompt import video_prompt
from agents.prompts.pet_prompt import pet_prompt
from agents.prompts.summary_prompt import summary_prompt

import logging
from pathlib import Path
from datetime import datetime
from google import genai
from google.genai import types

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

IMAGE_GENERATION_MODEL = "gemini-2.5-flash-image"

def generate_image(prompt: str, output_dir: str = "generated_images") -> str:
    """Generate an image using Gemini Image and return saved file path."""
    # Ensure output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Initialize client with ADC (no explicit API key needed on GCP)
    client = genai.Client()

    contents = [
        types.Content(
            role="user",
            parts=[types.Part(text=prompt)]
        )
    ]

    config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        max_output_tokens=32768,
        response_modalities=["TEXT", "IMAGE"],
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
        ],
    )

    logger.info(f"Generating image with prompt: {prompt}")
    response = client.models.generate_content(
        model=IMAGE_GENERATION_MODEL,
        contents=contents,
        config=config,
    )

    image_bytes = None
    # Extract first image part
    candidate = response.candidates[0]
    for part in candidate.content.parts:
        if hasattr(part, 'inline_data') and part.inline_data:
            image_bytes = part.inline_data.data
            break

    if not image_bytes:
        raise RuntimeError("No image was generated in the response")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = Path(output_dir) / f"generated_image_{timestamp}.png"
    with open(filepath, "wb") as f:
        f.write(image_bytes)

    logger.info(f"Image saved to: {filepath}")
    return str(filepath)


# --- Sub-Agents ---

video_processor_agent = LlmAgent(
    name="VideoProcessorAgent",
    model=GEMINI_MODEL,
    instruction=video_prompt,
    description="Generates a caption and tags from a video description.",
    output_key="video_output_json"
)

pet_agent = LlmAgent(
    name="PetAgent",
    model=GEMINI_MODEL,
    instruction=pet_prompt,
    description="Creates a one-line summary from video output JSON and pet profile.",
    output_key="one_line_summary"
)

summary_agent = Agent(
    name="SummaryAgent",
    model="gemini-2.5-flash",
    instruction=summary_prompt,
    description="Generates an image based on a one-line summary.",
    output_key="image_path",
    tools=[generate_image],
)

# --- Orchestrator ---
root_agent = SequentialAgent(
    name="PetVideoPipelineAgent",
    sub_agents=[video_processor_agent, pet_agent, summary_agent],
    description="Executes video processing, pet summary generation, and summary prompt generation."
)
