# -*- coding: utf-8 -*-
# # Copyright (c) 2016-2020 educorvi GmbH & Co. KG
# # lars.walther@educorvi.de

import os.path
import tempfile
from datetime import date
from time import gmtime, localtime, strftime

from apply import apply
from reportlab.lib.colors import grey, white
from reportlab.lib.enums import TA_CENTER as _c
from reportlab.lib.enums import TA_RIGHT as _r
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Table
from reportlab.platypus.doctemplate import BaseDocTemplate, PageTemplate
from reportlab.platypus.flowables import BalancedColumns, Flowable, Image, PageBreak, Spacer
from reportlab.platypus.frames import Frame
from reportlab.platypus.paragraph import Paragraph

# pdfmetrics.registerFont(TTFont("Helvetica", "DGUVMeta-Normal.ttf"))
# pdfmetrics.registerFont(TTFont("Helvetica", "DGUVMeta-Bold.ttf"))

absatz1 = "absatz1"
absatz2 = "absatz2"
absatz3 = "absatz3"
absatz4 = "absatz4"
absatz5 = "absatz5"
zelle1 = "zelle1"
zelle2 = "zelle2"
bulletlist = ["bulletlist1", "bulletlist2"]


class PdfBaseTemplate(BaseDocTemplate):
    """Basistemplate for PDF-Prints"""

    def __init__(self, filename, **kw):
        frame1 = Frame(1 * cm, 1 * cm, 18.5 * cm, 27 * cm, id="F1", showBoundary=False)
        self.allowSplitting = 0
        apply(BaseDocTemplate.__init__, (self, filename), kw)
        self.addPageTemplates(PageTemplate("normal", [frame1]))

    # def handle_pageBegin(self):
    #    import pdb;pdb.set_trace()


class NumberedCanvas(canvas.Canvas):
    """Add Page number to generated PDF"""

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 7.5)
        if self._pageNumber < page_count:
            self.drawRightString(19.3 * cm, 1 * cm, "Seite %d von %d" % (self._pageNumber, page_count))
        if self._pageNumber == page_count:
            self.drawRightString(19.3 * cm, 2 * cm, "Seite %d von %d" % (self._pageNumber, page_count))
            self.drawString(9.25 * cm, 2 * cm, "www.bgetem.de")
            self.drawString(1.2 * cm, 2 * cm, "Berufsgenossenschaft")
            self.drawString(1.2 * cm, 1.6 * cm, "Energie Textil Elektro")
            self.drawString(1.2 * cm, 1.2 * cm, "Medienerzeugnisse")


class InteractiveCheckBox(Flowable):
    def __init__(self, text="A Box"):
        Flowable.__init__(self)
        self.text = text
        self.boxsize = 16

    def draw(self):
        self.canv.saveState()
        form = self.canv.acroForm
        form.checkbox(checked=False, buttonStyle="cross", name=self.text, tooltip=self.text, relative=True, borderStyle="solid", borderWidth=0.5, borderColor=grey, size=self.boxsize)
        self.canv.restoreState()
        return


class InteractiveTextField(Flowable):
    def __init__(self, text="A Text", width=210):
        Flowable.__init__(self)
        self.text = text
        self.width = width
        self.height = 20

    def draw(self):
        self.canv.saveState()
        form = self.canv.acroForm
        form.textfield(
            borderStyle="underlined", name=self.text, width=self.width, fillColor=white, borderWidth=0.5, height=self.height, fieldFlags="richText", fontSize=8, tooltip=self.text, relative=True
        )
        self.canv.restoreState()
        return


