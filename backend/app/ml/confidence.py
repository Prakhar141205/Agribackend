def evaluate_prediction_confidence(
    top_k: list[dict],
    confidence_threshold: float,
    margin_threshold: float,
) -> dict:
    top1_confidence = float(top_k[0]["confidence"])
    top2_confidence = float(top_k[1]["confidence"]) if len(top_k) > 1 else 0.0
    confidence_margin = top1_confidence - top2_confidence
    confidence_threshold_passed = (
        top1_confidence >= confidence_threshold
    )
    margin_threshold_passed = (
        confidence_margin >= margin_threshold
    )

    return {
        "top1_confidence": top1_confidence,
        "top2_confidence": top2_confidence,
        "confidence_margin": confidence_margin,
        "confidence_threshold_passed": confidence_threshold_passed,
        "margin_threshold_passed": margin_threshold_passed,
        "accepted": (
            confidence_threshold_passed
            and margin_threshold_passed
        ),
    }