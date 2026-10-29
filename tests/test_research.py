from research import chunk_text, retrieve, load_documents, create_offline_report

def test_retrieval():
    docs = chunk_text('Shipping delays increased. Supplier costs rose.', 'sample.txt')
    chosen = retrieve(docs, 'supplier shipping risks')
    assert chosen and 'sample.txt' in chosen[0]['source']

def test_report():
    report = create_offline_report('Example', 'risks?', [{'source':'x.txt','text':'Shipping delays','similarity':0.25}], [])
    assert 'x.txt' in report and 'not verified' in report
