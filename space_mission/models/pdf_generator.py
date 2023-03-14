from odoo import models, fields, api, _
from docxtpl import DocxTemplate
from docx import Document
import subprocess
import tempfile
import os
import io
from io import BytesIO
import base64
import logging

class PDFGenerator(models.Model):
    _name = 'space_mission.pdf_generator'
    _description = 'Space Documents'

    name = fields.Char(string='Nombre del documento')
    file_name = fields.Char(string='File name')
    pdf_file = fields.Binary(string="PDF Document")
    id = fields.Integer(string='ID', readonly=True)
    _logger = logging.getLogger(__name__)

    @api.model
    def generate_pdf_report(self, data):
        # Define your PDF generation code here.
        # In this example, we're using the ReportLab library to generate a simple PDF.
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.drawString(100, 750, "Welcome to Odoo PDF Generation:")
        pdf.save()
        pdf_data = buffer.getvalue()
        buffer.close()

        # Convert the PDF data to a base64-encoded string for display in the browser.
        pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')

        # Return a dictionary containing the PDF data and the file name.
        return {
            'pdf_data': pdf_base64,
            'file_name': 'my_report.pdf'
        }
    
    def open_pdf_report(self, data):
        pdf_data = io.BytesIO(self.pdf_file)
        if self.pdf_file:
            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'space_mission.pdf_generator',
                'res_id': self.id,
                'target': 'current',
                'context': {
                    'default_name': self.name,
                    'default_description': self.file_name,
                },
            }
        else:
            return {
                'type': 'ir.actions.act_url',
                'url': '/space_mission/pdf_reports/',
                'tag': 'pdf_viewer',
                'params': {
                    'title': 'PDF Report',
                    'data': pdf_base64,
                }
            }
            
    def convert_to_pdf(docx_path):
        pdf_path = os.path.splitext(docx_path)[0] + ".pdf"
        cmd = ["unoconv", "-f", "pdf", "-o", pdf_path, docx_path]
        subprocess.run(cmd, check=True)
        return pdf_path

    def edit_word(self):
        #Variables: fecha, empleador, empleador_email, empleado, empleado_email, puesto, actividades, dias_antes_terminacion_empleador, dias_antes_terminacion_empleado, periodo_empleado, periodo_empleador
        if self.pdf_file:
        #    with tempfile.NamedTemporaryFile(delete=False,dir='/tmp',suffix='.docx') as tmp_file:
        #        tmp_file.write(self.pdf_file)
        #        docx_path = tmp_file.name.replace('/tmp/','')
        #        if os.path.exists('/tmp/'+docx_path):
            decoded_data = base64.b64decode(self.pdf_file)
            doc = Document(BytesIO(decoded_data))
            temp_path = 'tmp/temp-doc.docx'
            doc.save(temp_path)
            try:
                doc = DocxTemplate(os.path.join(temp_path))
                context = {'fecha' : '7 de marzo, 2023',
                            'empleador':'William Pech',
                            'empleado':'Mario León',
                            'empleador_email':'wpech@test.com',
                            'empleado_email':'mleon@test.com',
                            'puesto':'Developer',
                            'actividades':'Desarrollador de Python para Odoo',
                            'dias_antes_terminacion_empleador':'14',
                            'dias_antes_terminacion_empleado':'14',
                            'periodo_empleado':'4',
                            'periodo_empleador':'5'}
            except Exception as e:
                self._logger.error(f"Error al crear el documento: {e}")
            doc.render(context)
            doc.save(temp_path.replace('temp-doc.docx','result.docx'))
            pdf_path = self.convert_to_pdf(temp_path.replace('temp-doc.docx','result.docx'))
            print(pdf_path)
                #else:
                #    self._logger.info("Archivo no encontrado")
        else:
            self._logger.info("Upload a document1")
        return self._logger.info("Finish")