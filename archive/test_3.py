from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Flowable, Paragraph, SimpleDocTemplate

style = getSampleStyleSheet()["BodyText"]


class InteractiveCheckBox(Flowable):
    def __init__(self, name, tooltip="", checked=False, size=12, button_style="check"):
        Flowable.__init__(self)
        self.name = name
        self.tooltip = tooltip
        self.size = size
        self.checked = checked
        self.buttonStyle = button_style

    def draw(self):
        self.canv.saveState()
        form = self.canv.acroForm
        form.checkbox(checked=self.checked, buttonStyle=self.buttonStyle, name=self.name, tooltip=self.tooltip, relative=True, size=self.size)
        self.canv.restoreState()


doc = SimpleDocTemplate("test_3.pdf")
checkbox1 = InteractiveCheckBox("first_name", "First name")
Story = [Paragraph("First Name", style=style), checkbox1]
doc.build(Story)
