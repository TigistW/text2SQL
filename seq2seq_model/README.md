### 📌 Purpose

This notebook prepares and augments natural language data through **cleaning, normalization, and paraphrasing**. The processed outputs are intended to improve the robustness and generalization of downstream NLP models such as Text-to-SQL systems.

### 🔍 What This Notebook Does

* Loads raw natural language query data
* Cleans and normalizes text (lowercasing, punctuation handling, spacing, etc.)
* Applies paraphrasing techniques to generate alternative user queries
* Expands the dataset with semantically equivalent sentences
* Saves or outputs processed data for later model training

### 🧠 Why It Matters

Paraphrasing helps the model:

* Handle linguistic variation in user queries
* Generalize beyond memorized sentence patterns
* Perform better on real-world, unseen inputs

### 📤 Output

* A cleaned and augmented dataset of natural language queries
* Data formatted for direct use in model training

---

## 2️⃣ TextToSQL_enc_dec.ipynb

### 📌 Purpose

This notebook implements a **Text-to-SQL system** using an **Encoder–Decoder neural architecture**, enabling the translation of natural language questions into executable SQL queries.

### 🔍 What This Notebook Does

* Loads preprocessed natural language–SQL pairs
* Tokenizes and encodes input text and SQL queries
* Builds an encoder–decoder model (sequence-to-sequence)
* Trains the model on the dataset
* Evaluates model performance on validation/test data
* Demonstrates inference: NL query → SQL query

### 🧠 Key Concepts Used

* Sequence-to-sequence learning
* Encoder–decoder architecture
* Tokenization and vocabulary building
* Teacher forcing (if applicable)
* Loss tracking and evaluation

### 📤 Output

* A trained Text-to-SQL model
* Predicted SQL queries for given natural language inputs
* Training metrics such as loss curves

---

## 🔗 Workflow Overview

```
Natural Language Queries
        ↓
DataProcessing_Paraphrase.ipynb
        ↓
Augmented & Cleaned Dataset
        ↓
TextToSQL_enc_dec.ipynb
        ↓
Natural Language → SQL Queries
```

---

## 🛠️ Requirements

Common dependencies include:

* Python 3.x
* Jupyter Notebook
* NumPy
* Pandas
* PyTorch / TensorFlow (depending on implementation)
* NLP utilities (e.g., tokenizers)

> ⚠️ Exact library versions depend on your environment and model implementation.

---

## 🚀 How to Use

1. Open and run `DataProcessing_Paraphrase.ipynb` to generate cleaned/paraphrased data
2. Verify the output dataset format
3. Open `TextToSQL_enc_dec.ipynb`
4. Train the encoder–decoder model using the processed data
5. Test the model with custom natural language queries

---

## 📌 Notes

* Ensure file paths between notebooks are consistent
* Training may require a CPU/GPU depending on dataset size
* This project is modular: preprocessing and modeling are intentionally separated

---
## 👩‍💻👨‍💻 Authors

| Name        | Student ID |
|-------------|------------|
| Tigist Wondimneh| GSR/5506/17   |
|  Nahom Senay   |GSR/4848/17|
| Michael Shimeles | GSR/6484/17   |


---

## 📄 License

This project is intended for academic and research purposes. Add a license file if public distribution is planned.
