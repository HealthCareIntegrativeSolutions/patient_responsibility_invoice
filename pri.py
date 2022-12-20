from functools import partial

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, inch
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Image

import dataformatter

styles = getSampleStyleSheet()
styleN = styles["Normal"]
styleH = styles["Heading1"]

styles.add(ParagraphStyle(name="Justify", alignment=TA_JUSTIFY))
styles.add(ParagraphStyle(name="RIGHT", alignment=TA_RIGHT))
styles.add(ParagraphStyle(name="LEFT", alignment=TA_LEFT))


def footer(canvas, doc):
    canvas.saveState()
    P = Paragraph("This is a multi-line footer.  It goes on every page.  " * 5, styleN)
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

    doc = BaseDocTemplate("test.pdf", pagesize=letter)
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    template = PageTemplate(id="test", frames=frame, onPage=footer)
    doc.addPageTemplates([template])

    text = []
    for i in range(111):
        text.append(Paragraph("This is line %d." % i, styleN))
    doc.build(text)


def create_header(invoice_number, styles):
    logo = "C:/Users/nagas/OneDrive/Documents/Sankrithi Consulting/HNT_HIS/Projects/Vivify Implementation/Brochure/Modified_logos/logos/hnts-logo/PNG/hnts-logo.png"
    im = Image(logo, 2 * inch, 0.75 * inch)
    im.hAlign = "RIGHT"

    from_address_parts = [
        "Home Nursing & Therapy Services",
        "2018 Avenue B, Suite 200",
        "San Antonio, TX 78215",
        "Ph: (210)-822-8807 Ext. 1009",
        "Fax: (210)-822-8863",
        "email: accounting@hnts.org",
        "Attn: Pernetter Christian",
    ]
    full_address = []
    for part in from_address_parts:
        ptext = "<font size=10>%s</font>" % part.strip()
        full_address.append(Paragraph(ptext, styles["LEFT"]))

    headerdata = [[" ", full_address, invoice_number, [im], ""]]
    h = Table(headerdata, [0.4 * inch, 2.5 * inch, 3 * inch, 2 * inch, 0.2 * inch])
    return h


def createdoc2():
    doc = BaseDocTemplate("test2.pdf", pagesize=letter)
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 2 * cm, id="normal")
    header_content = Paragraph("This is a multi-line header.  It goes on every page.  " * 8, styleN)
    footer_content = Paragraph("This is a multi-line footer.  It goes on every page.  " * 5, styleN)
    template = PageTemplate(
        id="test",
        frames=frame,
        onPage=partial(header_footer, header=header_content, footer=footer_content),
    )
    doc.addPageTemplates([template])

    text = []
    for i in range(111):
        text.append(Paragraph("This is line %d." % i, styleN))
    doc.build(text)


