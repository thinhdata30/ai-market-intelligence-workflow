# AI Market Intelligence Workflow — reproducible upgrade

This package is a **starter implementation** to add to an existing GitHub portfolio project. It does NOT prove that the original project used CrewAI or SerpAPI. Only claim the features you actually run and validate.

## What is tested
- Offline research pipeline: reads `.txt` / text-based `.pdf`, retrieves relevant chunks with TF-IDF, and writes a source-labeled Markdown evidence review.
- The bundled `data/sample_company.txt` is **fictional** demonstration data.

## Optional / not verified here
- `--mode crewai`: 3-role CrewAI workflow using a configured external LLM. This requires paid or limited-quota API access and is **not tested** with a real account here.
- `SERPAPI_API_KEY`: optional live web search. Internet search calls were **not tested** here.
- Scanned PDFs need OCR; this code supports only PDF pages with extractable text.

## Setup on Windows
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py --company "Example Retail" --question "What are the shipping and supplier delays?"
```
Read the report created at `outputs/example-retail-report.md`.

## Your own reports
Put **public, legally usable** PDF or text reports inside `data/` and set `--company` and `--question`. Do not commit private documents or API keys.

## Optional CrewAI mode
```powershell
pip install -r requirements-ai.txt
# Set OPENAI_API_KEY as an environment variable in your terminal
python main.py --company "Example Retail" --mode crewai
```
CrewAI APIs can change: if the optional mode raises an import/model error, check your installed CrewAI version and LLM configuration. Do not claim it is tested unless you run it.

## GitHub upload
Upload `main.py`, `research.py`, `agents_workflow.py`, `requirements.txt`, `requirements-ai.txt`, `.gitignore`, `.env.example`, `data/sample_company.txt` and merge this documentation into the root README. Keep your existing `workflow.png`.

## Accurate portfolio language
- **Before online AI verification:** "Built a reproducible document-retrieval research prototype using Python, TF-IDF and PDF extraction, generating source-labeled market intelligence evidence reviews."
- **After verifying CrewAI online:** you can separately describe the multi-agent report generation and cite a real example output.
