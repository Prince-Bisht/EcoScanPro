
# 🌱 EcoScanPro — AI-Powered Smart Waste Management System

**EcoScanPro** is an AI-powered smart waste management web application developed using Python, Flask, Machine Learning, Deep Learning, and Computer Vision.

The project aims to improve waste management through waste generation prediction, image-based waste classification, and AI-assisted environmental education.

> **Project Status:** Functional college demonstration project. Machine learning predictions are experimental and should not be treated as verified municipal waste-management decisions.

## 🚀 Live Website

**Deployment Platform:** Render

**Website:** https://YOUR-SERVICE-NAME.onrender.com

Replace the above URL with the actual Render deployment link once the application is successfully deployed.

## ✨ Key Features

### 1. AI Waste Generation Prediction

Predicts estimated waste generation in kilograms per day using Linear Regression.

**Features:**
- Indian city-based waste prediction
- Population and urbanization-based inputs
- Historical waste generation trends
- Future waste projections
- Interactive Chart.js graphs
- Model evaluation using MAE, RMSE, and R²
- Live environmental news integration

**Dataset:** Synthetic Indian waste-generation data.

The initial dataset is generated for demonstration purposes and is not official Indian government data.

### 2. AI Waste Image Classification

Uses OpenCV for image preprocessing and MobileNetV2 for deep learning-based waste classification.

**Supported Categories:**

1. Cardboard
2. E-Waste
3. General Waste
4. Glass
5. Metal
6. Organic Waste
7. Paper
8. Plastic

**Features:**
- Image upload
- OpenCV preprocessing
- MobileNetV2 classification
- Top three predicted categories
- Model confidence scores
- Uncertainty detection
- Waste disposal recommendations
- Recycling guidance

The classifier uses a trained neural network rather than random or hardcoded predictions.

### 3. Eco AI Chatbot

An environmental assistant designed to answer questions about:

- Recycling
- Waste segregation
- Plastic pollution
- E-waste
- Composting
- Sustainable living
- Waste management in India

The chatbot supports configurable LLM API integration.

If an LLM API is unavailable, the application uses a clearly labeled environmental knowledge-base fallback.

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python, Flask |
| Waste Prediction | Scikit-learn Linear Regression |
| Computer Vision | OpenCV |
| Deep Learning | TensorFlow, Keras |
| Image Classifier | MobileNetV2 |
| Data Processing | Pandas, NumPy |
| Graphs | Chart.js |
| Model Storage | Joblib, Keras |
| Environmental News | RSS / News API |
| Deployment | Render |
| Version Control | Git, GitHub |

## 📊 Waste Classification Datasets

EcoScanPro V2 uses three publicly available waste-image dataset sources.

### Dataset 1 — TrashNet

**Source:** https://github.com/garythung/trashnet

TrashNet provides images of six waste categories.

| Category | Images |
|---|---:|
| Cardboard | 403 |
| Glass | 501 |
| Metal | 410 |
| Paper | 594 |
| Plastic | 482 |
| General Waste | 137 |
| **Total** | **2,527** |

The original `trash` category is mapped to `General Waste`.

### Dataset 2 — AlphaTrash

**Source:** https://github.com/Patipol-BKK/alphatrash-dataset

Used for Organic Waste classification.

**Images collected:** 819

Original dataset splits:

- Training: 574 images
- Validation: 123 images
- Testing: 122 images

### Dataset 3 — TrashBox

**Source:** https://github.com/nikhilvenkatkumsetty/TrashBox

Used for E-Waste classification.

The dataset includes electronic waste images such as:

- Smartphones
- Laptops
- Electrical cables
- Small appliances
- Electronic chips

**Images collected:** 2,405

### Combined Dataset

| Category | Original Images |
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

Dataset images were organized into eight waste categories for model training.

Original dataset licenses and attribution requirements should be checked before redistribution or commercial deployment.

## 🧹 Dataset Preparation

The dataset preparation process included:

1. Downloading public waste-image datasets.
2. Organizing images into eight categories.
3. Separating training, validation, and test images.
4. Detecting exact duplicate images using SHA-256 hashing.
5. Removing three training images duplicated across splits.
6. Normalizing training images to RGB JPEG format.
7. Preparing images for MobileNetV2.

### Dataset Split

After duplicate cleanup:

| Dataset Partition | Images |
|---|---:|
| Training pool | 4,766 |
| Reserved Organic validation | 123 |
| Held-out test | 859 |
| **Total** | **5,748** |

The training script additionally creates its own validation subset from the training pool.

The 859 held-out test images are reserved for independent evaluation.

**Note:** Exact duplicate removal does not guarantee the absence of visually similar images or mislabeled samples.

## 🧠 Machine Learning Models

### Linear Regression

Used for waste generation prediction.

Linear Regression models relationships between waste generation and numerical or encoded demographic features.

The regression model is stored as:

`models/waste_regression.joblib`

### MobileNetV2

Used for image-based waste classification.

MobileNetV2 is a lightweight convolutional neural network architecture suitable for transfer learning.

**Current training configuration:**

- Input resolution: 224 × 224
- Batch size: 16
- Training epochs: 8
- Optimizer: Adam
- Loss: Sparse Categorical Crossentropy
- Pretrained ImageNet weights
- Frozen MobileNetV2 backbone
- Trainable classification head

The current recorded training run uses feature extraction. Additional fine-tuning and class balancing remain possible improvements.

## 📈 Model Training Results

The eight-category MobileNetV2 model completed training successfully.