def create_patient_responsibity_invoice(fname, invoicenum, claims_df, to_address_parts, insurance_info):
    # #doc = SimpleDocTemplate(fname, pagesize=letter,
    #                         rightMargin=50, leftMargin=20,
    #                         topMargin=20, bottomMargin=10)

    doc = BaseDocTemplate(fname, pagesize=letter, rightMargin=50, leftMargin=20, topMargin=40, bottomMargin=10)
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 2.5 * cm, id="normal")
    invoicenum = invoicenum
    header_content = create_header(invoicenum, styles)
    footer_content = Paragraph("THANK YOU FOR YOUR BUSINESS!", styles["Justify"])
    # footer_content.append(Paragraph("For payment arrangements Contact Pernetter Christian at 210-822-8807 # 1009", styles['Justify']))
    template = PageTemplate(
        id="test",
        frames=frame,
        onPage=partial(header_footer, header=header_content, footer=footer_content),
    )
    doc.addPageTemplates([template])
    Story = []
    Story.append(Spacer(1, 12))
    # Recipient's address
    ptext = "<font size=12>To</font>"
    to_P = Paragraph(ptext, styles["RIGHT"])
    # to_address_parts = ["GALLEGOS, RAY", "1711 SILVER MOUNTAIN DR", "SAN ANTONIO, TX 78264", "(210)-262-6209"]
    # Create
    to_address = []
    for part in to_address_parts:
        ptext = "<font size=10>%s</font>" % part
        to_address.append(Paragraph(ptext, styles["LEFT"]))

    insurance_text = []
    for part in insurance_info:
        ptext = "<font size=10>%s</font>" % part
        insurance_text.append(Paragraph(ptext, styles["RIGHT"]))

    to_data = [
        [to_P, "", ""],
        ["", to_address, insurance_text],
    ]
    to_T = Table(to_data, [1.0 * inch, 3 * inch, 4.5 * inch])
    Story.append(to_T)

    name_parts = to_address_parts[0].split(",")
    full_name = name_parts[1].strip() + " " + name_parts[0].strip()
    Story.append(Spacer(1, 20))
    ptext = "<font size=12>Dear %s:</font>" % full_name.title()
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 20))

    ptext = (
        '<font size=12>Thank you for trusting HNTS to provide you with home healthcare services.  You should have received an "Explanation of Benefits" from your insurance carrier regarding your claims.'
        " This invoice is for the patient's responsibility for the services rendered by HNTS.</font>"
    )
    Story.append(Paragraph(ptext, styles["Justify"]))

    Story.append(Spacer(1, 20))
    ptext = "<font size=12>Check or Money order payable to:</font>"
    Story.append(Paragraph(ptext, styles["Justify"]))
    ptext = "<font size=12>Home Nursing & Therapy Services</font>"
    Story.append(Paragraph(ptext, styles["Justify"]))
    ptext = "<font size=12>Attn: Accounts Payable</font>"
    Story.append(Paragraph(ptext, styles["Justify"]))
    ptext = "<font size=12>2018 Avenue B, Ste. 200</font>"
    Story.append(Paragraph(ptext, styles["Justify"]))
    ptext = "<font size=12>San Antonio, TX 78215</font>"
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 20))
    ptext = "<font size=12>Credit Card payment:</font>"
    Story.append(Paragraph(ptext, styles["Justify"]))
    ptext = "<font size=12>Email accounting@hnts.org for an invoice to be emailed directly to you for secure online payment.</font>"
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 20))
    ptext = "<font size=12>Questions/ Payment arrangements :</font>"
    Story.append(Paragraph(ptext, styles["Justify"]))
    ptext = "<font size=12>Contact Pernetter Christian at accounting@hnts.org or 210-822-8807 #1009</font>"
    Story.append(Paragraph(ptext, styles["Justify"]))

    Story.append(Spacer(1, 20))

    header_row = [
        [
            " Claim\nItem #",
            "Description of Service",
            "Amt \n Billed to \n Insurance",
            "Insurance\nAdjustment",
            "Insurance\nPayment to\n Agency",
            "Patient's\nResponsible\nAmount",
        ],
    ]

    lista = header_row + claims_df.values.tolist()

    t_style = TableStyle(
        [
            ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
            ("TEXTCOLOR", (1, 1), (-2, -1), colors.black),
            ("VALIGN", (0, 0), (0, -1), "BOTTOM"),
            ("ALIGN", (0, 0), (0, -1), "CENTER"),
            ("ALIGN", (0, 0), (-1, 0), "RIGHT"),
            ("TEXTCOLOR", (0, 0), (0, -1), colors.black),
            ("ALIGN", (1, -1), (-1, -1), "RIGHT"),
            ("VALIGN", (0, -1), (-1, -1), "MIDDLE"),
            ("TEXTCOLOR", (0, -1), (-1, -1), colors.black),
            ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
            ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.85, 0.86, 0.8)),
            ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
            ("BOX", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ]
    )
    s = getSampleStyleSheet()
    s = s["BodyText"]
    s.wordWrap = "CJK"
    t = Table(
        lista,
        colWidths=[
            0.6 * inch,
            2.7 * inch,
            1 * inch,
            1 * inch,
            1 * inch,
            1.3 * inch,
        ],
        repeatRows=1,
    )
    t.setStyle(t_style)

    Story.append(t)
    doc.build(Story)


def read_claims(claim_file_name):

    df = pd.read_csv(claim_file_name)
    return df


