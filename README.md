# 🥃 WHISKY-GOGGLES

> **An advanced AI-powered whisky recognition system that seamlessly blends computer vision, NLP, OCR, and domain expertise to identify whisky bottles with exceptional accuracy.**

## 🌟 Overview

WHISKY-GOGGLES represents a significant advancement in specialized image recognition technology. By combining multiple AI modalities with whisky domain expertise, the system achieves remarkable accuracy in identifying whisky bottles from images, even in challenging real-world conditions.

This project demonstrates how purpose-built, domain-specific image recognition can outperform general-purpose solutions through architectural innovation and intelligent decision-making processes.

## 🧠 Technical Innovation: The Dual-Pipeline Architecture

At the heart of WHISKY-GOGGLES lies a revolutionary approach to image recognition that overcomes the limitations of traditional single-method systems:

```
USER IMAGE
    │
    ▼
┌─────────────────┐
│  PREPROCESSING  │──────────────────┐
└─────────────────┘                  │
    │                                │
    ▼                                ▼
┌─────────────────┐          ┌─────────────────┐
│   CLIP ENGINE   │          │   OCR ENGINE    │
│                 │          │                 │
│ ┌─────────────┐ │          │ ┌─────────────┐ │
│ │ CLIP Model  │ │          │ │  EasyOCR    │ │
│ └─────────────┘ │          │ └─────────────┘ │
│        │        │          │        │        │
│        ▼        │          │        ▼        │
│ ┌─────────────┐ │          │ ┌─────────────┐ │
│ │FAISS Search │ │          │ │Text Cleaning│ │
│ └─────────────┘ │          │ └─────────────┘ │
└────────│────────┘          └────────│────────┘
         │                            │
         └────────────┬───────────────┘
                      │
              ┌───────▼───────┐
              │  LLM MEDIATOR │
              │  (LangGraph)  │
              └───────┬───────┘
                      │
              ┌───────▼───────┐
              │  BM25 SEARCH  │
              └───────┬───────┘
                      │
                      ▼
             FINAL RESULT WITH 
               METADATA AND
             CONFIDENCE SCORE
```

### 1️⃣ The CLIP Engine: Visual Intelligence

The CLIP engine leverages OpenAI's powerful vision-language model:
- **Embedding Database**: Pre-embedded collection of 500+ high-quality whisky bottle images
- **FAISS Similarity Search**: Lightning-fast vector search identifies visual matches
- **Confidence Scoring**: Sophisticated algorithm assigns reliability scores to each match

### 2️⃣ The OCR Engine: Textual Precision

The OCR pipeline extracts and processes text with domain-specific optimizations:
- **Custom Preprocessing**: Specialized image enhancement for whisky label clarity
- **Text Extraction**: EasyOCR with fine-tuned parameters for bottle text
- **Noise Reduction**: Advanced filtering of irrelevant text and OCR artifacts

### 3️⃣ The LLM Mediator: Intelligent Decision-Making

The LangGraph-powered mediator is the breakthrough component that elevates WHISKY-GOGGLES beyond existing systems:
- **Decision Engine**: Analyzes and weighs evidence from both pipelines
- **Domain Expertise**: Incorporates whisky-specific knowledge to resolve ambiguities
- **Confidence Assessment**: Provides realistic confidence scores based on evidence quality

### 4️⃣ BM25 Metadata Retrieval: Precision Matching

Unlike systems that rely on fuzzy matching, our precision-focused BM25 implementation ensures:
- **Exact Brand Matching**: Distinguishes between similarly named whiskies
- **Detail Preservation**: Captures age statements, cask types, and special editions
- **Comprehensive Metadata**: Returns rich information about each identified bottle

## 🚀 API Endpoints 

WHISKY-GOGGLES offers two powerful endpoints:

### `/recognize` - Direct Image Upload

### `/recognize_url` - accepts image url


### Response Format
see localhost:8000/docs


## ⚙️ Implementation Details

### Project Structure

```
whisky-goggles/
├── .cache/                  # Cache directory
├── app/                     # Main application
│   ├── __pycache__/         # Python cache
│   ├── api/                 # API endpoints
│   ├── core/                # Core business logic
│   │   ├── clip_engine.py   # CLIP-based recognition
│   │   ├── ocr_engine.py    # OCR-based recognition
│   │   ├── mediator.py      # LangGraph mediator
│   │   └── metadata.py      # BM25 metadata retrieval
│   ├── models/              # ML models and data structures
│   ├── utils/               # Utility functions
│   ├── config.py            # Configuration
│   └── main.py              # Application entry point
├── data/                    # Whisky image and metadata collections
├── frontend/                # Pre-built React frontend
├── scripts/                 # Utility scripts
├── venv/                    # Virtual environment
├── .env                     # Environment variables
├── .env.example             # Environment template
├── .python-version          # Python version
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile               # Docker configuration
├── README.md                # This documentation
├── requirements.lock.txt    # Locked dependencies
├── requirements.txt         # Project dependencies
└── yolov8n.pt              # YOLOv8 model file
```

