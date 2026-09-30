import os
from datetime import datetime
from fpdf import FPDF

def save_pdf(layout: list) -> str:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font('Helvetica', '', 12)
        
    for frame in layout:
        pdf.add_page()
        pdf.set_font('Helvetica', 'B', 16)
        pdf.cell(0, 12, text=f"Panel {frame['panel']}: {frame['title']}", ln=True, align="C")
        pdf.ln(4)
        
        image_y = 32
        target_box_height = 95
        
        if os.path.exists(frame['image_path']):
            pdf.image(frame['image_path'], x=15, y=image_y, w=pdf.epw - 10, h=target_box_height)
        else:
            pdf.set_y(image_y)
            pdf.multi_cell(0, 10, text="System storage verification for graphic resource asset failed targets.")
            
        pdf.set_y(image_y + target_box_height + 12)
        
        if frame.get('scene_description'):
            pdf.set_font('Helvetica', 'I', 11)
            pdf.multi_cell(0, 6, text=f"Scene Parameters: {frame['scene_description']}")
            pdf.ln(2)
            
        pdf.set_font('Helvetica', '', 12)
        pdf.multi_cell(0, 8, text=frame['text'])
        
    output_filename = f"comic_export_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    destination_path = os.path.join("static/exports", output_filename)
    
    pdf.output(destination_path)
    return destination_path
