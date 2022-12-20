from datetime import datetime

import pytz
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle
from reportlab.platypus.flowables import Flowable, Image

TIMEZONE_CST = pytz.timezone("US/Central")
TIMESTAMP_FORMAT_STRING = "%Y-%m-%d %H:%M:%S"
TIMESTAMP_FORMAT_FILENAME = "%Y%m%d%H%M%S"
DATESTAMP_FORMAT_STRING = "%Y-%m-%d"
DATESTAMP_FORMAT_LETTER = "%A, %B %d, %Y"


class InteractiveTextField(Flowable):
    def __init__(self, text="A Text", value="", width=210):
        Flowable.__init__(self)
        self.text = text
        self.value = value
        self.width = width
        self.height = 20

    def draw(self):
        self.canv.saveState()
        form = self.canv.acroForm
        form.textfield(
            value=self.value,
            name=self.text,
            tooltip=self.text,
            width=self.width,
            height=self.height,
            fontSize=10,
            borderWidth=0.2,
            borderStyle="solid",
            borderColor=colors.grey,
            fillColor=colors.HexColor("#eeeeee"),
            relative=True,
            fieldFlags="richText",
        )
        self.canv.restoreState()
        return


class InteractiveCheckBox(Flowable):
    def __init__(self, text="A Box", checked=False):
        Flowable.__init__(self)
        self.text = text
        self.checked = checked
        self.boxsize = 20

    def draw(self):
        self.canv.saveState()
        form = self.canv.acroForm
        form.checkbox(
            checked=self.checked,
            name=self.text,
            tooltip=self.text,
            buttonStyle="cross",
            size=self.boxsize,
            borderWidth=0.2,
            borderStyle="solid",
            borderColor=colors.grey,
            fillColor=colors.HexColor("#eeeeee"),
            relative=True,
        )
        self.canv.restoreState()
        return


def smart_split(text, join_token="<br/>"):
    text_tokens = text.split(" ")
    split_index = int(len(text_tokens) / 2)
    first_part = " ".join(text_tokens[:split_index])
    second_part = " ".join(text_tokens[split_index:])
    text = f"{first_part}<br/>{second_part}"
    return text


