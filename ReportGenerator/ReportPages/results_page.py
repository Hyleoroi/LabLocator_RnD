import math
import textwrap
from typing import List

from pubmedarticle import PubmedArticle

def generate_resultpage(pdf, datatable: List[PubmedArticle], config):
    # Specific for scout4you tool json file
    pdf.add_page(orientation="landscape")
    pdf.title1('Top 15 similar articles')
    pdf.set_font(config["font"],config["table"]["title_style"], config["table"]["font_size"])
    pdf.set_fill_color(config["table"]["title_fill_color"])
    line_height = pdf.font_size + 2
    col_width = 20

    pdf.multi_cell(col_width, line_height, 'Pubmed ID', border=1, new_x="RIGHT", new_y="TOP",
                    max_line_height=pdf.font_size, fill=True)
    pdf.multi_cell(col_width - 1.5, line_height, "Simularity", border=1, new_x="RIGHT", new_y="TOP",
                    max_line_height=pdf.font_size, fill=True)
    pdf.multi_cell(col_width + 5, line_height, 'Country', border=1, new_x="RIGHT", new_y="TOP",
                    max_line_height=pdf.font_size, fill=True, align='C')
    pdf.multi_cell(132, line_height, 'Abstract', border=1, new_x="RIGHT",
                    new_y="TOP", max_line_height=pdf.font_size, fill=True)
    pdf.multi_cell(30, line_height, "Author name", border=1, new_x="RIGHT", new_y="TOP",
                    max_line_height=pdf.font_size, fill=True, align='C')
    pdf.multi_cell(52,line_height, "Affiliation", border=1, new_x="RIGHT", new_y="TOP",
                    max_line_height=pdf.font_size, fill=True, align='C')
    pdf.ln(line_height)

    pdf.set_font(config["font"],config["table"]["text_style"], config["table"]["font_size"])
    line_height = 24
    pdf.set_fill_color(config["table"]["row_fill_color"])
    bfill = True
    for row in datatable:
        # Swap colors per row
        if bfill == True:
            bfill = False
        else:
            bfill = True

        # change layout of the simularity number
        sim = row.similarity * 100
        sim = str(sim)[0:4]
        sim = sim + '%'

        # fix for multicel centers horizontal on top. No option to change this, so extra calculation how mutch empty lines to add.

        try:
            if row.first_author is not None:
                if row.first_author.affiliation is not None:
                    txt_width = pdf.get_string_width(row.first_author.affiliation)
                    number_of_lines = txt_width / (52 - 1)
                    number_of_lines = math.ceil(number_of_lines)
                    number_of_lines = math.ceil(((10 - number_of_lines) / 2))-1

                    author_country = row.first_author.country
                    author_name = row.first_author.fullname
                    affiliation_txt = row.first_author.affiliation
                    affiliation_txt = '\n' * number_of_lines + affiliation_txt
                else:
                    pass
            else:
                if row.last_author is not None and row.last_author.affiliation is not None:
                    txt_width = pdf.get_string_width(row.last_author.affiliation)
                    number_of_lines = txt_width / (52 - 1)
                    number_of_lines = math.ceil(number_of_lines)
                    number_of_lines = math.ceil(((10 - number_of_lines) / 2))-1

                    author_country = row.last_author.country
                    author_name = row.last_author.fullname
                    affiliation_txt = row.last_author.affiliation
                    affiliation_txt = '\n' * number_of_lines + affiliation_txt
                else:
                    pass

            pdf.set_text_color(config["table"]["font_color"])
            pdf.multi_cell(col_width, line_height, str(row.pmid), border=1, new_x="RIGHT", new_y="TOP",
                           max_line_height=pdf.font_size, fill=bfill, link=row.url)
            pdf.set_text_color(0)
            pdf.multi_cell(col_width - 1.5, line_height, sim, border=1, new_x="RIGHT", new_y="TOP",
                           max_line_height=pdf.font_size, fill=bfill)
            pdf.multi_cell(col_width + 5, line_height, author_country, border=1, new_x="RIGHT",
                           new_y="TOP",
                           max_line_height=pdf.font_size, fill=bfill, align='C')
            pdf.multi_cell(132, line_height, '\n' + textwrap.shorten(row.abstract, width=650), border=1,
                           new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size, fill=bfill)
            pdf.multi_cell(30, line_height, author_name, border=1, new_x="RIGHT", new_y="TOP",
                           max_line_height=pdf.font_size, fill=bfill, align='C')
            pdf.multi_cell(52, line_height, affiliation_txt, border=1, new_x="RIGHT", new_y="TOP",
                           max_line_height=pdf.font_size, fill=bfill, align='C')
            pdf.ln(line_height)

        except Exception as e:
            print(e)
            print(row.pmid)
            continue

