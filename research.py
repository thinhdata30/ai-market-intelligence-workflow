"""Document ingestion, basic retrieval, optional web search, and cited output."""
import re
from datetime import datetime, timezone
from pathlib import Path
import requests
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_documents(folder):
    records = []
    for path in sorted(Path(folder).rglob('*')):
        if not path.is_file() or path.suffix.lower() not in {'.txt', '.pdf'}:
            continue
        try:
            if path.suffix.lower() == '.pdf':
                for i, page in enumerate(PdfReader(str(path)).pages, start=1):
                    text = page.extract_text() or ''
                    if text.strip():
                        records.extend(chunk_text(text, f'{path.name}, p. {i}'))
            else:
                records.extend(chunk_text(path.read_text(encoding='utf-8'), path.name))
        except Exception as ex:
            print(f'Warning: could not parse {path.name}: {ex}')
    return records


def chunk_text(text, source, words_per_chunk=130, overlap=25):
    words = text.split()
    if not words:
        return []
    step = max(1, words_per_chunk - overlap)
    return [{'source': source, 'text': ' '.join(words[i:i + words_per_chunk])}
            for i in range(0, len(words), step)]


def retrieve(records, question, top_k=5):
    if not records:
        return []
    corpus = [r['text'] for r in records]
    matrix = TfidfVectorizer(stop_words='english').fit_transform(corpus + [question])
    similarities = cosine_similarity(matrix[-1], matrix[:-1]).ravel()
    indices = similarities.argsort()[::-1][:top_k]
    return [{**records[int(i)], 'similarity': round(float(similarities[i]), 3)} for i in indices]


def search_web(query):
    """Only calls SerpAPI if SERPAPI_API_KEY is configured. No hardcoded secrets."""
    import os
    key = os.getenv('SERPAPI_API_KEY')
    if not key:
        return []
    response = requests.get('https://serpapi.com/search.json', params={
        'engine': 'google', 'q': query, 'api_key': key, 'num': 5
    }, timeout=20)
    response.raise_for_status()
    data = response.json()
    return [{'title': x.get('title', ''), 'url': x.get('link', ''),
             'snippet': x.get('snippet', '')} for x in data.get('organic_results', [])[:5]]


def create_offline_report(company, question, evidence, web_results):
    """Extractive evidence review, NOT AI-authored strategic conclusions."""
    lines = [f'# Market Intelligence Evidence Review: {company}', '',
             f'**Question:** {question}',
             f'**Created (UTC):** {datetime.now(timezone.utc).strftime("%Y-%m-%d")}', '',
             '## Evidence from supplied documents',
             '_The following are retrieved excerpts, not verified strategic conclusions._', '']
    for idx, item in enumerate(evidence, 1):
        lines.append(f'{idx}. **Source:** `{item["source"]}` (retrieval score {item["similarity"]:.3f})')
        lines.append(f'   > {item["text"][:650]}')
        lines.append('')
    lines.append('## Optional web search results (verify independently)')
    if web_results:
        for x in web_results:
            lines.append(f'- [{x["title"]}]({x["url"]}): {x["snippet"]}')
    else:
        lines.append('_Not included. Set `SERPAPI_API_KEY` for an optional SerpAPI search._')
    lines += ['', '## Analyst checklist', '- Verify excerpts against original documents.',
              '- Distinguish facts from possible risks and opportunities.',
              '- Check publication dates and any conflicting sources.',
              '- Do not represent an AI agent conclusion unless CrewAI mode was run.', '']
    return '\n'.join(lines)


def save_report(text, folder, company):
    dest = Path(folder)
    dest.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r'[^a-z0-9]+', '-', company.lower()).strip('-') or 'company'
    path = dest / f'{slug}-report.md'
    path.write_text(text, encoding='utf-8')
    return path
