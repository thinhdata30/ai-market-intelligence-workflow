"""Evidence-first company research demo. Offline baseline requires no API key.

Usage:
  python main.py --company 'Example Retail' --question 'What risks does it face?'
  python main.py --company 'Example Retail' --mode crewai
"""
import argparse
import os
from pathlib import Path

from research import load_documents, retrieve, search_web, create_offline_report, save_report


def main():
    parser = argparse.ArgumentParser(description='Market intelligence research workflow')
    parser.add_argument('--company', default='Example Retail')
    parser.add_argument('--question', default='What are the main risks and opportunities?')
    parser.add_argument('--data-dir', default='data')
    parser.add_argument('--mode', choices=['offline', 'crewai'], default='offline')
    args = parser.parse_args()

    docs = load_documents(args.data_dir)
    if not docs:
        raise SystemExit(f'No readable .txt or .pdf files found in {args.data_dir}/')
    evidence = retrieve(docs, args.question, top_k=5)
    if args.mode == 'crewai':
        from agents_workflow import run_crew
        report = run_crew(args.company, args.question, evidence)
    else:
        # Offline mode deliberately does NOT generate unsupported AI conclusions.
        results = search_web(args.company + ' ' + args.question) if os.getenv('SERPAPI_API_KEY') else []
        report = create_offline_report(args.company, args.question, evidence, results)
    path = save_report(report, 'outputs', args.company)
    print(f'Report written to {path}')
    print('Mode:', args.mode)


if __name__ == '__main__':
    main()
