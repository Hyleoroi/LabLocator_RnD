from PIL import Image
from fpdf import XPos

def generate_statistics(pdf, statistics_image,config):
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=0)
    pdf.title1("Heatmap")
    pdf.set_font(config["font"], config["font_style"], config["font_size"])
    pdf.cell(200,5,"Note:The heatmap can show more references then the result table, this due to a restriction of similarities close to zero %.", align="L", new_x=XPos.LEFT)


    img = Image.open(statistics_image[0])
    img_width, img_height = img.size

    # Calculate the image size while maintaining the aspect ratio
    a4_width_mm = 210
    a4_height_mm = 297
    width_percentage = 0.85  # Adjust this value as needed

    # Image dimensions
    img_width_mm = a4_width_mm * width_percentage
    img_height_mm = img_width_mm * (img_height / img_width)  # Maintain aspect ratio

    # Calculate the position to center the image on the page
    x = (a4_width_mm - img_width_mm) / 2
    y = (a4_height_mm - img_height_mm)/ 2

    # Add the image to the PDF
    pdf.image(statistics_image[0], x, y+20, img_width_mm, img_height_mm)

    #Part is dropped, it showed elapse time and similarity dispersion
    """    pdf.add_page(orientation="landscape")

    width_percentage = 1  # Adjust this value as needed
    img_width_mm = a4_width_mm * width_percentage
    img_height_mm = img_width_mm * (img_height / img_width)  # Maintain aspect ratio

    # Calculate the position to center the image on the page
    x = (a4_width_mm - img_width_mm)/2
    y = (a4_height_mm - img_height_mm)/ 2

    pdf.image(statistics_image[1], x+50, y,190)"""