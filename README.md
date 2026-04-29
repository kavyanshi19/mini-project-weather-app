 Weather Prediction App

A Python-based weather application built using Streamlit that provides weather data visualization and predictive insights using a trained model.

 Project Structure

project-folder/
│
├── streamlit_india_weather.py   # Streamlit application
├── README.md                    # Documentation
│
└── model/
    ├── train_model.py           # Training script& code
 Features

-  Interactive user interface using Streamlit
-  Weather data visualization
- Prediction system based on trained model
-  Modular structure (training, prediction, app separated)
-  Fast performance using pre-saved model


Technologies Used

- Python
- Streamlit
- scikit-learn
- Requests
- Pillow
- Matplotlib


Installation & Setup

1. Clone the repository:

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

2. Install dependencies:

pip install -r requirements.txt

3. Run the application:

streamlit run streamlit_india_weather.py

---
 Prediction System

- The model is trained using "train_model.py"
- Predictions are handled using "predict.py"
- The Streamlit app loads the model and displays results

---

 Notes

- If the model file is large, it may not be included in the repository

Future Improvements

- Improve user interface
- Add real-time weather API integration
- Deploy the application online
- Enhance prediction accuracy


 Author

Kavyanshi Agarwal
Yashika Tiwari
Bhumika