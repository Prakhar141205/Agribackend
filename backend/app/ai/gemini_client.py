from typing import TYPE_CHECKING, Any
import base64
from app.core.config import settings
from app.schemas.disease import DiseaseInformation
from app.schemas.explorer import ExplorerResponse
from app.schemas.advisory import (
    CropManagementResponse,
    CropRecommendationResponse,
)

from app.schemas.leaf_validation import LeafValidationResponse

if TYPE_CHECKING:
    from langchain_core.prompts import ChatPromptTemplate


class GeminiClient:

    def __init__(self):
        if not settings.GEMINI_API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured."
            )

        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
        except ImportError as exc:
            raise RuntimeError(
                "LangChain Gemini dependencies are not installed."
            ) from exc

        self.chat_model: Any = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash",
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0,
        )

    async def generate_disease_information(
        self,
        prompt: "ChatPromptTemplate",
        prompt_variables: dict[str, str],
    ) -> DiseaseInformation:
        structured_model = self.chat_model.with_structured_output(
            DiseaseInformation
        )

        chain = prompt | structured_model
        response = await chain.ainvoke(prompt_variables)

        if not response:
            raise ValueError(
                "Gemini returned an empty response."
            )

        if isinstance(response, DiseaseInformation):
            return response

        try:
            return DiseaseInformation.model_validate(response)
        except Exception as exc:
            raise ValueError(
                "Gemini response did not match the expected schema."
            ) from exc

    async def generate_explorer_information(
        self,
        prompt: "ChatPromptTemplate",
        prompt_variables: dict[str, str],
    ) -> ExplorerResponse:
        structured_model = self.chat_model.with_structured_output(
            ExplorerResponse
        )

        chain = prompt | structured_model

        response = await chain.ainvoke(
            prompt_variables
        )

        if not response:
            raise ValueError(
                "Gemini returned an empty response."
            )

        if isinstance(response, ExplorerResponse):
            return response

        try:
            return ExplorerResponse.model_validate(
                response
            )
        except Exception as exc:
            raise ValueError(
                "Gemini response did not match the Explorer schema."
            ) from exc


    async def generate_crop_recommendations(
    self,
        prompt: "ChatPromptTemplate",
        prompt_variables: dict[str, str],
    ) -> CropRecommendationResponse:

        structured_model = self.chat_model.with_structured_output(
            CropRecommendationResponse
        )

        chain = prompt | structured_model

        response = await chain.ainvoke(
            prompt_variables
        )

        if not response:
            raise ValueError(
                "Gemini returned an empty response."
            )

        if isinstance(response, CropRecommendationResponse):
            return response

        try:
            return CropRecommendationResponse.model_validate(
                response
            )
        except Exception as exc:
            raise ValueError(
                "Gemini response did not match the crop recommendation schema."
            ) from exc


    async def generate_crop_management(
        self,
        prompt: "ChatPromptTemplate",
        prompt_variables: dict[str, str],
    ) -> CropManagementResponse:

        structured_model = self.chat_model.with_structured_output(
            CropManagementResponse
        )

        chain = prompt | structured_model

        response = await chain.ainvoke(
            prompt_variables
        )

        if not response:
            raise ValueError(
                "Gemini returned an empty response."
            )

        if isinstance(response, CropManagementResponse):
            return response

        try:
            return CropManagementResponse.model_validate(
                response
            )
        except Exception as exc:
            raise ValueError(
                "Gemini response did not match the crop management schema."
            ) from exc
    async def validate_leaf_image(
            self,
            image_bytes: bytes,
            mime_type: str,
        ) -> LeafValidationResponse:

        structured_model = self.chat_model.with_structured_output(
            LeafValidationResponse
        )

        image_base64 = base64.b64encode(
            image_bytes
        ).decode("utf-8")

        image_data_url = (
            f"data:{mime_type};base64,{image_base64}"
        )

        response = await structured_model.ainvoke(
            [
                {
                    "role": "system",
                    "content": """
    You are an agricultural image validation assistant.

    Your ONLY task is to determine whether the supplied image
    contains a visible plant leaf suitable for downstream
    agricultural disease classification.

    Do NOT diagnose the disease.
    Do NOT identify the crop.
    Do NOT provide treatment recommendations.

    Accept:
    - clearly visible plant leaves
    - healthy leaves
    - diseased leaves
    - damaged leaves
    - discolored or spotted leaves

    Reject:
    - images without a plant leaf
    - soil-only images
    - people
    - buildings
    - equipment
    - screenshots
    - documents
    - unrelated objects
    - images where the leaf is too small to inspect
    - severely blurry or unusable images

    A diseased leaf is still a valid leaf.

    Return only the requested structured fields.
    """.strip(),
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Determine whether this image "
                                "contains a usable plant leaf."
                            ),
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_data_url
                            },
                        },
                    ],
                },
            ]
        )

        if not response:
            raise ValueError(
                "Gemini returned an empty leaf validation response."
            )

        if isinstance(
            response,
            LeafValidationResponse,
        ):
            return response

        try:
            return LeafValidationResponse.model_validate(
                response
            )
        except Exception as exc:
            raise ValueError(
                "Gemini response did not match the leaf validation schema."
            ) from exc