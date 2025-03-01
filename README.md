# Energy Consumption and Prediction Model

## Overview
This project focuses on predicting energy consumption using machine learning techniques and provides an interactive Streamlit application for user-friendly predictions. The repository includes a Jupyter Notebook (`energy_prediction_model.ipynb`) for model training and an application script (`app.py`) for real-time energy consumption analysis.

## Features
- Data preprocessing and cleaning
- Exploratory data analysis (EDA)
- Feature selection and engineering
- Machine learning model training and evaluation
- Streamlit-based interactive web application for predictions
- Performance metrics visualization

## Requirements
To run this project, install the following dependencies:

```bash
pip install numpy pandas scikit-learn matplotlib seaborn jupyter streamlit joblib
```

## Usage
### Running the Jupyter Notebook
1. Clone this repository:
   ```bash
   git clone https://github.com/harshitharajesh19/Energy-Consumption-and-prediction.git
   ```
2. Navigate to the project folder:
   ```bash
   cd Energy-Consumption-and-prediction
   ```
3. Open Jupyter Notebook:
   ```bash
   jupyter notebook
   ```
4. Open `energy_prediction_model.ipynb` and run the cells step by step.

### Running the Streamlit App
1. Ensure the trained models (`linear_model.pkl`, `ridge_model.pkl`, and `feature_names.pkl`) are available in the project directory.
2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
3. Open the provided localhost URL in your browser to interact with the application.

## Dataset
The model requires an energy consumption dataset. Ensure the dataset is placed in the project directory and properly referenced in the notebook.
[Download Dataset](https://drive.google.com/file/d/10I4ZW_4Cnh1Yqi82ew4Od7I6ezzgOXxw/view?usp=sharing)

## Model Training
The notebook walks through the process of loading data, preprocessing, training a machine learning model, and evaluating its performance using various metrics such as RMSE, MAE, and R² score.

## Streamlit Application
The `app.py` file contains a Streamlit-based web interface allowing users to input various parameters and receive energy consumption predictions using trained machine learning models.

## Results
After training the model, the notebook generates various plots and performance evaluations to help analyze the prediction accuracy. The Streamlit app also provides real-time predictions based on user inputs.

## Contributing
Contributions are welcome! Feel free to fork this repository and submit a pull request with improvements or new features.

## License
This project is licensed under the MIT License.

---

**Author:** M.Harshitha  
**GitHub:** [harshitharajesh19](https://github.com/harshitharajesh19)

