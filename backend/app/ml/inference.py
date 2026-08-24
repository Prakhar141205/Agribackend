from pathlib import Path

import torch
from PIL import Image

from app.ml.confidence import evaluate_prediction_confidence
from app.ml.model import create_model
from app.ml.preprocessing import inference_transform


class ViTInference:

    def __init__(
        self,
        model_path: str,
        confidence_threshold: float = 0.70,
        margin_threshold: float = 0.20,
        top_k: int = 3,
    ):
        self.model_path = Path(model_path)

        self.device = torch.device(
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        checkpoint = torch.load(
            self.model_path,
            map_location=self.device,
            weights_only=False,
        )

        if not isinstance(checkpoint, dict):
            raise ValueError("The model checkpoint must be a dictionary.")

        state_dict = checkpoint.get("model_state_dict")
        class_to_index = checkpoint.get("class_to_index")

        if not isinstance(state_dict, dict):
            raise ValueError(
                "The model checkpoint does not contain model_state_dict."
            )

        if not isinstance(class_to_index, dict) or not class_to_index:
            raise ValueError(
                "The model checkpoint does not contain class_to_index."
            )

        try:
            self.class_to_index = {
                str(class_name): int(index)
                for class_name, index in class_to_index.items()
            }
        except (TypeError, ValueError) as exc:
            raise ValueError(
                "The checkpoint class_to_index mapping is invalid."
            ) from exc

        indices = sorted(self.class_to_index.values())
        if indices != list(range(len(indices))):
            raise ValueError(
                "The checkpoint class indices must be contiguous from zero."
            )

        self.index_to_class = {
            int(index): class_name
            for class_name, index in self.class_to_index.items()
        }

        self.num_classes = int(
            checkpoint.get("num_classes", len(self.class_to_index))
        )

        if self.num_classes != len(self.class_to_index):
            raise ValueError(
                "Checkpoint num_classes does not match class_to_index."
            )

        self.confidence_threshold = (
            confidence_threshold
        )

        self.margin_threshold = (
            margin_threshold
        )

        self.top_k = min(
            top_k,
            self.num_classes,
        )

        self.model = create_model(
            self.num_classes
        )

        classifier_weight = state_dict.get(
            "heads.head.weight"
        )
        if classifier_weight is None or classifier_weight.shape[0] != self.num_classes:
            raise ValueError(
                "Checkpoint classifier shape does not match the class mapping."
            )

        self.model.load_state_dict(
            state_dict
        )

        self.model.to(
            self.device
        )

        self.model.eval()

    def predict(
        self,
        image: Image.Image,
    ):

        image = image.convert("RGB")

        image_tensor = inference_transform(
            image
        )

        image_tensor = image_tensor.unsqueeze(
            0
        )

        image_tensor = image_tensor.to(
            self.device
        )

        with torch.inference_mode():

            logits = self.model(
                image_tensor
            )

            probabilities = torch.softmax(
                logits,
                dim=1
            )

        top_probabilities, top_indices = (
            torch.topk(
                probabilities,
                k=self.top_k,
                dim=1,
            )
        )

        top_probabilities = (
            top_probabilities[0]
            .cpu()
            .tolist()
        )

        top_indices = (
            top_indices[0]
            .cpu()
            .tolist()
        )

        predictions = []

        for probability, index in zip(
            top_probabilities,
            top_indices,
        ):
            predictions.append({
                "class_name": self.index_to_class[
                    int(index)
                ],
                "confidence": float(
                    probability
                ),
                "class_index": int(index),
            })

        best_prediction = predictions[0]

        confidence_evaluation = evaluate_prediction_confidence(
            top_k=predictions,
            confidence_threshold=self.confidence_threshold,
            margin_threshold=self.margin_threshold,
        )

        accepted = confidence_evaluation["accepted"]

        result = {
            "prediction": best_prediction if accepted else None,
            "top_k": predictions,
            "uncertain": not accepted,
            "confidence_analysis": confidence_evaluation,
            "more_information_available": accepted,
        }

        if not accepted:
            result["message"] = (
                "The model is not sufficiently confident. "
                "Please upload a clearer or additional image."
            )

        return result