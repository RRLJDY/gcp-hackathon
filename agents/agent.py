from google.adk.agents import LlmAgent, SequentialAgent, Agent

GEMINI_MODEL = "gemini-2.5-flash"

# import prompts
from agents.prompts.video_prompt import video_prompt
from agents.prompts.pet_prompt import pet_prompt
from agents.prompts.summary_prompt import summary_prompt

from google.adk.tools import ToolContext

def generate_image(prompt: str, scene_number: int, tool_context: ToolContext):
    """
    gemini-2.5-flash-image 모델을 사용하여 텍스트로 이미지를 생성합니다.
    """
    try:
        # 1. 이미지 생성 모델 선택
        # 이 모델은 텍스트 프롬프트에 대해 이미지 데이터를 직접 반환합니다.
        print(f"'{prompt_text}'에 대한 이미지 생성을 시작합니다...")
        model = genai.GenerativeModel(model_name="gemini-2.5-flash-image")

        # 2. 이미지 생성 요청
        response = model.generate_content(prompt_text)

        # 3. 응답에서 이미지 데이터 추출
        # 응답의 'parts' 리스트에 이미지 데이터가 포함됩니다.
        if response.parts:
            # 첫 번째 part에서 'inline_data' (Blob)를 가져옵니다.
            image_data = response.parts[0].inline_data
            
            # MIME 타입이 이미지인지 확인
            if image_data.mime_type.startswith("image/"):
                
                # 4. PIL을 사용하여 이미지 데이터 열기
                image_bytes = image_data.data
                image = PIL.Image.open(io.BytesIO(image_bytes))
                
                # (선택 사항) Jupyter 노트북 등에서 이미지 바로 보기
                # image.show() 

                # 5. 이미지 파일로 저장
                output_filename = "generated_image.png"
                image.save(output_filename)
                print(f"성공! 이미지를 '{output_filename}' 파일로 저장했습니다.")
                
            else:
                print(f"오류: 이미지 데이터가 아닌 응답을 받았습니다. (MIME: {image_data.mime_type})")
        
        else:
            # 프롬프트가 안전 필터에 의해 거부되었거나 다른 문제가 발생한 경우
            print(f"오류: 응답에 이미지 데이터가 없습니다.")
            # 거부 사유 등을 확인하려면 'response.prompt_feedback'을 확인하세요.
            print(f"응답 피드백: {response.prompt_feedback}")

    except Exception as e:
        print(f"이미지 생성 중 오류가 발생했습니다: {e}")


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
    output_key="generated_image",
    tools=[generate_image],
)

# --- Orchestrator ---
root_agent = SequentialAgent(
    name="PetVideoPipelineAgent",
    sub_agents=[video_processor_agent, pet_agent, summary_agent],
    description="Executes video processing, pet summary generation, and summary prompt generation."
)
