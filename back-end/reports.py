from fpdf import FPDF

def pdf_generate(values):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', size=16)
    pdf.cell(0, 3, txt='Relatório Nativas Grill Estoque Carnes', ln=1, align='C')
    pdf.ln(10)
    pdf.set_font('Arial', '', 10)  
    for meat, usage, rest in values:
        if usage != 0.0 or rest != 0.0:
            pdf.cell(0, 7, txt=f"{meat}: USADO: {usage:.3f} | SOBRA: {rest:.3f}", ln=1, align='L')
    file = 'backup.pdf'
    pdf.output(file)
    return file