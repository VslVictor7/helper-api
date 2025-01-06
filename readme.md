## Pre-requisites

- Python 3.8 or higher
- Docker (optional)

## Installation

1. **Clone the repository** (if you haven’t done so already):
```bash
   git clone <https://github.com/VslVictor7/helper-api.git>

   cd helper-api
```

2. **Create a Virtual Environment** (venv):

```bash
python -m venv venv
```

3. **Activate the Virtual Environment:**:
```bash
source .venv/scripts/activate
```

4. **Upgrade pip**
```bash
python -m pip install --upgrade pip
```

5. **Install requirements.txt**
```bash
pip install -r requirements.txt
```

## Running Flask

- **Running api.py**
```bash
py api.py
```

- Or

- **Running with Docker-Compose**
```bash
docker-compose up --build
```