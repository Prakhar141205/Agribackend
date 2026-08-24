**# AgriAI Backend**

FastAPI backend for AgriAI, an agricultural intelligence platform combining computer vision, confidence-aware disease classification, Gemini-powered assistance, and an extensible agricultural advisory layer.

**## Core capabilities**

* ****Disease diagnosis:**** Gemini validates that an uploaded image contains a usable leaf, then a fine-tuned ViT-B/16 performs disease classification.

* ****Confidence-aware inference:**** top-1 confidence and top-1/top-2 margin are evaluated before accepting a prediction.

* ****Disease information:**** Gemini generates structured, farmer-friendly information from an accepted ViT diagnosis.

* ****Explorer:**** users can ask custom agricultural questions with optional crop/disease context.

* ****Agricultural advisory:**** crop recommendation and crop-management services are structured for future soil/environment/sensor inputs.

* ****Future IoT integration:**** the advisory layer can consume soil and environmental sensor data.

**## Architecture**

```text

                         Frontend

                            |

                            v

                     FastAPI Backend

                            |

          +-----------------+------------------+

          \|                 |                  |

          v                 v                  v

      Diagnosis          Explorer           Advisory

          \|                 |                  |

          v                 v                  v

   Gemini leaf check      Gemini             Gemini

          |

     +----+----+

     \|         |

   leaf     not leaf

     \|         |

     v         v

    ViT      reject

     |

     v

confidence / margin

     |

     v

final diagnosis

```

The diagnosis pipeline is intentionally split by responsibility:

```text

Image validation       -> FastAPI/PIL validation

Leaf suitability check -> Gemini

Disease classification -> ViT-B/16

Confidence decision    -> deterministic backend logic

Explanation/information-> Gemini

```

Gemini is ****not**** the primary disease classifier.

**## Project structure**

```text

backend/

├── app/

│   ├── ai/

│   ├── api/

│   │   └── routes/

│   ├── core/

│   ├── ml/

│   ├── repositories/

│   ├── schemas/

│   ├── services/

│   ├── utils/

│   └── main.py

├── data/

│   ├── crops/

│   ├── diseases/

│   ├── regions/

│   └── soil/

├── models/

│   └── best_vit_b16.pt

├── notebooks/

│   └── agrivision.ipynb

├── tests/

├── requirements.txt

└── README.md

```

**## Technology stack**

* Python 3.11

* FastAPI

* Uvicorn

* Pydantic / Pydantic Settings

* PyTorch

* TorchVision

* Vision Transformer (ViT-B/16)

* Pillow

* Google Gemini

* LangChain

* `langchain-google-genai`

FastAPI provides:

```text

/docs

/openapi.json

```

**## Installation**

go to the backend directory

```bash

cd backend

```

Create the environment using conda:

```bash

conda create -n agriai python=3.11

conda activate agriai

```

From the `backend` directory:

```bash

pip install -r requirements.txt

```

**## Environment configuration**

Create `backend/.env`:

```env

APP_NAME=AgriAI Backend

APP_VERSION=1.0.0

DEBUG=True

MODEL_PATH=models/best_vit_b16.pt

CONFIDENCE_THRESHOLD=0.70

TOP2_MARGIN_THRESHOLD=0.20

TOP_K=3

LEAF_VALIDATION_THRESHOLD=0.80

GEMINI_API_KEY=your_gemini_api_key

```

Never commit `.env` or expose `GEMINI_API_KEY` to the frontend.

**## Run the backend**

From `AgriBackend/backend`:

```bash

uvicorn app.main:app --reload

```

Server:

```text

http://127.0.0.1:8000

```

Swagger:

```text

http://127.0.0.1:8000/docs

```

OpenAPI:

```text

http://127.0.0.1:8000/openapi.json

```

**## Health endpoint**

```http

GET /

```

Example:

```json

{

  "service": "AgriAI Backend",

  "version": "1.0.0",

  "status": "running"

}

```

**## Disease prediction**

**### Endpoint**

```http

POST /api/v1/diseases/predict

```

Request:

```text

multipart/form-data

file=\<plant image>

```

**### Pipeline**

```text

Uploaded image

      |

      v

Image validation

      |

      v

Gemini leaf validation

      |

      +---- not a leaf ----> reject

      |

      v

ViT-B/16

      |

      v

Top-K predictions

      |

      v

Confidence evaluation

      |

      v

Accepted / uncertain result

```

The frontend calls the disease prediction endpoint for diagnosis. Leaf validation is an internal gate; there is no separate frontend-facing leaf-validation request. After an accepted diagnosis, the frontend can call the disease-information endpoint when the user selects **View More Information**.

**### Leaf validation**

Gemini is instructed only to determine whether the image is a usable plant leaf.

Example:

```json

{

  "is_leaf": true,

  "confidence": 0.96,

  "reason": "A clearly visible plant leaf occupies most of the image."

}

```

If the image is not suitable:

```json

{

  "is_leaf": false,

  "confidence": 0.99,

  "reason": "The image does not contain a usable plant leaf."

}

```

A diseased, damaged, spotted, or discolored leaf is still considered a valid leaf.

