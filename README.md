***PRODUCT UNDERCONSTRUCTION***
SafetyKitDetection/
│── backend/
│   ├── models/                         # Trained YOLO model stored here
│   │   ├── best.pt                     # Your YOLO trained model
│   ├── uploads/                        # Uploaded images/videos will be stored here
│   ├── processed/                      # Processed output images/videos stored here
│   ├── reports/                        # Generated reports for each detection
│   ├── main.py                         # FastAPI backend script
│   ├── detection.py                     # YOLO model processing script
│   ├── requirements.txt                 # Dependencies
│── frontend/
│   ├── index.html                       # Main HTML file
│   ├── first.css                         # Stylesheet
│   ├── safety4.js                        # JavaScript logic for frontend
│   ├── assets/                          # Static files (images, icons, etc.)
│   │   ├── helmet.png
│   │   ├── gloves.png
│   │   ├── ...
│── README.md                            # Project documentation
│── .gitignore                           # Files to ignore in Git
