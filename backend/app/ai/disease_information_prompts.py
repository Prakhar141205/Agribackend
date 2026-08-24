import json

from langchain_core.prompts import ChatPromptTemplate

from app.schemas.disease import DiseaseInformationRequest


DISEASE_INFORMATION_PROMPT = ChatPromptTemplate.from_messages(
	[
		(
			"system",
			"""
You are an agricultural information assistant.

The plant disease has already been classified by an upstream ViT image classifier.
Do not reclassify the image. Do not contradict the supplied diagnosis.
Treat the supplied ViT result as the diagnostic context.

Use farmer-friendly language.
Provide practical general guidance and avoid absolute certainty.
Do not invent precise pesticide dosage instructions.
When local regulations or product labels are unknown, avoid highly specific chemical recommendations.
Distinguish general management guidance from regulated pesticide instructions.

Return only the requested structured fields.
""".strip(),
		),
		(
			"human",
			"""
Complete ViT diagnostic result:
{vit_result}

Predicted disease: {predicted_disease}
Prediction confidence: {prediction_confidence}
Top alternative predictions: {top_k_json}
Confidence margin: {confidence_margin}
Diagnosis status: uncertain={uncertain}, accepted={accepted}
""".strip(),
		),
	]
)


def build_diagnostic_prompt_context(
	diagnostic: DiseaseInformationRequest,
) -> dict[str, str]:
	prediction = diagnostic.prediction
	predicted_disease = prediction.class_name
	prediction_confidence = str(prediction.confidence)
	serialized_vit_result = json.dumps(
		diagnostic.model_dump(),
		ensure_ascii=True,
	)

	return {
		"vit_result": serialized_vit_result,
		"predicted_disease": predicted_disease,
		"prediction_confidence": prediction_confidence,
		"top_k_json": json.dumps(
			[item.model_dump() for item in diagnostic.top_k],
			ensure_ascii=True,
		),
		"confidence_margin": str(diagnostic.confidence_analysis.confidence_margin),
		"uncertain": str(diagnostic.uncertain),
		"accepted": str(diagnostic.confidence_analysis.accepted),
	}