### Key Technologies

- **FastAPI**: High-performance API framework with automatic Swagger documentation
- **CLIP**: OpenAI's powerful vision-language model for visual similarity
- **EasyOCR**: Optimized text extraction with multiple language support
- **LangGraph**: Advanced agent orchestration for the LLM mediator's decision flow
- **FAISS**: Facebook AI's efficient similarity search for embedding matching
- **BM25**: Precision text matching algorithm for metadata retrieval
- **React**: Modern frontend interface with responsive design
- **Docker**: Containerized deployment for consistent environments

## 💻 Getting Started

### Start by cloning this repo
```bash
git clone https://github.com/tsmboa0/whisky-goggles.git
```
Cd into the directory

```bash
cd whisky-goggles
```

create and activate a virtual environment e.g venv
```bash
python3 -m venv venv
```
Activate your venv
```bash
source venv/bin/activate
```
install all packages
```bash
pip install -r requirements.txt
```
Install frontend packages and build
```bash
cd frontend/
npm i
npm run build
```
Create a .env file and copy the .env.example file into it. Remember to get your GROQ/OPENAI API Key

### Get your Google Credentials (to be able to use Google Vision API)

Step 1: Enable Cloud Vision API

1: Go to: https://console.cloud.google.com
2: Create or select a project.
3: Navigate to APIs & Services > Library
4: Search for “Cloud Vision API” and click Enable

STEP 2: Create a Service Account

1: Go to: IAM & Admin > Service Accounts
2: Click “Create Service Account”
3: Give it a name (e.g., vision-reader) → Continue
4: Assign the role: Project > Editor or Cloud Vision API User
5: Click Done
6: Go to the created service account → Keys tab → Add Key > JSON

📦 This will download a JSON file — your credentials file.

Ensure you activate billing for your google account. (you have free API calls, so you won't be charged)

Open your .env file and add the path to the downloaded credentials.json file

GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"

start your server
```bash
uvicorn app.main:app --reload
```

Visit http://127.0.0.1:8000/ to interact with the application

Note: depending on your machine, you may need to pay attention to your terminal to see what variable to add to path.
```


### You can aslo check the scripts/ folder to see how to train new dataset from a new metadata.csv file

## 🔍 User Experience

When interacting with WHISKY-GOGGLES, users experience a seamless journey:

1. **Upload or URL** — Submit an image through the elegant React interface or API
2. **Instant Processing** — Real-time processing with visual feedback (~1-2 seconds)
3. **Confidence-Scored Results** — Accurate identification with transparency about confidence
4. **Rich Metadata** — Comprehensive details about the identified whisky

## 🔮 Applications and Use Cases

WHISKY-GOGGLES provides a foundation for numerous practical applications:

- **Retail and E-commerce**: Instant product identification for pricing and inventory
- **Collection Management**: Help enthusiasts catalog and manage their collections
- **Authentication**: Verify bottles at auctions and secondary markets
- **Educational Tool**: Help newcomers learn about whiskies they encounter
- **Market Research**: Analyze whisky trends and consumer preferences

## 🛠️ Technical Achievements

Several technical innovations make WHISKY-GOGGLES particularly noteworthy:

### Multi-Modal Fusion
The system demonstrates how combining visual and textual modalities can create recognition capabilities greater than the sum of their parts. By leveraging the strengths of each approach, WHISKY-GOGGLES achieves superior accuracy compared to single-modality systems.

### LLM as Intelligent Mediator
Rather than using an LLM merely for classification, WHISKY-GOGGLES employs it as a reasoning engine that makes informed decisions based on evidence from multiple sources. This approach mimics human expert reasoning and significantly improves accuracy in edge cases.

### Domain-Specific Optimization
Every component has been fine-tuned specifically for whisky bottle recognition, from preprocessing steps that enhance label visibility to OCR parameters optimized for whisky typography. This domain focus yields substantial performance improvements over general-purpose recognition systems.

### Production-Ready Implementation
Unlike many proof-of-concept AI systems, WHISKY-GOGGLES is fully production-ready with Docker containerization, comprehensive API documentation, and an integrated frontend application.

## 📈 Future Development

The WHISKY-GOGGLES architecture provides a solid foundation for future enhancements:

- **Expanded Database**: Growing the reference database beyond the current 500 bottles
- **Mobile Optimization**: Adapting the system for mobile-first deployment
- **Offline Capability**: Implementing a smaller model for edge deployment
- **Multilingual Support**: Enhancing OCR capabilities for international whisky labels
- **Transfer Learning**: Adapting the architecture to other bottle recognition domains (wine, spirits, etc.)


WHISKY-GOGGLES demonstrates how purpose-built AI systems with domain-specific architectures can achieve exceptional performance in specialized recognition tasks. By combining multiple AI modalities with intelligent decision-making, this system sets a new standard for what's possible in the field of product recognition.

## 📬 License
MIT
