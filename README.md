# Positioning Systems - CUEVAS & MIRBEY

## Authors
- **Kyllian Cuevas**
- **Thomas Mirbey**

## Description
This project implements several positioning algorithms based on different methods:
- **KBest Neighbors** (`kbest.py`): Uses the K-best neighbors method to estimate a position.
- **N-Lateration (3D)** (`nlateration.py`): A method based on multilateration in three dimensions for position calculation.
- **Flask Web Application** (`website.py`): A web interface to display and manage positioning system data.

## Dependency Installation
This project requires Python 3 and the following libraries:

```sh
pip install numpy matplotlib scipy flask
```

## Usage
### Run the KBest Neighbors script
```sh
python3 kbest.py
```

### Run the N-Lateration script
```sh
python3 nlateration.py
```

### Start the Flask Web Application
```sh
python3 website.py
```
The web server will run locally. Open your browser and go to `http://127.0.0.1:80/`.

## Project Structure
```
Positionning_systems_CUEVAS_MIRBEY/
├── kbest.py          # KBest Neighbors implementation
├── nlateration.py    # 3D multilateration algorithm
├── website.py        # Flask web interface
├── README.md         # Documentation
└── requirements.txt  # Project dependencies
```