| Metric | Recorded Result |
|---|---:|
| Final Training Accuracy | 98.95% |
| Final Validation Accuracy | 90.87% |
| Completed Epochs | 8 |
| Output Classes | 8 |
| Independent Test Accuracy | Pending evaluation |

These are training-run metrics, not verified real-world classification accuracy.

Softmax confidence scores should not be interpreted as guaranteed probabilities of correctness.

### Known Classification Limitations

The classifier can misclassify unfamiliar objects.

For example, a transparent phone cover was classified as E-Waste with high model confidence, although the item is likely a plastic-based accessory.

Possible contributing factors include:

- Class imbalance
- Limited training diversity
- Dataset-specific backgrounds
- Missing object variations
- Neural network overconfidence

Future model improvements should be evaluated using independent test images and real-world examples.

## 📁 Project Structure

```text
EcoScanPro/
|
|-- app.py
|-- requirements.txt
|-- README.md
|-- .env.example
|-- .gitignore
|
|-- data/
|   |-- indian_waste_data.csv
|   |-- waste_guidelines.json
|   |-- waste_images/
|   |-- held_out_validation/
|   |-- held_out_test/
|
|-- ml/
|   |-- generate_dataset.py
|   |-- train_regression.py
|   |-- train_classifier.py
|   |-- evaluate_models.py
|   |-- predict.py
|
|-- models/
|   |-- waste_regression.joblib
|   |-- waste_classifier.keras
|   |-- waste_classifier_classes.json
|
|-- routes/
|   |-- prediction.py
|   |-- classification.py
|   |-- chatbot.py
|   |-- news.py
|
|-- services/
|   |-- image_processing.py
|   |-- chatbot_service.py
|   |-- news_service.py
|
|-- templates/
|   |-- index.html
|   |-- prediction.html
|   |-- scanner.html
|   |-- chatbot.html
|   |-- about.html
|
|-- static/
|   |-- css/
|   |-- js/
|   |-- images/
|
|-- tests/
```

Training datasets and generated model files may not be included in the GitHub repository. They must be made available separately when required.

## 💻 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/EcoScanPro.git
cd EcoScanPro
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

For local classifier training, install a compatible TensorFlow version if it is not already included.

### 4. Configure environment variables

Create a `.env` file using `.env.example` as a reference.

Configure the chatbot and news API credentials if those services are required.

Never commit `.env` or secret API keys to GitHub.

### 5. Run the application

```bash
python app.py
```

Open:

http://127.0.0.1:5000

## 🏋️ Training the Models

### Train Waste Regression

```bash
python ml/train_regression.py
```

### Train Waste Classifier

Ensure the eight labeled image-category folders are available under:

`data/waste_images/`

Then run:

```bash
python ml/train_classifier.py
```

The training script saves:

- `models/waste_classifier.keras`
- `models/waste_classifier_classes.json`

The model and class mapping must be deployed together.

## 🔌 Backend API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/classify-waste` | Classify an uploaded waste image |
| POST | `/api/chat` | Send a message to Eco AI |
| GET | `/api/health` | Check application health |

Additional prediction and news endpoints are implemented through their respective Flask route modules.

## ☁️ Deployment on Render

EcoScanPro can be deployed using a Render Python Web Service.

### Deployment Steps

1. Upload the application source code to GitHub.
2. Open https://dashboard.render.com/
3. Create a new Web Service.
4. Connect the GitHub repository.
5. Select Python as the runtime.
6. Configure the build and start commands.
7. Add required environment variables.
8. Deploy the application.

### Recommended Render Configuration

| Setting | Value |
|---|---|
| Service Name | ecoscanpro |
| Runtime | Python |
| Branch | main |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app --bind 0.0.0.0:$PORT` |

Ensure `gunicorn` is included in `requirements.txt`.

### Important Deployment Notes

- Render runs on Linux, so dependencies must be compatible with its runtime.
- Use `opencv-python-headless` for server-side image processing.
- The trained Keras model must be available on the server.
- Large model files may require Git LFS or external artifact storage.
- TensorFlow may exceed the memory limits of some hosting plans.
- Never upload API keys or local virtual environments.
- Dataset repositories are not required at runtime once the trained model is available.

## 🔐 Security

The application includes or is designed to support:

- Image upload size restrictions
- File extension and content validation
- Environment-based API credentials
- Backend request validation
- Error handling
- Secure model inference
- Safe frontend rendering

Additional security testing is recommended before production deployment.

## 🔮 Future Enhancements

- MobileNetV2 fine-tuning
- Better class balancing
- Expanded real-world training datasets
- Dedicated mouse and electronic accessory examples
- Improved unknown-object detection
- Independent confusion-matrix evaluation
- City-wise AQI integration
- Official Indian municipal waste datasets
- Location-specific recycling guidance
- Optimized cloud model inference
- Model monitoring and retraining

## 📚 References and Credits

1. TrashNet — https://github.com/garythung/trashnet
2. AlphaTrash — https://github.com/Patipol-BKK/alphatrash-dataset
3. TrashBox — https://github.com/nikhilvenkatkumsetty/TrashBox
4. TensorFlow — https://www.tensorflow.org/
5. Scikit-learn — https://scikit-learn.org/
6. OpenCV — https://opencv.org/
7. Flask — https://flask.palletsprojects.com/
8. Render — https://render.com/

## 📌 Project Disclaimer

EcoScanPro is an educational and experimental AI-based waste management system.

Waste generation estimates currently use synthetic demonstration data. Waste image classifications are model predictions and may be incorrect.

The system should not replace official municipal recycling instructions or professional waste-management guidance.

---

**EcoScanPro — Smarter Waste Management, Powered by Artificial Intelligence.**
