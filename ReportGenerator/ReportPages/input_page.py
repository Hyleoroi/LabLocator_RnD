from fpdf import FPDF, XPos, YPos


def generate_inputpage(pdf, config, **kwargs):
    pdf.add_page()
    pdf.title1("Request input")
    pdf.set_font(config["font"],config["font_style"], config["font_size"])

    def get_max_str(lst):
        return max(lst, key=len)

    # Get width's needed for format because of variable input.
    longestString = get_max_str(kwargs)
    longestWidth = pdf.get_string_width(str(longestString)) + 10
    v_width = pdf.w - longestWidth - 30



    for k, v in kwargs.items():
        pdf.cell(2)
        pdf.cell(longestWidth, 5, k + ":", align="L", new_x=XPos.LEFT)
        pdf.cell(longestWidth)
        v_str = str(v) if v is not None else ""
        pdf.multi_cell(v_width, 5, v_str, align="J", new_y=YPos.NEXT, new_x=XPos.LMARGIN)
