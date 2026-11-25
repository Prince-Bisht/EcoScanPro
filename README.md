
# 🌱 EcoScanPro
### AI-Powered Smart Waste Management System

EcoScanPro is a full-stack, AI-powered waste management web application built using **Python, Flask, Machine Learning, Deep Learning, OpenCV, and Google Gemini AI**.

The project combines waste generation forecasting, image-based waste classification, and an AI environmental assistant into one responsive web platform.

EcoScanPro is designed as an educational project demonstrating how Artificial Intelligence can support smarter and more sustainable waste management.

---

## 🌐 Live Website

**Deployment Platform:** Render

**Live Website:** [EcoScanPro](https://ecoscanpros.onrender.com)

> The deployment link will be updated after the website is successfully hosted on Render.

---

## 🚀 Key Features

EcoScanPro consists of three major modules.

### 📊 Module 1 — AI Waste Generation Prediction

Predicts estimated waste generation using **Linear Regression**.

Features:

- Indian city-based waste forecasting
- Estimated waste generation in kilograms
- Population-based prediction inputs
- Historical waste trend visualization
- Interactive graphs using Chart.js
- Future waste generation estimates
- Environmental news integration
- Model performance evaluation

**Machine Learning Algorithm:** Linear Regression

**Libraries:** Scikit-learn, Pandas, NumPy

**Dataset:** Synthetic Indian waste-generation data used for demonstration purposes.

The synthetic dataset can be replaced with verified Indian municipal waste statistics in future versions.

### ♻️ Module 2 — AI Waste Image Scanner

An intelligent waste classification system using **OpenCV and MobileNetV2**.

Users can upload images of waste items and receive AI-generated classification results.

#### Supported Waste Categories

1. Cardboard
2. E-Waste
3. General Waste
4. Glass
5. Metal
6. Organic Waste
7. Paper
8. Plastic

#### Features

- Image upload interface
- OpenCV-based image preprocessing
- MobileNetV2 deep learning classification
- Top three predicted categories
- Model confidence scores
- Uncertain classification handling
- Recycling recommendations
- Waste disposal guidance

The classifier uses a trained neural network rather than hardcoded predictions.

### 🤖 Module 3 — Eco AI Chatbot

Eco AI is an environmental assistant integrated with the **Google Gemini API**.

It is designed to provide contextual answers about environmental sustainability and waste management.

#### Features

- Google Gemini API integration
- Natural-language conversations
- Hindi, English and Hinglish support
- Conversation history support
- Waste segregation guidance
- Plastic recycling information
- E-waste disposal guidance
- Composting and organic waste education
- Environmental awareness
- Automatic retry for temporary API server errors
- Offline knowledge-base fallback

The chatbot uses the Google GenAI Python SDK.

When Gemini is unavailable, EcoScanPro provides a clearly labeled offline knowledge-base response.

**Note:** The Gemini integration has been configured, but successful live responses depend on API model availability, quota and service status.

---

## 🛠️ Technology Stack

| Component | Technologies |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python, Flask |
| Machine Learning | Scikit-learn |
| Deep Learning | TensorFlow, Keras |
| Image Classification | MobileNetV2 |
| Computer Vision | OpenCV |
| AI Chatbot | Google Gemini API |
| AI SDK | Google GenAI |
| Data Processing | Pandas, NumPy |
| Data Visualization | Chart.js |
| Model Storage | Joblib, Keras |
| Environmental News | RSS Feeds |
| Deployment | Render |
| Version Control | Git, GitHub |

---

## 📂 Project Structure

```text
EcoScanPro/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
├── data/
│   ├── waste_images/
│   ├── held_out_validation/
│   ├── held_out_test/
│   └── waste_guidelines.json
│
├── ml/
│   ├── generate_dataset.py
│   ├── train_regression.py
│   ├── train_classifier.py
│   ├── evaluate_models.py
│   └── predict.py
│
├── models/
│   ├── waste_classifier.keras
│   ├── waste_classifier_classes.json
│   └── waste_regression.joblib
│
├── routes/
│   ├── prediction.py
│   ├── classification.py
│   ├── chatbot.py
│   └── news.py
│
├── services/
│   ├── image_processing.py
│   ├── chatbot_service.py
│   └── news_service.py
│
├── templates/
│   ├── index.html
│   ├── prediction.html
│   ├── scanner.html
│   ├── chatbot.html
│   └── about.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── tests/
```

Some datasets and trained model artifacts may be excluded from GitHub because of their size.

---

## 📊 Dataset Sources

EcoScanPro uses publicly available image datasets for waste classification.

### 1. TrashNet Dataset

**Source:** https://github.com/garythung/trashnet

TrashNet provides labeled images of common waste materials.

| Category | Images |
|---|---:|
| Cardboard | 403 |
| Glass | 501 |
| Metal | 410 |
| Paper | 594 |
| Plastic | 482 |
| General Waste | 137 |
| **Total** | **2,527** |

The original TrashNet `trash` category is mapped to `General Waste`.

### 2. AlphaTrash Dataset

**Source:** https://github.com/Patipol-BKK/alphatrash-dataset

Used for Organic Waste classification.

**Total Organic Waste Images:** 819

Original dataset partitions:

- Training: 574 images
- Validation: 123 images
- Testing: 122 images

### 3. TrashBox Dataset

**Source:** https://github.com/nikhilvenkatkumsetty/TrashBox

Used for E-Waste classification.

**Total E-Waste Images:** 2,405

The dataset includes images of:

- Smartphones
- Laptops
- Electrical cables
- Electronic chips
- Small electronic appliances

### Combined Dataset Summary

| Category | Images |
|---|---:|
| Cardboard | 403 |
| E-Waste | 2,405 |
| General Waste | 137 |
| Glass | 501 |
| Metal | 410 |
| Organic Waste | 819 |
| Paper | 594 |
| Plastic | 482 |
| **Total** | **5,751** |

### Dataset Preparation

The preparation pipeline included:

1. Downloading public datasets.
2. Organizing images into eight waste categories.
3. Separating training, validation and test images.
4. Checking exact duplicates using SHA-256.
5. Removing three cross-split training duplicates.
6. Converting training images to standard RGB JPEG format.
7. Preparing images for MobileNetV2 classification.

#### Dataset Partition Summary

| Partition | Images |
|---|---:|
| Training Pool | 4,766 |
| Reserved Organic Validation | 123 |
| Held-Out Test | 859 |
| **Total After Cleanup** | **5,748** |

The training script also creates an internal validation split from its training pool.

The reserved held-out test images have not yet been reported as an independently evaluated final test result.

Dataset licenses and attribution requirements should be reviewed before redistribution or commercial use.

---

## 🧠 Machine Learning Architecture

### Linear Regression

Linear Regression is used to estimate waste generation from numerical and demographic input features.

The trained regression model is stored in:

`models/waste_regression.joblib`

### MobileNetV2

MobileNetV2 is used for image-based waste classification.

The current trained model uses transfer learning with pretrained ImageNet weights.

#### Model Configuration

| Parameter | Value |
|---|---|
| Architecture | MobileNetV2 |
| Input Size | 224 × 224 |
| Output Classes | 8 |
| Batch Size | 16 |
| Epochs | 8 |
| Optimizer | Adam |
| Loss | Sparse Categorical Crossentropy |
| Transfer Learning | ImageNet pretrained backbone |
| Classification Head | Trainable |
| Backbone | Frozen in recorded training run |

### Training Results

| Metric | Result |
|---|---:|
| Training Accuracy | 98.95% |
| Validation Accuracy | 90.87% |
| Training Epochs | 8 |
| Waste Categories | 8 |
| Independent Test Accuracy | Not yet evaluated |

These metrics are from the recorded training run and do not represent guaranteed accuracy on real-world images.

### Known Limitations

The model may incorrectly classify unfamiliar objects or waste items that are poorly represented in the training datasets.

For example, a transparent phone case was classified as E-Waste with high confidence.

Future improvements include:

- Class balancing
- Additional real-world training images
- Fine-tuning MobileNetV2 layers
- Better unknown-object handling
- Independent per-category evaluation
- Confusion matrix analysis

---

## 🤖 Google Gemini AI Integration

EcoScanPro uses the Google GenAI Python SDK to communicate with Gemini.

### Chatbot Architecture

```text
User Message
     |
     v
Flask Chat API
     |
     v
chatbot_service.py
     |
     v
Google Gemini API
     |
     +---- Successful Response
     |          |
     |          v
     |      Eco AI Reply
     |
     +---- API Failure
                |
                v
       Knowledge-Base Fallback
```

### Chatbot Capabilities

- Context-aware environmental conversations
- Previous-message history
- Multilingual responses
- Environmental knowledge-base grounding
- Limited retries on temporary server failures
- Offline fallback when the AI provider is unavailable

### API Configuration

Create a `.env` file in the project root.

```env
SECRET_KEY=YOUR_RANDOM_SECRET
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_MODEL=gemini-3.5-flash-lite
NEWS_CACHE_SECONDS=1800
MAX_CONTENT_LENGTH_MB=8
```

The Gemini model name is configurable and should be selected from models supported by the API project.

**Security:** Never upload `.env` or API credentials to GitHub.

---

## 💻 Installation and Setup

### Step 1 — Clone Repository

```bash
git clone https://github.com/Prince-Bisht/EcoScanPro.git
cd EcoScanPro
```

### Step 2 — Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

For Windows:

```bash
.venv\Scripts\activate
```

### Step 3 — Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Ensure the requirements include the Google GenAI SDK:

```text
google-genai
```

### Step 4 — Configure Environment Variables

Create a `.env` file and configure the Gemini API key and other required settings.

### Step 5 — Run Flask Application

```bash
python app.py
```

Open the application:

https://ecoscanpros.onrender.com

### Application Pages

| Page | URL |
|---|---|
| Home | `/` |
| Waste Prediction | `/prediction` |
| AI Waste Scanner | `/scanner` |
| Eco AI Chatbot | `/chatbot` |

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/classify-waste` | Waste image classification |
| POST | `/api/chat` | Eco AI chatbot |
| GET | `/api/health` | Application health |

Additional routes support waste prediction and environmental news.

---

## ☁️ Render Deployment

EcoScanPro is designed to be deployable as a Python web service on Render.

### Deployment Steps

1. Push the source code to GitHub.
2. Open https://dashboard.render.com/
3. Select **New Web Service**.
4. Connect the EcoScanPro GitHub repository.
5. Select Python as the runtime.
6. Configure the build and start commands.
7. Add environment variables.
8. Deploy the web service.

### Render Configuration

| Setting | Value |
|---|---|
| Service Name | ecoscanpro |
| Runtime | Python |
| Branch | main |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app --bind 0.0.0.0:$PORT` |

Ensure `gunicorn` is installed through `requirements.txt`.

### Render Environment Variables

Configure the following through the Render dashboard:

```text
SECRET_KEY
GEMINI_API_KEY
GEMINI_MODEL
NEWS_CACHE_SECONDS
MAX_CONTENT_LENGTH_MB
```

### Deployment Considerations

- Render uses a Linux environment.
- Use Linux-compatible Python dependencies.
- Prefer `opencv-python-headless` for server deployment.
- Ensure trained model files are available at runtime.
- Large TensorFlow models may require additional hosting resources.
- Never commit private API keys.
- Configure the Gemini API key through Render environment settings.
- Test all three modules after deployment.

---

## 🔒 Security and Privacy

EcoScanPro uses or is designed to support:

- Environment-based API credentials
- Flask request validation
- File upload restrictions
- Backend image processing
- API error handling
- Safe AI fallback behavior
- Separation of frontend and backend API credentials

Production deployments should include appropriate security testing and resource limits.

---

## 🔮 Future Improvements

- MobileNetV2 fine-tuning
- Improved classification accuracy
- Additional Indian waste datasets
- Official municipal waste statistics
- Better AI confidence calibration
- Dedicated e-waste accessory detection
- Real-time environmental monitoring
- Location-specific recycling recommendations
- Cloud model optimization
- Independent test-set evaluation
- Improved chatbot reliability
- More interactive sustainability dashboards

---

## 📚 References

### Datasets

- TrashNet: https://github.com/garythung/trashnet
- AlphaTrash: https://github.com/Patipol-BKK/alphatrash-dataset
- TrashBox: https://github.com/nikhilvenkatkumsetty/TrashBox

### Technologies

- TensorFlow: https://www.tensorflow.org/
- Keras: https://keras.io/
- Scikit-learn: https://scikit-learn.org/
- OpenCV: https://opencv.org/
- Flask: https://flask.palletsprojects.com/
- Google Gemini API: https://ai.google.dev/
- Render: https://ecoscanpros.onrender.com

---

## ⚠️ Disclaimer

EcoScanPro is an educational AI project.

Waste prediction currently uses synthetic demonstration data. Image classification results are experimental and may be incorrect.

AI-generated responses should not replace official municipal waste-management regulations or professional environmental guidance.

---

### 🌱 EcoScanPro
**Predict Waste. Classify Smarter. Build a Sustainable Future.**
