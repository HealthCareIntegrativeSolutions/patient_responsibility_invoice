from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import BaseDocTemplate, Frame, NextPageTemplate, PageBreak, PageTemplate, Paragraph, Table, TableStyle


class ShippingListReport(BaseDocTemplate):
    def __init__(self, filename, their_adress, objects, **kwargs):
        super().__init__(filename, page_size=A4, _pageBreakQuick=0, **kwargs)
        self.their_adress = their_adress
        self.objects = objects

        self.page_width = self.width + self.leftMargin * 2
        self.page_height = self.height + self.bottomMargin * 2

        styles = getSampleStyleSheet()

        # Setting up the frames, frames are use for dynamic content not fixed page elements
        first_page_table_frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height - 6 * cm, id="small_table")
        later_pages_table_frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="large_table")

        # Creating the page templates
        first_page = PageTemplate(id="FirstPage", frames=[first_page_table_frame], onPage=self.on_first_page)
        later_pages = PageTemplate(id="LaterPages", frames=[later_pages_table_frame], onPage=self.add_default_info)
        self.addPageTemplates([first_page, later_pages])

        # Tell Reportlab to use the other template on the later pages,
        # by the default the first template that was added is used for the first page.
        story = [NextPageTemplate(["*", "LaterPages"])]

        table_grid = [["Product", "Quantity"]]
        # Add the objects
        for shipped_object in self.objects:
            table_grid.append([shipped_object, "42"])

        story.append(
            Table(
                table_grid,
                repeatRows=1,
                colWidths=[0.5 * self.width, 0.5 * self.width],
                style=TableStyle(
                    [
                        ("GRID", (0, 1), (-1, -1), 0.25, colors.gray),
                        ("BOX", (0, 0), (-1, -1), 1.0, colors.black),
                        ("BOX", (0, 0), (1, 0), 1.0, colors.black),
                    ]
                ),
            )
        )

        self.build(story)

    def on_first_page(self, canvas, doc):
        canvas.saveState()
        # Add the logo and other default stuff
        self.add_default_info(canvas, doc)

        canvas.drawString(doc.leftMargin, doc.height, "My address")
        canvas.drawString(0.5 * doc.page_width, doc.height, self.their_adress)

        canvas.restoreState()

    def add_default_info(self, canvas, doc):
        canvas.saveState()
        canvas.drawCentredString(0.5 * (doc.page_width), doc.page_height - 2.5 * cm, "Company Name")

        canvas.restoreState()


if __name__ == "__main__":
    ShippingListReport("example.pdf", "Their address", ["Product", "Product"] * 50)
