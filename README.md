# Codexity Implementation

## Setup

### Prerequisites

- [Python 3.12](https://www.python.org/downloads/release/python-3120/)
- [CppCheck](https://cppcheck.sourceforge.io/#download)
- [LM Studio](https://lmstudio.ai/)

### Run up services

#### codegen-agent

Setup `.env` file:

```.env
OPENAI_API_KEY=<OPENAI_API_KEY>
OPENAI_MODEL=gpt-4o-mini
LOCAL_BASE_URL=http://localhost:1234/v1
LOCAL_API_KEY=lm_studio
```

Run in terminal:

```sh
cd codegen-agent
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

#### sast-agent

Run in terminal:

```sh
cd sast-agent
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

#### orchestrator

Run in terminal:

```sh
cd orchestrator
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Execute evaluations

Install dependencies:

```sh
python -m venv .venv
source .venv/bin/activate
pip install requests
```

Evaluate Iteration Repair:

```sh
source .venv/bin/activate
python executeIteration.py
```

Evaluate Preshot Repair:

```sh
source .venv/bin/activate
python executePreshot.py
```

Evaluate Hybrid Repair:

```sh
source .venv/bin/activate
python executeHybrid.py
```
