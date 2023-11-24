import json

from pubmedarticle import PubmedArticle
from request import Request
from typing import List

from fpdf import FPDF, XPos, YPos

from ReportGenerator.ReportPages.front_page import generate_frontpage
from ReportGenerator.ReportPages.input_page import generate_inputpage
from ReportGenerator.ReportPages.results_page import generate_resultpage
from ReportGenerator.ReportPages.statistics_page import generate_statistics

from agrifirm_databricks_core.sharepoint.sharepoint_uploader import SharepointUploader

def read_config(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config

class MyPDF(FPDF):
    def __init__(self, orientation='P',unit='mm',format='A4',config=None):
        super().__init__(orientation, unit, format)
        self.config = config

    def header(self):
        center = (self.w / 2) - 25
        rightal = self.w - 65

        self.image("data/logo header.png", 10, 8, 59)
        self.set_font(self.config["font"],self.config["header"]["font_style"], self.config["header"]["font_size"])
        self.set_text_color(0)
        self.cell(center)
        self.cell(10, 5, self.config["header"]["company"], align="L", new_x=XPos.LMARGIN)
        self.cell(rightal)
        self.cell(10, 5, self.config["header"]["phone"], align="L", new_y=YPos.NEXT, new_x=XPos.LMARGIN)
        self.cell(center)
        self.cell(1, 5, self.config["header"]["street"], align="L", new_x=XPos.LMARGIN)
        self.cell(rightal)
        self.cell(10, 5, self.config["header"]["fax"], align="L", new_y=YPos.NEXT, new_x=XPos.LMARGIN)
        self.cell(center)
        self.cell(1, 5, self.config["header"]["city"], align="L", new_x=XPos.LMARGIN)
        self.cell(rightal)
        self.set_text_color(51, 102, 153)
        self.cell(10, 5, self.config["header"]["mailadress"], align="L", new_y=YPos.NEXT, new_x=XPos.LMARGIN)
        self.cell(center)
        self.cell(1, 5, self.config["header"]["homepage"], align="L", new_y=YPos.NEXT, link=self.config["header"]["url_homepag"], new_x=XPos.LMARGIN)
        self.set_text_color(0)
        self.ln(10)

    def footer(self):
        self.set_y(-20)
        self.set_font(self.config["font"],self.config["footer"]["font_style"], self.config["footer"]["font_size"])
        self.set_text_color(0)
        self.cell(20, 5, self.config["footer"]["footer_note"], align="L")
        # Printing page number:
        self.cell(self.w - 50)
        self.cell(1, 5, f"Page {self.page_no()}/{{nb}}", align="L")

    def title1(self, text):
        self.ln(10)
        self.set_font(self.config["font"],self.config["title1"]["font_style"], self.config["title1"]["font_size"])
        # Setting background color
        self.set_fill_color(self.config["fill_color1"])
        # Printing chapter name:
        self.cell(0, 8, text, new_x="LMARGIN", new_y="NEXT", align="L", fill=True)
        self.set_draw_color(self.config["draw_color1"])
        self.set_fill_color(self.config["fill_color2"])
        self.rect(self.get_x(), self.get_y(), 120, 0.2, style='F')
        # Performing a line break:
        self.ln(4)

def generate_pdf_report(request: Request, result_table: List[PubmedArticle],statistics_image):
    config = read_config("data/config.json")

    pdf = MyPDF(config=config)
    pdf.add_font('DejaVuSans', fname='data/DejaVuSans.ttf')
    pdf.set_fallback_fonts(['DejaVuSans'])

    #add here the pages you want for the report
    generate_frontpage(pdf,config, request.req_id, request.request_person)
    generate_inputpage(pdf,config,Keywords= request.query.replace('AND',', '), Region= request.region_of_interest, Abstract=request.abstract)
    generate_resultpage(pdf,result_table,config)
    generate_statistics(pdf, statistics_image)
    
    datalake_path = "/dbfs/mnt/current/datascience/platinum/general/innolab/result.pdf"
    pdf.output(datalake_path)
    sharepoint_path = f"{request.req_id}.pdf"
    uploader = SharepointUploader()
    uploader.upload_project_file("innolab", datalake_path, sharepoint_path)