**### ViT inference**

The model is loaded from:

```text

models/best_vit_b16.pt

```

The inference pipeline is:

```text

PIL image

  -> RGB

  -> resize 224x224

  -> tensor

  -> ImageNet normalization

  -> ViT-B/16

  -> logits

  -> softmax

  -> Top-K predictions

```

**### Confidence filtering**

The backend evaluates both:

```text

top1_confidence >= CONFIDENCE_THRESHOLD

```

and:

```text

top1_confidence - top2_confidence >= TOP2_MARGIN_THRESHOLD

```

A prediction is accepted only if both pass.

Default values:

```text

CONFIDENCE_THRESHOLD = 0.70

TOP2_MARGIN_THRESHOLD = 0.20

TOP_K = 3

```

If the prediction is uncertain, the API returns `prediction: null` rather than presenting an unreliable diagnosis.

**## Disease information

### Endpoint

```http
POST /api/v1/diseases/information
```

This endpoint powers the frontend's **View More Information** action after a disease has been successfully diagnosed.

The endpoint does **not** accept another image and does **not** perform disease classification again. The frontend sends the accepted ViT diagnostic result to the backend, and `DiseaseService` passes that diagnostic context to Gemini to generate structured, farmer-friendly information.

### User flow

```text
Plant image
    |
    v
POST /api/v1/diseases/predict
    |
    v
Gemini leaf validation
    |
    v
ViT-B/16 classification
    |
    v
Confidence + margin evaluation
    |
    +---- uncertain / rejected
    |          |
    |          v
    |     No detailed information
    |
    v
Accepted diagnosis
    |
    v
Frontend displays disease result
    |
    v
User clicks "View More Information"
    |
    v
POST /api/v1/diseases/information
    |
    v
DiseaseService
    |
    v
Gemini structured generation
    |
    v
Detailed disease information
```

### Request

The request body is JSON and contains the accepted ViT diagnostic result.

Example:

```json
{
  "prediction": {
    "class_name": "Tomato Early Blight",
    "confidence": 0.94,
    "class_index": 3
  },
  "top_k": [
    {
      "class_name": "Tomato Early Blight",
      "confidence": 0.94,
      "class_index": 3
    },
    {
      "class_name": "Tomato Late Blight",
      "confidence": 0.12,
      "class_index": 5
    }
  ],
  "uncertain": false,
  "confidence_analysis": {
    "accepted": true,
    "top1_confidence": 0.94,
    "top2_confidence": 0.12,
    "confidence_margin": 0.82,
    "confidence_threshold_passed": true,
    "margin_threshold_passed": true
  },
  "more_information_available": true
}
```

### Request fields

| Field | Purpose |
|---|---|
| `prediction` | Accepted top-1 ViT prediction |
| `top_k` | Alternative ViT predictions supplied as diagnostic context |
| `uncertain` | Indicates whether the diagnosis was considered uncertain |
| `confidence_analysis` | Deterministic confidence and margin evaluation |
| `more_information_available` | Indicates whether the frontend should request detailed information |

The backend rejects the request when:

- `uncertain` is `true`
- `confidence_analysis.accepted` is `false`
- `more_information_available` is `false`

### Response

The endpoint returns a structured `DiseaseInformation` response containing:

```json
{
  "disease": "Tomato Early Blight",
  "overview": "...",
  "symptoms": ["..."],
  "causes": ["..."],
  "spread": ["..."],
  "favorable_conditions": ["..."],
  "prevention": ["..."],
  "management": ["..."],
  "treatment": ["..."],
  "affected_parts": ["..."],
  "severity": "Moderate",
  "immediate_actions": ["..."],
  "things_to_avoid": ["..."]
}
```

### Information covered

The disease-information response can contain:

- Disease name
- Overview
- Symptoms
- Causes
- Spread
- Favorable environmental conditions
- Affected plant parts
- Severity
- Immediate actions
- Treatment
- Management
- Prevention
- Things to avoid

### Gemini responsibility

Gemini receives the already-computed ViT diagnostic result as context.

Gemini is instructed to:

- explain the supplied diagnosis
- use farmer-friendly language
- provide practical general guidance
- avoid reclassifying the image
- avoid contradicting the upstream ViT diagnosis
- avoid absolute certainty
- avoid inventing precise pesticide dosage instructions
- distinguish general management guidance from regulated pesticide instructions

The ViT remains the disease-classification component. Gemini is responsible for validation, explanation, and agricultural reasoning.

### Frontend integration

The frontend should treat disease information as a second-stage request:

```text
POST /api/v1/diseases/predict
        |
        v
Display accepted disease
        |
        v
[ View More Information ]
        |
        v
POST /api/v1/diseases/information
        |
        v
Render structured disease-information sections
```

The frontend does not need to know the internal Gemini prompt or service implementation.

## API endpoint summary

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | Backend health check |
| `POST` | `/api/v1/diseases/predict` | Validate leaf and classify disease |
| `POST` | `/api/v1/diseases/information` | Generate detailed information for an accepted diagnosis |
| `POST` | `/api/v1/explorer/ask` | Ask a custom agricultural question |
| `POST` | Advisory routes | Crop recommendation and crop-management capabilities |