def create_coc():
    sign_off_name = "Rachel Woolard"
    text_fields = {
        "Patient": "NNNN, NNNN",
        "Date of Birth": "01/01/2000",
        "Referring Physician": "MMMM, MMMM",
        "Primary Care Physician": "PPPP, PPPP",
        "Hospitalization Dates": "12/25/2023 - 12/31/2023",
        "Episode Dates": "01/01/2024 - 03/01/2024",
        "Hospitalization Reason": "ZZZZ ZZZZ ZZZZ ZZZZ",
    }
    checkbox_fields = {
        "Skilled Nursing": True,
        "Physical Therapy": True,
        "Occupational Therapy": False,
        "Speech Therapy": False,
        "Medical Social Work": False,
    }

    current_timestamp = datetime.now(tz=TIMEZONE_CST).replace(microsecond=0)
    current_timestamp_filename = current_timestamp.strftime(TIMESTAMP_FORMAT_FILENAME)
    current_datestamp_letter = current_timestamp.strftime(DATESTAMP_FORMAT_LETTER)
    filename = f"coc.pdf"

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=0.8 * inch,
        leftMargin=0.8 * inch,
        topMargin=0.8 * inch,
        bottomMargin=0.8 * inch,
        # showBoundary=True,
    )

    table_text_data = []
    table_text_colWidths = [6.7 * inch / 2] * 2
    table_text_style = [
        ("LEFTPADDING", (0, 0), (-1, -1), 0 * inch),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0 * inch),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0.1 * inch),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 0 * inch),
        ("TOPPADDING", (0, 0), (-1, -1), 0 * inch),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        # ("GRID", (0, 0), (-1, -1), 0.5, colors.palegreen),
        ("SPAN", (0, -1), (-1, -1)),
    ]
    table_text_counter = 0
    table_text_row_counter = 0
    table_text_row_cell_counter = 0
    for label in text_fields.keys():
        width = 6.7 * inch / 2 - 0.1 * inch
        if table_text_row_cell_counter == 0 and table_text_counter + 1 == len(text_fields):
            width = 6.7 * inch - 0.1 * inch

        if table_text_row_cell_counter == 0:
            table_text_data.append([])
            table_text_data[table_text_row_counter].append(
                [
                    Paragraph(text=label, style=styles["BodyText"]),
                    InteractiveTextField(text=label, value=text_fields[label], width=width),
                ]
            )
            table_text_row_cell_counter += 1
        elif table_text_row_cell_counter == 1:
            table_text_data[table_text_row_counter].append(
                [
                    Paragraph(text=label, style=styles["BodyText"]),
                    InteractiveTextField(text=label, value=text_fields[label], width=width),
                ]
            )
            table_text_row_counter += 1
            table_text_row_cell_counter = 0
        table_text_counter += 1

    table_text_fields = Table(
        data=table_text_data,
        colWidths=table_text_colWidths,
        style=TableStyle(table_text_style),
    )

    table_checkbox_data = []
    table_checkbox_colWidths = []
    table_checkbox_style = [
        ("LEFTPADDING", (0, 0), (-1, -1), 0 * inch),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0 * inch),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0 * inch),
        ("TOPPADDING", (0, 0), (-1, -1), 0 * inch),
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        # ("GRID", (0, 0), (-1, -1), 0.5, colors.palegreen),
    ]
    for label in checkbox_fields.keys():
        table_checkbox_data.append(InteractiveCheckBox(text=label, checked=checkbox_fields[label]))
        table_checkbox_data.append(Paragraph(text=smart_split(label), style=styles["Normal"]))
        overall_width = (6.7 * inch) / len(checkbox_fields)
        table_checkbox_colWidths.append(0.25 * overall_width)
        table_checkbox_colWidths.append(0.75 * overall_width)

    table_checkbox_fields = Table(
        data=[table_checkbox_data],
        colWidths=table_checkbox_colWidths,
        style=TableStyle(table_checkbox_style),
    )

    story = [
        Table(
            data=[
                [
                    Paragraph(
                        text="""
                        Home Nursing & Therapy Services
                        <br/>2018 Avenue B, Suite 200
                        <br/>San Antonio, TX 78215
                        <br/>Phone: (210) 822-8807 Ext. 1009
                        <br/>Fax: (210) 822-8863
                        <br/>Email: accounting@hnts.org
                        <br/>Attn: Pernetter Christian
                        """,
                        style=styles["Normal"],
                    ),
                    Image(
                        filename="logos/hnts-logo/PNG/hnts-logo.png",
                        width=2.5 * inch,
                        height=0.9375 * inch,
                        hAlign="RIGHT",
                    ),
                ],
                [
                    Paragraph(text=current_datestamp_letter, style=styles["Normal"]),
                ],
                [
                    Paragraph(text="Coordination of Care Letter", style=styles["Heading2"]),
                ],
                [
                    Paragraph(
                        text="""
                        This letter is to inform that the following patient has been admitted to 
                        Home Nursing and Therapy Services for Home Health Care services for the 
                        mentioned episode dates. The initial 485 will be signed by the referring 
                        physician mentioned below. The patient has identified the below mentioned PCP 
                        for subsequent orders and follow up regarding their medical care.
                        """,
                        style=styles["Normal"],
                    )
                ],
                [
                    table_text_fields,
                ],
                [
                    Paragraph(
                        text="""
                        After the initial evaluation, we have determined that the following services 
                        will be provided during the certification period.
                        """,
                        style=styles["Normal"],
                    )
                ],
                [
                    table_checkbox_fields,
                ],
                [
                    Paragraph(
                        text="""
                        HNTS may contact/receive from your office orders as needed for patient care. 
                        If you have any request(s) for additional information or orders, please notify 
                        us at:  
                        """,
                        style=styles["Normal"],
                    )
                ],
                [
                    Paragraph(
                        text="""
                        Phone: (210) 822-8807 
                        <br/>Fax: (210) 822-8863
                        """,
                        style=styles["Normal"],
                    )
                ],
                [
                    Paragraph(
                        text="""
                        Thank you,
                        """,
                        style=styles["Normal"],
                    )
                ],
                [
                    Paragraph(
                        text=f"""
                        <b>{sign_off_name}</b>
                        <br/>Case Manager
                        <br/>Home Nursing and Therapy Services
                        """,
                        style=styles["Normal"],
                    )
                ],
            ],
            colWidths=[3.4 * inch, 3.4 * inch],
            hAlign="LEFT",
            style=TableStyle(
                [
                    ("LEFTPADDING", (0, 0), (-1, -1), 0.05 * inch),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0.05 * inch),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 0.07 * inch),
                    ("TOPPADDING", (0, 0), (-1, -1), 0.07 * inch),
                    ("VALIGN", (0, 0), (1, 1), "TOP"),
                    ("ALIGN", (0, 0), (0, 1), "LEFT"),
                    ("ALIGN", (-1, 0), (-1, 1), "RIGHT"),
                    # ("GRID", (0, 0), (-1, -1), 0.5, colors.palegreen),
                ]
                + [("SPAN", (0, r), (-1, r)) for r in range(2, 11)]
            ),
        ),
    ]

    doc.build(story)


create_coc()
