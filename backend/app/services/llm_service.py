import base64
import json

from openai import OpenAI
from app.core.config import settings
from app.core.logging import logger

class LLMService:
    def __init__(self):
        self.client = OpenAI(
            base_url=settings.OPENROUTER_URL,
            api_key=settings.OPENROUTER_API_KEY
        )
        logger.info(f"LLM Service initialized with model: {settings.OPENROUTER_MODEL_NAME}")

    async def analyze(self, prompt: str, structure: list, image_bytes: bytes, image_type: str):
        logger.info(f"Starting LLM analysis with {len(structure)} fields, image: {bool(image_bytes)}")
        logger.debug(f"Prompt: {prompt[:100]}...")  # Log only first 100 chars
        
        user_content = [{"type": "text", "text": prompt}]

        if image_bytes and image_type:  # Only add image if provided
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            data_url = f"data:{image_type};base64,{base64_image}"
            user_content.append({"type": "image_url", "image_url": {"url": data_url}})
            logger.debug(f"Image included: {image_type}, size: {len(image_bytes)} bytes")

        field_instructions = ", ".join([f"'{f['name']}' (type: {f['type']})" for f in structure])

        system_prompt = f"""
        You are data extration assistant.
        Your goal is to analyze and extract data from the image based on the user's prompt.

        STRICT OUTPUT FORMAT:
        - Respond ONLY in a valid JSON format.
        - Do not include any explanations or additional text.
        - The JSON must exactly match these keys and types: {field_instructions}.
        - If a value is not found, use null for that field.
        """

        try:
            response = self.client.chat.completions.create(
                model=settings.OPENROUTER_MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            result = json.loads(content)
            logger.info(f"LLM analysis completed successfully, fields returned: {list(result.keys())}")
            return result
        except Exception as e:
            logger.error(f"LLM analysis failed: {str(e)}", exc_info=True)
            raise Exception(f"LLM analysis failed: {str(e)}")