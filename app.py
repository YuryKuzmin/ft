import streamlit as st
import pandas as pd
import json
import io
import base64

st.set_page_config(page_title="OpenAI Fine-Tuning Data Converter", page_icon="📊", layout="wide")

st.title("OpenAI Fine-Tuning Data Converter")
st.markdown("""
Convert your CSV or Excel data into the proper JSONL format for OpenAI fine-tuning.
* **Supervised Fine-Tuning**: Converts to standard fine-tuning format
* **DPO Fine-Tuning**: Converts to preference optimization format
""")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=['csv', 'xlsx'])

if uploaded_file:
    # Read the file
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    # Display preview of the data
    st.subheader("Preview of uploaded data")
    st.dataframe(df.head())
    
    # Fine-tuning type selector
    ft_type = st.radio(
        "Select the fine-tuning format you need:",
        ("Supervised Fine-Tuning", "DPO (Direct Preference Optimization)")
    )
    
    if ft_type == "Supervised Fine-Tuning":
        # Column mapping for supervised fine-tuning
        st.subheader("Map your columns")
        prompt_col = st.selectbox("Select the column containing prompts/instructions:", df.columns)
        completion_col = st.selectbox("Select the column containing completions/responses:", df.columns)
        
        # Optional system message
        system_message = st.text_area(
            "System message (optional):", 
            "Translate the following into German.", 
            help="This message sets the behavior of the assistant"
        )
        
        if st.button("Generate JSONL for Supervised Fine-Tuning"):
            # Create the JSONL for standard fine-tuning
            jsonl_output = io.StringIO()
            for index, row in df.iterrows():
                json_obj = {
                    "messages": [
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": str(row[prompt_col])},
                        {"role": "assistant", "content": str(row[completion_col])}
                    ]
                }
                # Use ensure_ascii=False to keep Cyrillic and other non-ASCII characters readable
                jsonl_output.write(json.dumps(json_obj, ensure_ascii=False) + '\n')
            
            # Create download button for the JSONL file
            st.download_button(
                label="Download JSONL File",
                data=jsonl_output.getvalue(),
                file_name="supervised_training_data.jsonl",
                mime="application/jsonl"
            )
            
            # Show sample of the output
            st.subheader("Sample of JSONL output")
            output_sample = jsonl_output.getvalue().split('\n')
            # Only show non-empty lines
            output_sample = [line for line in output_sample if line.strip()]
            st.code('\n'.join(output_sample[:3]))
            
    else:  # DPO Fine-Tuning
        # Column mapping for DPO
        st.subheader("Map your columns")
        prompt_col = st.selectbox("Select the column containing prompts:", df.columns)
        preferred_col = st.selectbox("Select the column containing preferred completions:", df.columns)
        rejected_col = st.selectbox("Select the column containing rejected completions:", df.columns)
        
        if st.button("Generate JSONL for DPO Fine-Tuning"):
            # Create the JSONL for DPO
            jsonl_output = io.StringIO()
            for index, row in df.iterrows():
                # Create the JSON object in the format required for DPO
                json_obj = {
                    "input": {
                        "messages": [
                            {"role": "user", "content": str(row[prompt_col])}
                        ],
                        "tools": [],
                        "parallel_tool_calls": True
                    },
                    "preferred_output": [
                        {"role": "assistant", "content": str(row[preferred_col])}
                    ],
                    "non_preferred_output": [
                        {"role": "assistant", "content": str(row[rejected_col])}
                    ]
                }
                # Use ensure_ascii=False to keep Cyrillic and other non-ASCII characters readable
                jsonl_output.write(json.dumps(json_obj, ensure_ascii=False) + '\n')
            
            # Create download button for the JSONL file
            st.download_button(
                label="Download JSONL File",
                data=jsonl_output.getvalue(),
                file_name="dpo_training_data.jsonl",
                mime="application/jsonl"
            )
            
            # Show sample of the output
            st.subheader("Sample of JSONL output")
            output_sample = jsonl_output.getvalue().split('\n')
            # Only show non-empty lines
            output_sample = [line for line in output_sample if line.strip()]
            st.code('\n'.join(output_sample[:3]))

# Documentation section
st.markdown("""
---
## How to use this converter

1. **Upload your data file** (CSV or Excel)
2. **Select the fine-tuning format** you need
3. **Map your columns** to the appropriate fields
4. **Generate the JSONL file** and download it
5. **Upload the JSONL** to OpenAI for fine-tuning

### Format Requirements

#### Supervised Fine-Tuning
- You need columns for prompts and completions
- Format will include system, user, and assistant messages

#### DPO Fine-Tuning
- You need columns for prompts, preferred completions, and rejected completions
- Format follows OpenAI's required schema with:
  - `input.messages` containing the user message
  - `preferred_output` containing the preferred assistant response
  - `non_preferred_output` containing the rejected assistant response
""")
