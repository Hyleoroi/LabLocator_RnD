import math
import textwrap
from typing import List

from pubmedarticle import PubmedArticle

def generate_resultpage(pdf, datatable: List[PubmedArticle], config, similarities):
    # Specific for scout4you tool json file
    pdf.add_page(orientation="landscape")
    pdf.title1('Top 15 similar references of ' + str(len(similarities)) + ' references')
    col_width = 20
    line_height = 24

    def tableheader():
        pdf.set_font(config["font"],config["table"]["title_style"], config["table"]["font_size"])
        pdf.set_fill_color(config["table"]["title_fill_color"])
        line_height_header = pdf.font_size + 2

        pdf.multi_cell(col_width, line_height_header, 'Pubmed ID', border=1, new_x="RIGHT", new_y="TOP",
                        max_line_height=pdf.font_size, fill=True)
        pdf.multi_cell(col_width - 1.5, line_height_header, "Similarity", border=1, new_x="RIGHT", new_y="TOP",
                        max_line_height=pdf.font_size, fill=True)
        pdf.multi_cell(col_width + 5, line_height_header, 'Country', border=1, new_x="RIGHT", new_y="TOP",
                        max_line_height=pdf.font_size, fill=True, align='C')
        pdf.multi_cell(132, line_height_header, 'Abstract', border=1, new_x="RIGHT",
                        new_y="TOP", max_line_height=pdf.font_size, fill=True)
        pdf.multi_cell(30, line_height_header, "Author name", border=1, new_x="RIGHT", new_y="TOP",
                        max_line_height=pdf.font_size, fill=True, align='C')
        pdf.multi_cell(52,line_height_header, "Affiliation", border=1, new_x="RIGHT", new_y="TOP",
                        max_line_height=pdf.font_size, fill=True, align='C')
        pdf.ln(line_height_header)
        #reset font to the text in the table
        pdf.set_font(config["font"], config["table"]["text_style"], config["table"]["font_size"])
        pdf.set_fill_color(config["table"]["row_fill_color"])

    tableheader()

    bfill = True
    for row in datatable:
        # Swap colors per row
        if bfill == True:
            bfill = False
        else:
            bfill = True

        # change layout of the similarity number
        sim = row.similarity * 100
        sim = str(sim)[0:4]
        sim = sim + '%'


        #Check if a new line will start on a new page. If so then repead the tableheader
        if (pdf.y+line_height>pdf.page_break_trigger):
            tableheader()

        # fix for multicel centers horizontal on top. No option to change this, so extra calculation how mutch empty lines to add.
        try:
            if row.last_author is not None:
                if row.last_author.affiliation is not None:
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
            else:
                if row.first_author is not None and row.first_author.affiliation is not None:
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

def generate_resultpage_no_results(pdf, config):
    '''
    Make a pdf when there are no referenced found on the internet with a suggestion to make a new inpur.
    :return: pdf report
    '''

    pdf.add_page(orientation="landscape")
    pdf.title1('Top 15 similar references of 0 references')
    col_width = 20
    line_height = 6

    pdf.set_font(config["font"], size=12)
    pdf.write(line_height, "It looks like there are no references found or there are no references located in your region of interest.\nYou can try again and limit the keywords so you search in a broader scope: ")
    pdf.set_text_color(51, 102, 204)
    pdf.write(line_height, "Input form for RefeR&D.", link='https://agrifirm.sharepoint.com/sites/rdglobal/innolab/Lists/Innolab%20LabLocator/NewForm.aspx?Source=https%3A%2F%2Fagrifirm%2Esharepoint%2Ecom%2Fsites%2Frdglobal%2Finnolab%2FLists%2FInnolab%2520LabLocator%2FAllItems%2Easpx&ContentTypeId=0x010012448E5AF7E03F49A70BFCF47B4FD48100362EEDC5A5AE394EBB6C5F582B8151E6&RootFolder=%2Fsites%2Frdglobal%2Finnolab%2FLists%2FInnolab%20LabLocator')