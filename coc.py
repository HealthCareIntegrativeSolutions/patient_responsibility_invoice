# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.platypus.flowables import Image
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_JUSTIFY, TA_LEFT
import dataformatter

import PIL
import pandas as pd
import time


from functools import partial

styles = getSampleStyleSheet()
styleN = styles['Normal']
styleH = styles['Heading1']

styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
styles.add(ParagraphStyle(name='RIGHT', alignment=TA_RIGHT))
styles.add(ParagraphStyle(name='LEFT', alignment=TA_LEFT))

def footer(canvas, doc):
    canvas.saveState()
    P = Paragraph("This is a multi-line footer.  It goes on every page.  " * 5,
                  styleN)
    w, h = P.wrap(doc.width, doc.bottomMargin)
    P.drawOn(canvas, doc.leftMargin, h)
    canvas.restoreState()

def header(canvas, doc, content):
    canvas.saveState()
    w, h = content.wrap(doc.width, doc.topMargin)
    content.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)
    canvas.restoreState()

def header_footer(canvas, doc, header, footer):
    canvas.saveState()
    w, h = header.wrap(doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)

    w, h = footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, h)
    canvas.restoreState()
def createdoc():

    doc = BaseDocTemplate('test.pdf', pagesize=letter)
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,id='normal')
    template = PageTemplate(id='test', frames=frame, onPage=footer)
    doc.addPageTemplates([template])

    text = []
    for i in range(111):
        text.append(Paragraph("This is line %d." % i,
                              styleN))
    doc.build(text)

def create_header(invoice_number,styles):
    logo = "C:/Users/nagas/OneDrive/Documents/Sankrithi Consulting/HNT_HIS/Projects/Vivify Implementation/Brochure/Modified_Logos/Logos/hnts-logo/PNG/hnts-logo.png"
    im = Image(logo, 2 * inch, 0.75 * inch)
    im.hAlign = 'RIGHT'

    from_address_parts = ["Home Nursing & Therapy Services", "2018 Avenue B, Suite 200","San Antonio, TX 78215", "Ph: (210)-822-8807 Ext. 1009",
                          "Fax: (210)-822-8863", "email: accounting@hnts.org", "Attn: Pernetter Christian"]
    full_address = []
    for part in from_address_parts:
        ptext = '<font size=10>%s</font>' % part.strip()
        full_address.append(Paragraph(ptext, styles["LEFT"]))

    headerdata = [[' ', full_address, invoice_number, [im], '']]
    h = Table(headerdata, [0.4 * inch, 2.5 * inch, 3 * inch, 2 * inch, 0.2 * inch])
    return h


def createdoc2():
    doc = BaseDocTemplate('test2.pdf', pagesize=letter)
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height-2*cm, id='normal')
    header_content = Paragraph("This is a multi-line header.  It goes on every page.  " * 8, styleN)
    footer_content = Paragraph("This is a multi-line footer.  It goes on every page.  " * 5, styleN)
    template = PageTemplate(id='test', frames=frame, onPage=partial(header_footer, header=header_content, footer=footer_content))
    doc.addPageTemplates([template])

    text = []
    for i in range(111):
        text.append(Paragraph("This is line %d." % i, styleN))
    doc.build(text)

