from pathlib import Path

import joblib


BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "model_ml"


class ModelPredict:
    def __init__(self):
        self.__naive_bayes_loaded = joblib.load(MODEL_DIR / "naive_bayes_model.pkl")
        self.__svm_loaded = joblib.load(MODEL_DIR / "SVM_model.pkl")
        self.__vectorizer = joblib.load(MODEL_DIR / "vectorizer.pkl")

    def __vectorizer_text(self, text):
        return self.__vectorizer.transform([text])
    
    def __sentiments_text(self, predicted_val):
        if predicted_val[0] == 1:
            return "POSITIF"
        return "NEGATIF"

    def model_predict_nvm(self, text):
        temp_vec = self.__vectorizer_text(text)
        return self.__sentiments_text(self.__naive_bayes_loaded.predict(temp_vec))
    
    def model_predict_svm(self, text):
        temp_vec = self.__vectorizer_text(text)
        return self.__sentiments_text(self.__svm_loaded.predict(temp_vec))
    
