# ft
Convert CSV datasets into JSONL for GPT fine-tuning

# OpenAI Fine-Tuning Data Converter

A simple web app that converts CSV/Excel data into the proper JSONL format for OpenAI fine-tuning.

## Features

- **Support for multiple fine-tuning formats**:
  - Supervised Fine-Tuning (standard format)
  - DPO (Direct Preference Optimization)
- **Easy-to-use interface** for mapping your data columns
- **Preview** your data and output format
- **Download** ready-to-use JSONL files

## How it works

1. Upload your CSV or Excel file containing training data
2. Select the fine-tuning format you need
3. Map your columns to the appropriate fields
4. Generate and download the JSONL file
5. Use the JSONL file with OpenAI's fine-tuning API

## Local Development

### Prerequisites

- Python 3.8+
- pip

### Setup

1. Clone this repository
   ```
   git clone https://github.com/yourusername/openai-finetuning-converter.git
   cd openai-finetuning-converter
   ```

2. Install dependencies
   ```
   pip install -r requirements.txt
   ```

3. Run the app
   ```
   streamlit run app.py
   ```

## Data Format Requirements

### For Supervised Fine-Tuning

Your CSV/Excel file should contain at least:
- A column for prompts/instructions
- A column for completions/responses

### For DPO Fine-Tuning

Your CSV/Excel file should contain:
- A column for prompts
- A column for preferred completions
- A column for rejected completions

## Deployment

This app is ready to deploy on Streamlit Cloud. See the deployment instructions in the repository.

## License

MIT License
