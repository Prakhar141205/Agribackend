from pathlib import Path


PROJECT_NAME = "backend"


FILES = [
    # ============================================================
    # APPLICATION ENTRY POINT
    # ============================================================

    "app/__init__.py",
    "app/main.py",

    # ============================================================
    # API LAYER
    # ============================================================

    "app/api/__init__.py",

    "app/api/routes/__init__.py",
    "app/api/routes/health.py",
    "app/api/routes/diagnosis.py",
    "app/api/routes/diseases.py",
    "app/api/routes/assistant.py",
    "app/api/routes/explorer.py",
    "app/api/routes/soil.py",

    # ============================================================
    # CORE CONFIGURATION
    # ============================================================

    "app/core/__init__.py",
    "app/core/config.py",
    "app/core/security.py",

    # ============================================================
    # MACHINE LEARNING / VIT
    # ============================================================

    "app/ml/__init__.py",
    "app/ml/model.py",
    "app/ml/inference.py",
    "app/ml/preprocessing.py",
    "app/ml/class_mapping.py",
    "app/ml/confidence.py",

    # ============================================================
    # BUSINESS LOGIC / SERVICES
    # ============================================================

    "app/services/__init__.py",
    "app/services/diagnosis_service.py",
    "app/services/disease_service.py",
    "app/services/genai_service.py",
    "app/services/assistant_service.py",
    "app/services/explorer_service.py",
    "app/services/soil_service.py",

    # ============================================================
    # DATA ACCESS / STATIC DATA
    # ============================================================

    "app/repositories/__init__.py",
    "app/repositories/disease_repository.py",
    "app/repositories/crop_repository.py",
    "app/repositories/region_repository.py",
    "app/repositories/soil_repository.py",

    # ============================================================
    # PYDANTIC SCHEMAS
    # ============================================================

    "app/schemas/__init__.py",
    "app/schemas/diagnosis.py",
    "app/schemas/disease.py",
    "app/schemas/assistant.py",
    "app/schemas/explorer.py",
    "app/schemas/soil.py",

    # ============================================================
    # UTILITIES
    # ============================================================

    "app/utils/__init__.py",
    "app/utils/image_utils.py",
    "app/utils/validators.py",
    "app/utils/logger.py",

    # ============================================================
    # GENERATIVE AI
    # ============================================================

    "app/ai/__init__.py",
    "app/ai/openai_client.py",
    "app/ai/gemini_client.py",
    "app/ai/prompts.py",

    # ============================================================
    # STATIC DATA
    # ============================================================

    "data/diseases/.gitkeep",
    "data/crops/.gitkeep",
    "data/regions/.gitkeep",
    "data/soil/.gitkeep",

    # ============================================================
    # TRAINED MODELS
    # ============================================================

    "models/.gitkeep",

    # ============================================================
    # TESTS
    # ============================================================

    "tests/__init__.py",
    "tests/test_health.py",
    "tests/test_diagnosis.py",
    "tests/test_diseases.py",
    "tests/test_assistant.py",
    "tests/test_explorer.py",
    "tests/test_soil.py",

    # ============================================================
    # PROJECT CONFIGURATION
    # ============================================================

    ".env",
    ".env.example",
    ".gitignore",
    "requirements.txt",
    "README.md",
]


def create_project():
    root = Path(PROJECT_NAME)

    root.mkdir(
        parents=True,
        exist_ok=True,
    )

    for file in FILES:
        file_path = root / file

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not file_path.exists():
            file_path.touch()

            print(f"Created: {file_path}")
        else:
            print(f"Exists:  {file_path}")

    print()
    print("=" * 80)
    print("AGRIAI BACKEND STRUCTURE CREATED")
    print("=" * 80)
    print(f"Location : {root.resolve()}")
    print(f"Files    : {len(FILES)}")
    print("=" * 80)


if __name__ == "__main__":
    create_project()