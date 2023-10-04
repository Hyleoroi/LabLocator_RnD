import datetime
from fpdf import FPDF, XPos, YPos

def generate_frontpage(pdf, config, reportID, attentededTo):
    pdf.add_page()

    #Title boxed and colored rectangle at the right
    pdf.set_font(config["font"],config["front_page"]["titel"]["font_style"], config["front_page"]["titel"]["font_size"])
    pdf.cell(10, 50, new_y=YPos.NEXT)
    pdf.cell(170, 15, config["front_page"]["titel"]["text"], align="C", new_y=YPos.NEXT, border=1)
    pdf.set_draw_color(config["draw_color1"])
    pdf.set_fill_color(config["fill_color2"])
    pdf.rect(18, 90, 1, 15, style='F')

    #centered A4 pag logo
    pdf.image("data/logo frontpage.png", x=30, y=110, w=150)

    #Additional data for the frontpage (request, reportname, reportdate)
    pdf.set_font(config["font"],config["front_page"]["report_info"]["font_style"], config["front_page"]["report_info"]["font_size"])
    pdf.cell(10, 140, new_y=YPos.NEXT, new_x=XPos.LMARGIN)
    pdf.cell(10)
    pdf.cell(20, 5, 'Report ID: ', align="L", new_x=XPos.LEFT)
    pdf.cell(30)
    pdf.cell(10, 5, reportID, align="L", new_y=YPos.NEXT, new_x=XPos.LMARGIN)
    pdf.cell(10)
    pdf.cell(10, 5, 'Att.: ', align="L", new_x=XPos.LMARGIN)
    pdf.cell(40)
    pdf.cell(10, 5, attentededTo, align="L", new_y=YPos.NEXT, new_x=XPos.LMARGIN)
    pdf.cell(10)
    pdf.cell(10, 5, 'Report date: ', align="L", new_x=XPos.LMARGIN)
    pdf.cell(40)

    def report_date():
        today = datetime.date.today()
        formatted_date = today.strftime("%Y/%m/%d")
        return formatted_date

    pdf.cell(10, 5, report_date(), align="L", new_y=YPos.NEXT, new_x=XPos.LMARGIN)
    pdf.rect(18, 245, 1, 15, style='F')