def process_claims(df, invoiceprefix):
    All_MRNs = df["MRN"].unique()
    invoicenum = 0
    patientnum = 0
    for current_mrn in All_MRNs:
        df_patient = df["MRN"] == current_mrn
        current_claims = df.loc[df_patient]
        patientnum = patientnum + 1
        episode_ranges = pd.Series(current_claims["EPISODE_DATE_RANGE"].unique())
        episode_ranges = episode_ranges.sort_values(ascending=True)
        episode_ranges = episode_ranges.reset_index(drop=True)
        episodenum = 0

        for episode_range in episode_ranges:

            episodenum = episodenum + 1
            claims_df = current_claims.loc[current_claims["EPISODE_DATE_RANGE"] == episode_range]
            claims_df = claims_df.sort_values(by=["CLAIM_DATE_RANGE"], ascending=True)

            description_of_service = "Billed Insurance for claims\n" + claims_df["CLAIM_DATE_RANGE"] + " \non " + claims_df["BILLED_DATE"]
            billed_to_insurance = claims_df["BILLED_AMOUNT"]
            Insurancce_Adjustement = claims_df["ADJUSTMENT"]
            payment_to_agency = claims_df["PAYMENT"]
            patients_responsible_amount = claims_df["NET_RECEIVABLE"]
            claims_dict = {
                "Description of Service": description_of_service,
                "Billed to Insurance": billed_to_insurance,
                "Insurance Adjustement": Insurancce_Adjustement,
                "Payment to Agency": payment_to_agency,
                "Patient's Responsible Amount ": patients_responsible_amount,
            }
            new_claims_df = pd.concat(claims_dict, axis=1)
            new_claims_df.reset_index(inplace=True)
            new_claims_df = new_claims_df.rename(columns={"index": "Item"})
            new_claims_df["Item"] = new_claims_df.index + 1
            new_claims_df = new_claims_df.append(new_claims_df.sum(numeric_only=True), ignore_index=True)

            # Apply Formatting
            new_claims_df["Item"] = new_claims_df["Item"].apply(dataformatter.formatter_number0)
            new_claims_df["Billed to Insurance"] = new_claims_df["Billed to Insurance"].apply(dataformatter.formatter_currency_with_cents)
            new_claims_df["Insurance Adjustement"] = new_claims_df["Insurance Adjustement"].apply(dataformatter.formatter_currency_with_cents)
            new_claims_df["Payment to Agency"] = new_claims_df["Payment to Agency"].apply(dataformatter.formatter_currency_with_cents)
            new_claims_df["Patient's Responsible Amount "] = new_claims_df["Patient's Responsible Amount "].apply(dataformatter.formatter_currency_with_cents)

            new_claims_df.iloc[-1, new_claims_df.columns.get_loc("Description of Service")] = "Total"
            new_claims_df.iloc[-1, new_claims_df.columns.get_loc("Item")] = ""

            u_full_address = claims_df[["PATIENT", "ADDRESS", "CITY", "STATE", "ZIPCODE", "PHONE"]].drop_duplicates().values.tolist()[0]
            full_address = []
            full_address.append(u_full_address[0])
            full_address.append(u_full_address[1])
            full_address.append(u_full_address[2] + ", " + str(u_full_address[3]) + "  " + str(u_full_address[4]))
            # full_address.append('Ph: '+ u_full_address[5])

            invoicenum = "INVOICE #\n" + str(invoiceprefix) + "-" + str(patientnum) + "-" + str(episodenum)

            insurance_info = []
            u_ins_info = claims_df[["PAYOR", "INSURANCE_ID"]].drop_duplicates().values.tolist()[0]
            insurance_info.append("Insurance Name: " + u_ins_info[0])
            insurance_info.append("Insurance ID: " + str(u_ins_info[1]))

            create_patient_responsibity_invoice(
                "file_" + current_mrn + episode_range + ".pdf",
                invoicenum=invoicenum,
                claims_df=new_claims_df,
                to_address_parts=full_address,
                insurance_info=insurance_info,
            )


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    # createdoc()
    # createdoc2()
    # create_patient_responsibity_invoice("Inv-02.pdf")
    # old_claim_file_name = 'C:/Users/nagas/Downloads/04_29_2021_MRs/Payors_without_BCBS_05_01_2021.csv'
    # claim_file_name = 'C:/Users/nagas/Downloads/07_26_2021_PR/PATIENT_RESPONSIBILITY_07_26_2021.csv'
    # claim_file_name = 'C:/Users/nagas/Downloads/07_26_2021_PR/PATIENT_RESPONSIBILITY_04_21_2022.csv'
    claim_file_name = "C:/Users/nagas/Downloads/07_26_2021_PR/PATIENT_RESPONSIBILITY_08_31_2022.csv"
    df = read_claims(claim_file_name)
    invoiceprefix = "08_31-2022"
    process_claims(df, invoiceprefix)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
