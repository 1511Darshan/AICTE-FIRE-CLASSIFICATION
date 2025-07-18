# AICTE Fire Classification

This repository contains a Jupyter Notebook project for fire classification, developed as part of the AICTE initiative. The project leverages machine learning techniques to identify and classify fire events from input data, aiming to support early detection and prevention efforts.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Dataset](#dataset)
- [Model](#model)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)

## Overview

The AICTE Fire Classification project focuses on using image data and machine learning models to accurately classify fire occurrences. It provides a practical demonstration of data preprocessing, model building, training, and evaluation in Jupyter Notebook format.

## Features

- End-to-end notebook for fire classification
- Data loading, preprocessing, and augmentation
- Model training and evaluation
- Visualization of results and metrics

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/1511Darshan/AICTE-FIRE-CLASSIFICATION.git
   cd AICTE-FIRE-CLASSIFICATION
   ```

2. **Install required Python packages**

   It's recommended to use a virtual environment.

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

   > If `requirements.txt` is not present, install commonly used packages for image classification:
   ```bash
   pip install numpy pandas matplotlib scikit-learn tensorflow keras
   ```

## Usage

Open the Jupyter Notebook in your browser:

```bash
jupyter notebook
```

Navigate to the main notebook file, follow the instructions, and execute cells to run the fire classification pipeline.

## Dataset

You will need a dataset of fire and non-fire images. If a sample dataset is not included, please refer to public datasets such as:

- [Kaggle Fire Dataset](https://www.kaggle.com/datasets/phylake1337/fire-dataset)
- [Other references](#)

Update the notebook paths as needed to point to your local dataset.

## Model

The notebook demonstrates building a machine learning or deep learning model (such as CNN) for fire classification. You can customize the architecture, hyperparameters, and training process as needed.

## Results

Output metrics, accuracy, and sample predictions are visualized in the notebook. Check the final cells for results and insights.

## Contributing

Pull requests and suggestions are welcome! Please open an issue for bug reports, feature requests, or questions.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for more information.
