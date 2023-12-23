import spacy
import docx

def should_anonymize(token):
    # Дополнительные проверки, чтобы решить, нужно ли анонимизировать данный токен
    return token.ent_type_ and token.ent_type_ not in ["DATE", "PERSON", "LAW"] and not token.text.isdigit()

def anonymize_text(text):
    doc = nlp(text)
    return ''.join([' XXX ' if should_anonymize(token) else token.text + token.whitespace_ for token in doc])

def process_paragraph(paragraph):
    paragraph.text = anonymize_text(paragraph.text)
    for run in paragraph.runs:
        run.text = anonymize_text(run.text)

def process_cell(cell):
    cell.text = anonymize_text(cell.text)
    for paragraph in cell.paragraphs:
        process_paragraph(paragraph)

nlp = spacy.load("ru_core_news_sm")
docx_file = r"anon\examples\dist_obrabotka_full.docx"
document = docx.Document(docx_file)

for paragraph in document.paragraphs:
    process_paragraph(paragraph)

for table in document.tables:
    for row in table.rows:
        for cell in row.cells:
            process_cell(cell)

document.save(docx_file)
