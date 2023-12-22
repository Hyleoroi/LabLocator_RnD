from fpdf import FPDF, XPos, YPos
from fpdf.errors import FPDFUnicodeEncodingException

def sanitize_string(text):
    try:
        return str(text)
    except UnicodeEncodeError:
        # Replace or filter problematic characters causing encoding errors
        sanitized_text = ''.join(c if ord(c) < 256 else '' for c in text)
        return sanitized_text

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

        #Some encoding errors with the font, difficult to change because people can paste there text with al kinds of characters. Just skip the special ones
        v_str = sanitize_string(v) if v is not None else ""
        sanitized_v_str = ''.join(c if ord(c) < 256 else '' for c in v_str)

        try:
            pdf.multi_cell(v_width, 5, sanitized_v_str, align="J", new_y=YPos.NEXT, new_x=XPos.LMARGIN)
        except UnicodeEncodeError:
            # Handle the encoding error, perhaps by logging the issue or skipping this part
            pass  # Or perform an action as per your requirement