def createcoc(fname):
    # #doc = SimpleDocTemplate(fname, pagesize=letter,
    #                         rightMargin=50, leftMargin=20,
    #                         topMargin=20, bottomMargin=10)

    doc = BaseDocTemplate(fname, pagesize=letter,rightMargin=50, leftMargin=20,topMargin=40, bottomMargin=10)
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height -2.5 *cm, id='normal')
    invoicenum = "TEST-01"
    header_content = create_header(invoicenum, styles)
    footer_content = Paragraph("THANK YOU FOR YOUR BUSINESS!", styles['Justify'])
    #footer_content.append(Paragraph("For payment arrangements Contact Pernetter Christian at 210-822-8807 # 1009", styles['Justify']))
    template = PageTemplate(id='test', frames=frame,
                            onPage=partial(header_footer, header=header_content, footer=footer_content))
    doc.addPageTemplates([template])
    Story = []
    Story.append(Spacer(1, 12))
    # Recipient's address
    ptext = '<font size=12>To</font>'
    to_P = Paragraph(ptext, styles["RIGHT"])
    to_address_parts = ["GALLEGOS, RAY", "1711 SILVER MOUNTAIN DR", "SAN ANTONIO, TX 78264", "(210)-262-6209"]
    # Create
    to_address = []
    for part in to_address_parts:
        ptext = '<font size=10>%s</font>' % part
        to_address.append(Paragraph(ptext, styles["LEFT"]))
    insurance_info = ['SAIKIRAN', 'KADIYALA']
    insurance_text = []
    for part in insurance_info:
        ptext = '<font size=10>%s</font>' % part
        insurance_text.append(Paragraph(ptext, styles["RIGHT"]))

    to_data = [[to_P, '', ''],
               ['', to_address, insurance_text ],
               ]
    to_T = Table(to_data, [1.0 * inch, 3 * inch, 4.5*inch])
    Story.append(to_T)

    name_parts= to_address_parts[0].split(',')
    full_name = name_parts[1].strip() + ' ' + name_parts[0].strip()
    Story.append(Spacer(1, 20))
    ptext = '<font size=12>Dear %s:</font>' % full_name.title()
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 20))

    ptext = '<font size=12>Thank you for trusting HNTS to provide you with home healthcare services.  You should have received an "Explanation of Benefits" from your insurance carrier regarding your claims.' \
            ' This invoice is for the patient\'s responsibility for the services rendered by HNTS.</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))

    Story.append(Spacer(1, 20))
    ptext = '<font size=12>Check or Money order payable to:</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))
    ptext = '<font size=12>Home Nursing & Therapy Services</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))
    ptext = '<font size=12>Attn: Accounts Payable</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))
    ptext = '<font size=12>2018 Avenue B, Ste. 200</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))
    ptext = '<font size=12>San Antonio, TX 78215</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 20))
    ptext = '<font size=12>Credit Card payment:</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))
    ptext = '<font size=12>Email accounting@hnts.org for an invoice to be emailed directly to you for secure online payment.</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 20))
    ptext = '<font size=12>Questions/ Payment arrangements :</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))
    ptext = '<font size=12>Contact Pernetter Christian at accounting@hnts.org or 210-822-8807 #1009</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))


    Story.append(Spacer(1, 20))

    header_row = [[' Claim\nItem #', 'Description of Service', 'Amt \n Billed to \n Insurance', 'Insurance\nAdjustment','Insurance\nPayment to\n Agency','Patient\'s\nResponsible\nAmount'],
            ]

    #
    # lista = header_row + claims_df.values.tolist()
    #
    # t_style = TableStyle([('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
    #                       ('TEXTCOLOR', (1, 1), (-2, -1), colors.black),
    #                       ('VALIGN', (0, 0), (0, -1), 'BOTTOM'),
    #                       ('ALIGN', (0, 0), (0, -1), 'CENTER'),
    #                       ('ALIGN', (0, 0), (-1, 0), 'RIGHT'),
    #                       ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
    #                       ('ALIGN', (1, -1), (-1, -1), 'RIGHT'),
    #                       ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
    #                       ('TEXTCOLOR', (0, -1), (-1, -1), colors.black),
    #                       ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    #                       ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.85, 0.86, 0.8)),
    #
    #                       ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.lightgrey),
    #                       ('BOX', (0, 0), (-1, -1), 0.25, colors.lightgrey),
    #                       ])
    # s = getSampleStyleSheet()
    #s = s["BodyText"]
    #s.wordWrap = 'CJK'
    #t = Table(lista, colWidths=[0.6 * inch, 2.7 * inch, 1 * inch, 1 * inch,1* inch,1.3* inch,], repeatRows=1)
    #t.setStyle(t_style)

   # Story.append(t)
    doc.build(Story)


if __name__ == '__main__':
    from time import gmtime, strftime

    # using simple format of showing time
    s = strftime("%a, %d %b %Y", gmtime())

    createcoc('Saikiran_test'+str(s)+'.pdf')