## Explorer**

**### Endpoint**

```http

POST /api/v1/explorer/ask

```

Example request:

```json

{

  "query": "How can I prevent fungal disease during the rainy season?",

  "crop": "Tomato",

  "disease": "Early Blight"

}

```

`crop` and `disease` provide optional context.

The Explorer is designed for custom user questions and does not require a large static knowledge database for the current implementation.

Flow:

```text

User question

     |

     v

Explorer route

     |

     v

Explorer service

     |

     v

Gemini

     |

     v

structured response

```

**## Agricultural advisory**

The advisory layer contains separate capabilities for:

* crop recommendations

* crop management

The architecture is prepared to accept real farm/environment information later.

Potential future sensor inputs:

* soil moisture

* soil temperature

* soil pH

* nitrogen

* phosphorus

* potassium

* ambient temperature

* humidity

* light intensity

Future flow:

```text

IoT sensors

     |

     v

sensor/context API

     |

     v

context construction

     |

     v

Gemini

     |

     v

crop recommendation / management guidance

```

The current backend can use assumed/test context while hardware integration is being developed.

**## API responsibility**

\| Component         | Responsibility                       |

\| ----------------- | ------------------------------------ |

\| FastAPI routes    | HTTP/API orchestration               |

\| Pydantic schemas  | Request/response validation          |

\| Image utilities   | Image decoding and validation        |

\| ViT inference     | Disease classification               |

\| Confidence module | Prediction acceptance logic          |

\| Gemini client     | Gemini API integration               |

\| Disease service   | Disease-information business logic   |

\| Explorer service  | Custom agricultural Q&A              |

\| Advisory services | Crop recommendation/management logic |

**## Testing**

Run all tests:

```bash

pytest

```

Verbose:

```bash

pytest -v

```

Specific test:

```bash

pytest tests/test_diagnosis.py

```

**## Model requirements**

The checkpoint is expected at:

```text

backend/models/best_vit_b16.pt

```

The checkpoint must contain the state dictionary and class mapping expected by the current `ViTInference` implementation.

The inference engine validates the class mapping before running predictions.

**## Configuration reference**

\| Variable                    | Purpose                                 | Default                  |

\| --------------------------- | --------------------------------------- | ------------------------ |

\| `APP_NAME`                  | Application name                        | `AgriAI Backend`         |

\| `APP_VERSION`               | API version                             | `1.0.0`                  |

\| `DEBUG`                     | FastAPI debug mode                      | `True`                   |

\| `MODEL_PATH`                | ViT checkpoint                          | `models/best_vit_b16.pt` |

\| `CONFIDENCE_THRESHOLD`      | Minimum top-1 confidence                | `0.70`                   |

\| `TOP2_MARGIN_THRESHOLD`     | Minimum top-1/top-2 margin              | `0.20`                   |

\| `TOP_K`                     | Number of predictions                   | `3`                      |

\| `LEAF_VALIDATION_THRESHOLD` | Minimum accepted Gemini leaf confidence | `0.80`                   |

\| `GEMINI_API_KEY`            | Gemini authentication                   | Required                 |

**## Security**

The Gemini key must remain server-side:

```text

Frontend

   |

   v

FastAPI

   |

   \| GEMINI_API_KEY stays here

   v

Gemini API

```

Do not place the key in frontend code or expose it through public API responses.

**## Current implementation status**

**### Implemented**

* FastAPI application

* Modular routes/services/schemas architecture

* ViT-B/16 disease inference

* Image preprocessing

* Top-K predictions

* Confidence threshold

* Top-1/top-2 margin evaluation

* Gemini client

* Gemini disease-information generation

* Explorer

* Crop recommendation/advisory architecture

* Gemini leaf validation integrated into the disease-prediction pipeline

**### Next planned work**

* OOD detection integration

* Real IoT/sensor integration

* Persistent agricultural datasets

* Farm/field profiles

* Region-specific recommendations

* Sensor-aware fertilizer recommendations

* Weather integration

* Production deployment

* Authentication/authorization

* Observability and model monitoring

**## Design principles**

**### Separation of responsibilities**

```text

ViT       -> visual disease classification

Gemini    -> validation, explanation, agricultural reasoning

FastAPI   -> orchestration

Pydantic  -> validation

Services  -> business logic

ML layer  -> model inference

```

**### Fail safely**

An uncertain model prediction should be surfaced as uncertain rather than presented as a definitive diagnosis.

**### Keep the frontend simple**

The frontend interacts with high-level API endpoints and does not need to know the internal sequence of Gemini validation, ViT inference, and confidence evaluation.

**### Keep the architecture extensible**

The backend is designed to combine:

```text

Computer Vision

      \+

Generative AI

      \+

IoT Sensors

      \+

Agricultural Context

```

into a single agricultural decision-support platform.

**## Quick start**

```bash

conda activate agriai

cd backend

pip install -r requirements.txt

uvicorn app.main:app --reload

```

Open:

```text

http://127.0.0.1:8000/docs

```