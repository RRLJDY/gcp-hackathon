import os
import logging
from pathlib import Path
from datetime import datetime
from google import genai
from google.genai import types
from google.adk.agents import LlmAgent, SequentialAgent, Agent
from google.adk.tools.tool_context import ToolContext
from agents.prompts.video_prompt import video_prompt
from agents.prompts.pet_prompt import pet_prompt
from agents.prompts.summary_prompt import summary_prompt
from dotenv import load_dotenv

# --- Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Load environment variables ---
load_dotenv()

# --- Constants ---
GEMINI_MODEL = "gemini-2.5-flash"
IMAGE_GENERATION_MODEL = "gemini-2.5-flash-image"
OUTPUT_DIR = "generated_images"

# --- Gemini Client ---
client = genai.Client(
    vertexai=True,
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location="us-central1"
)

# --- Image generation tool (async) ---
async def generate_image(prompt: str, tool_context: ToolContext) -> dict:
    """
    Generate an image based on a text prompt and register it as an ADK Artifact.
    """
    try:
        Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

        contents = [types.Content(role="user", parts=[types.Part(text=prompt)])]
        generate_config = types.GenerateContentConfig(
            temperature=1,
            top_p=0.95,
            max_output_tokens=32768,
            response_modalities=["TEXT", "IMAGE"]
        )

        logger.info(f"Generating image with prompt: {prompt}")
        response = client.models.generate_content(
            model=IMAGE_GENERATION_MODEL,
            contents=contents,
            config=generate_config
        )

        # Extract image data
        image_data = None
        text_response = ""
        for part in response.candidates[0].content.parts:
            if hasattr(part, "inline_data") and part.inline_data:
                image_data = part.inline_data.data
            elif hasattr(part, "text") and part.text:
                text_response += part.text

        if not image_data:
            return {"status": "failed", "error": "No image generated", "text_response": text_response}

        # Save image locally
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_image_{timestamp}.png"
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(image_data)

        logger.info(f"Image saved locally: {filepath}")

        # --- Register as ADK Artifact ---
        image_artifact = types.Part(
            inline_data=types.Blob(
                mime_type="image/png",
                data=image_data
            )
        )

        artifact = await tool_context.save_artifact(
            filename=filename,
            artifact=image_artifact
        )

        return {
            "status": "success",
            "image_path": filepath,
            "prompt": prompt
        }

    except Exception as e:
        logger.error(f"Image generation error: {e}")
        return {"status": "failed", "error": str(e)}

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
    model=GEMINI_MODEL,
    instruction=summary_prompt,
    description="Generates an image based on a one-line summary and registers it as an Artifact.",
    output_key="generated_image",
    tools=[generate_image],
)

# --- Orchestrator ---
root_agent = SequentialAgent(
    name="PetVideoPipelineAgent",
    sub_agents=[video_processor_agent, pet_agent, summary_agent],
    description="Executes video processing, pet summary generation, and image generation with Artifact registration."
)
