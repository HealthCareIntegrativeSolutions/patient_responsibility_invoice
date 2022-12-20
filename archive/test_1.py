from reportlab.lib.colors import blue, green, magenta, pink
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph

# Set up a basic template
doc = BaseDocTemplate(filename="test_form_text.pdf")

# Create a Frame for the Flowables (Paragraphs and such)
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")


def draw_static(canvas, doc):
    # Save the current settings
    canvas.saveState()

    # Draw the static stuff
    # canvas.setFont("Courier", 12, leading=None)

    canvas.acroForm.checkbox(x=doc.leftMargin, y=645, buttonStyle="check", borderColor=magenta, fillColor=pink, textColor=blue, forceBorder=True)

    # canvas.drawString(doc.leftMargin, 650, "Dog:")
    # canvas.acroForm.checkbox(name="cb1", tooltip="Field cb1", x=100 + doc.leftMargin, y=645, buttonStyle="check", borderColor=magenta, fillColor=pink, textColor=blue, forceBorder=True)

    # canvas.drawString(doc.leftMargin, 600, "Cat:")
    # canvas.acroForm.checkbox(name="cb2", tooltip="Field cb2", x=100 + doc.leftMargin, y=595, buttonStyle="cross", borderWidth=2, forceBorder=True)

    # canvas.drawString(doc.leftMargin, 550, "Pony:")
    # canvas.acroForm.checkbox(name="cb3", tooltip="Field cb3", x=100 + doc.leftMargin, y=545, buttonStyle="star", borderWidth=1, forceBorder=True)

    # canvas.drawString(doc.leftMargin, 500, "Python:")
    # canvas.acroForm.checkbox(name="cb4", tooltip="Field cb4", x=100 + doc.leftMargin, y=495, buttonStyle="circle", borderWidth=3, forceBorder=True)

    # canvas.drawString(doc.leftMargin, 450, "Hamster:")
    # canvas.acroForm.checkbox(name="cb5", tooltip="Field cb5", x=100 + doc.leftMargin, y=445, buttonStyle="diamond", borderWidth=None, checked=True, forceBorder=True)

    # Restore setting to before function call
    canvas.restoreState()


# Add the Frame to the template and tell the template to call draw_static for each page
template = PageTemplate(id="test", frames=[frame], onPage=draw_static)

# Add the template to the doc
doc.addPageTemplates([template])

# All the default stuff for generating a document
styles = getSampleStyleSheet()
story = []

P = Paragraph("This is a paragraph", styles["Normal"])

story.append(P)
doc.build(story)
