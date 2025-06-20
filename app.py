from flask import Flask, request, render_template, send_file
from src.ai_writer import spin_chapter
from src.ai_reviewer import review_chapter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
import io
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {"spun": "", "reviewed": ""}
    if request.method == 'POST':
        raw_text = request.form['chapter_text']
        spun = spin_chapter(raw_text)
        reviewed = review_chapter(spun)
        result = {"spun": spun, "reviewed": reviewed}
    return render_template('index.html', result=result)

@app.route('/download', methods=['GET', 'POST'])
def download_pdf():
    if request.method == 'POST':
        content = request.form.get('content', '')
        output_type = request.form.get('type', 'output')
    else:
        content = request.args.get('content', '')
        output_type = request.args.get('type', 'output')

    if not content.strip():
        return "⚠️ No content provided to download.", 400

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.8 * inch,
        leftMargin=0.8 * inch,
        topMargin=0.8 * inch,
        bottomMargin=0.8 * inch
    )

    styles = getSampleStyleSheet()
    wrapped_style = ParagraphStyle(
        name='Wrapped',
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        wordWrap='CJK',  # Ensures word wrapping
        alignment=0
    )

    flowables = []
    for para in content.strip().split('\n'):
        if para.strip():
            paragraph = Paragraph(para.strip().replace('\n', '<br/>'), wrapped_style)
            flowables.append(paragraph)
            flowables.append(Spacer(1, 0.2 * inch))

    doc.build(flowables)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"{output_type}_chapter.pdf",
        mimetype='application/pdf'
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(debug=False, host='0.0.0.0', port=port)
