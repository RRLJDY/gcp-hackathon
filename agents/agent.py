from google.adk.agents import LlmAgent, SequentialAgent

GEMINI_MODEL = "gemini-2.5-flash"

# import prompts
from agents.prompts.video_prompt import video_prompt
from agents.prompts.pet_prompt import pet_prompt
from agents.prompts.summary_prompt import summary_prompt

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

summary_agent = LlmAgent(
    name="SummaryAgent",
    model=GEMINI_MODEL,
    instruction=summary_prompt,
    description="Generates a detailed summary prompt from the one-line summary.",
    output_key="summary_prompt"
)

# --- Orchestrator ---
root_agent = SequentialAgent(
    name="PetVideoPipelineAgent",
    sub_agents=[video_processor_agent, pet_agent, summary_agent],
    description="Executes video processing, pet summary generation, and summary prompt generation."
)
