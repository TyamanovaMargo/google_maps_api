# Places Analysis Project

A modular Python project for analyzing Google Places API data.

## Features

- Extract and clean places data
- Analyze reviews for keywords and sentiment
- Analyze categories and visualize statistics
- Generate summary reports
- Chatbot powered by LangChain for querying data

## Project Structure
```
places_analysis/
├── data/
├── notebooks/
│   └── exploration.ipynb
├── pipeline/
│   ├── pipeline_runner.py
│   └── save_results.py
├── reports/
├── scripts/
│   ├── extract_places.py
│   ├── analyze_reviews.py
│   ├── category_analysis.py
│   ├── visualize_data.py
│   └── llm_query_agent.py
├── requirements.txt
└── README.md
```

## Quick Start

1️⃣ Install dependencies:
```bash
pip install -r requirements.txt
```

2️⃣ Run the data pipeline:
```bash
python -m pipeline.pipeline_runner data/places_results.json
```

3️⃣ Explore data in Jupyter Notebook:
```
Open notebooks/exploration.ipynb and run the cells step by step.
```

4️⃣ Query your data with LLM agent:
```python
from scripts.llm_query_agent import create_llm_agent
agent = create_llm_agent('data/places_llm_data.jsonl')
result = agent.invoke("Show me top-rated restaurants in Shinjuku")
print(result['result'])
```

5️⃣ Save results and reports with:
```python
from pipeline.save_results import save_to_csv, save_report
save_to_csv(df, 'reports/places.csv')
save_report("Analysis Summary", 'reports/summary.txt')
```