def createpdf(filehandle, content):
    """Funktion zum Schreiben der PDF-Datei"""

    story = []  # Alle Elemente des PDFs werden der Story hinzugefuegt

    # Styles fuer normale Paragraphen, gelesen aus dem SampleStyleSheet
    stylesheet = getSampleStyleSheet()
    h1 = stylesheet["Heading1"]
    h1.fontname = "Helvetica"
    h2 = stylesheet["Heading2"]
    h2.fontName = "Helvetica"
    h3 = stylesheet["Heading3"]
    h3.fontname = "Helvetica"
    code = stylesheet["Code"]
    bodytext = stylesheet["BodyText"]
    bodytext.fontName = "Helvetica"
    bodybold = stylesheet["BodyText"]
    bodybold.fontName = "Helvetica"

    # Weitere Styles fuer Paragraphen
    stylesheet.add(ParagraphStyle(name="smallbody", fontName="Helvetica", fontSize=9, spaceAfter=5))
    stylesheet.add(ParagraphStyle(name="normal", fontName="Helvetica", fontSize=7.5, borderPadding=(5, 3, 3, 5)))
    stylesheet.add(ParagraphStyle(name="free", fontName="Helvetica", fontSize=7.5, borderPadding=0))
    stylesheet.add(ParagraphStyle(name="right", fontName="Helvetica", fontSize=7.5, borderPadding=(5, 3, 3, 5), alignment=_r))
    stylesheet.add(ParagraphStyle(name="center", fontName="Helvetica", fontSize=7.5, borderPadding=(5, 3, 3, 5), alignment=_c))
    stylesheet.add(ParagraphStyle(name="bold", fontName="Helvetica", fontSize=7.5, borderPadding=(5, 3, 3, 5)))
    stylesheet.add(ParagraphStyle(name="boldnew", fontName="Helvetica", fontSize=9, borderPadding=(5, 3, 3, 5)))
    stylesheet.add(ParagraphStyle(name="boldright", fontName="Helvetica", fontSize=7.5, borderPadding=(5, 3, 3, 5), alignment=_r))
    stylesheet.add(ParagraphStyle(name="boldcenter", fontName="Helvetica", fontSize=7.5, borderPadding=(5, 3, 3, 5), alignment=_c))

    smallbody = stylesheet["smallbody"]
    bullet = stylesheet["Bullet"]
    bullet.fontSize = 9
    bullet.fontName = "Helvetica"
    entry_normal = stylesheet["normal"]
    entry_free = stylesheet["free"]
    entry_right = stylesheet["right"]
    entry_center = stylesheet["center"]
    entry_bold = stylesheet["bold"]
    entry_boldnew = stylesheet["boldnew"]
    entry_boldright = stylesheet["boldright"]
    entry_boldcenter = stylesheet["boldcenter"]

    # Add your logo to the page head.
    # im = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images/bghw.jpg')
    # logo = Image(im, 6.22 * cm, 2 * cm)
    # logo.hAlign = 'RIGHT'
    # story.append(logo)
    # story.append(Spacer(0 * cm, 1.5 * cm))

    im = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Logos/AXXESS.png")
    logo = Image(im)
    logo.drawHeight = 6 * cm * logo.drawHeight / logo.drawWidth
    logo.drawWidth = 6 * cm
    logo.hAlign = "RIGHT"

    # Datum
    datum = "Datum: %s" % (strftime("%d.%m.%Y"))
    zeit = "Zeit: %s" % (strftime("%H:%M:%S", localtime()))

    colWidths = [9.5 * cm, 2.75 * cm, 6.25 * cm]
    testcontent = "Ergänzung der Gefährdungsbeurteilung für Bau- und Montagestellen zum Schutz vor Infektion mit dem Coronavirus"
    testheadline = '<font color="#008c8e"><b>%s</b></font>' % testcontent
    toptable = [[Paragraph(testheadline, h2), Paragraph(" ", bodytext), logo]]
    table = Table(toptable, colWidths=colWidths)
    table.hAlign = "CENTER"
    story.append(table)

    story.append(Spacer(0 * cm, 0.5 * cm))

    textbox_name = InteractiveTextField("Name", 250)
    textbox_datum = InteractiveTextField("Datum", 250)
    textbox_unternehmer = InteractiveTextField("Unternehmer/Unternehmerin", 250)

    story.append(Paragraph("Firma", entry_free))
    story.append(textbox_name)
    story.append(Spacer(0 * cm, 0.1 * cm))
    story.append(Paragraph("Datum", entry_free))
    story.append(textbox_datum)
    story.append(Spacer(0 * cm, 0.1 * cm))
    story.append(Paragraph("Unternehmer/Unternehmerin", entry_free))
    story.append(textbox_unternehmer)

    story.append(Spacer(0 * cm, 0.5 * cm))

    # story.append(Paragraph(absatz1, smallbody))
    # story.append(Spacer(0 * cm, 0.25* cm))
    # story.append(Paragraph(absatz2, smallbody))
    # story.append(Spacer(0 * cm, 0.25* cm))
    # story.append(Paragraph(absatz3, smallbody))
    # story.append(Spacer(0 * cm, 0.25* cm))
    # story.append(Paragraph(absatz4, smallbody))
    # story.append(Spacer(0 * cm, 0.25* cm))
    # for i in bulletlist:
    #    listentry = "<bullet>&bull;</bullet>%s" %i
    #    story.append(Paragraph(listentry, bullet))
    # story.append(Spacer(0 * cm, 0.25* cm))
    # story.append(Paragraph(absatz5, smallbody))

    ctt = []
    ctt.append(Paragraph(absatz1, smallbody))
    ctt.append(Paragraph(absatz2, smallbody))
    ctt.append(Paragraph(absatz3, smallbody))
    ctt.append(Paragraph(absatz4, smallbody))
    for i in bulletlist:
        listentry = "<bullet>&bull;</bullet>%s" % i
        ctt.append(Paragraph(listentry, bullet))
    ctt.append(Paragraph(absatz5, smallbody))

    story.append(BalancedColumns(ctt, nCols=2, needed=72, spaceBefore=0, spaceAfter=0))

    story.append(Spacer(0 * cm, 1 * cm))

    # optional: Festlegung fester Tabellenbreiten
    colWidths = [8 * cm, 1.25 * cm, 1.25 * cm, 8 * cm]

    checkbox_1 = InteractiveCheckBox("cb1")
    checkbox_2 = InteractiveCheckBox("cb2")
    textbox_1 = InteractiveTextField("zeile1")
    textbox_2 = InteractiveTextField("zeile2")

    checkbox_3 = InteractiveCheckBox("cb3")
    checkbox_4 = InteractiveCheckBox("cb4")
    textbox_3 = InteractiveTextField("zeile4")
    textbox_4 = InteractiveTextField("zeile5")

    mytable = []
    tableheader = [Paragraph("Organisation", entry_bold), Paragraph("ja", entry_boldcenter), Paragraph("nein", entry_boldcenter), Paragraph("Bemerkung/Maßnahme", entry_bold)]
    mytable.append(tableheader)

    tablebody = [
        Paragraph(zelle1, entry_normal),
        checkbox_1,
        checkbox_2,
        [textbox_1, textbox_2],
    ]
    mytable.append(tablebody)
    tablebody = [
        Paragraph(zelle2, entry_normal),
        checkbox_3,
        checkbox_4,
        [textbox_3, textbox_4],
    ]
    mytable.append(tablebody)

    table = Table(mytable, repeatRows=1, colWidths=colWidths, style=[("GRID", (0, 0), (-1, -1), 1, grey), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")])
    table.hAlign = "LEFT"
    story.append(table)

    story.append(PageBreak())
    story.append(Spacer(0 * cm, 1 * cm))
    story.append(Paragraph("Weitere Maßnahmen (z. B. Notfall- oder Pandemieplan):", smallbody))
    story.append(Spacer(0 * cm, 0.5 * cm))
    story.append(InteractiveTextField("massnahme1", 500))
    story.append(InteractiveTextField("massnahme2", 500))
    story.append(InteractiveTextField("massnahme3", 500))
    story.append(InteractiveTextField("massnahme4", 500))
    story.append(InteractiveTextField("massnahme5", 500))
    story.append(InteractiveTextField("massnahme6", 500))
    story.append(InteractiveTextField("massnahme7", 500))
    story.append(InteractiveTextField("massnahme8", 500))

    story.append(Spacer(0 * cm, 14 * cm))
    schlusstext = """Diese Gefährdungsbeurteilung ergänzt die betriebliche Gefährdungsbeurteilung. Sie wurde
                      vor Beginn der Arbeiten erstellt, die Maßnahmen wurden umgesetzt und auf Wirksamkeit überprüft.
                      Die Mitarbeiter sind unterwiesen."""
    schlussline = '<font color="#008c8e"><b>%s</b></font>' % schlusstext
    story.append(Paragraph(schlussline, bodybold))

    story.append(Spacer(0 * cm, 0.5 * cm))

    textbox_name = InteractiveTextField("name_verantwortlich", 250)
    textbox_unterschrift = InteractiveTextField("datum_unterschrift", 250)
    colWidths = [9.25 * cm, 9.25 * cm]
    signtable = [[textbox_name, textbox_unterschrift], [Paragraph("Name des Arbeitsverantwortlichen", entry_free), Paragraph("Datum, Unterschrift", entry_free)]]
    table = Table(signtable, colWidths=colWidths)
    table.hAlign = "CENTER"
    story.append(table)

    story.append(Spacer(0 * cm, 1 * cm))

    colWidths = [8 * cm, 4.5 * cm, 6 * cm]
    datatable = [[Paragraph(" "), Paragraph("25.05.2020, Version 3", entry_free), Paragraph("Bestell-Nr. GB-C01", entry_boldright)]]
    table = Table(datatable, colWidths=colWidths)
    story.append(table)

    doc = PdfBaseTemplate(filehandle, pagesize=A4)
    doc.build(story, canvasmaker=NumberedCanvas)


if __name__ == "__main__":
    filehandle = "test_4.pdf"
    createpdf(filehandle, {"formtitle": "Formulartitel"})
