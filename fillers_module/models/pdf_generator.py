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
    _name = 'fillers_module.pdf_generator'
    _description = 'Filler Documents'
    _inherits = {'res.partner': 'employees'}
    
    name = fields.Char(string="Employee", related='employees.name')
    employee_id = fields.Char(string='Employee ID', required=True, copy=False, readonly=True, 
                              default=lambda self: _('New'))
    file_name = fields.Selection(string ='File Name',
                                 selection = [('contrato por tiempo determinado', 'Contrato por Tiempo Determinado'),
                                              ('contrato por tiempo indeterminado', 'Contrato por Tiempo Indeterminado'),
                                              ('otro','Otro')], copy= False, required=True)
    word_file = fields.Binary(string='Word Document')
    pdf_file = fields.Binary(string='Pdf Word', readonly=True)
    temp_path = '/tmp/temp-doc.docx'
    _logger = logging.getLogger(__name__)

    employees = fields.Many2one(comodel_name='res.partner', string='Employee', required=True)
    
    employer = fields.Many2one(comodel_name='res.partner', string='Employer', required=True)
    
    @api.model
    def create(self, vals):
        vals['employee_id']= self.env['ir.sequence'].next_by_code('employee.id')
        return super(PDFGenerator, self).create(vals)

    @api.model
    def generate_pdf_report(self, data):
        # Define your PDF generation code here.
        # In this example, we're using the ReportLab library to generate a simple PDF.
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.drawString(100, 750, 'Welcome to Odoo PDF Generation:')
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
        pdf_data = io.BytesIO(self.word_file)
        if self.word_file:
            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'fillers_module.pdf_generator',
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
                'url': '/fillers_module/pdf_reports/',
                'tag': 'pdf_viewer',
                'params': {
                    'title': 'PDF Report',
                    'data': pdf_base64,
                }
            }
            
    def convert_to_pdf(self, docx_path):
        pdf_path = os.path.splitext(docx_path)[0] + '.pdf'
        cmd = ['unoconv', '-f', 'pdf', '-o', pdf_path, docx_path]
        subprocess.run(cmd, check=True)
        return pdf_path

    def edit_word(self):
        #Variables: fecha, empleador, empleador_email, empleado, empleado_email, puesto, actividades, dias_antes_terminacion_empleador, dias_antes_terminacion_empleado, periodo_empleado, periodo_empleador
        if self.word_file:
        #    with tempfile.NamedTemporaryFile(delete=False,dir='/tmp',suffix='.docx') as tmp_file:
        #        tmp_file.write(self.word_file)
        #        docx_path = tmp_file.name.replace('/tmp/','')
        #        if os.path.exists('/tmp/'+docx_path):
            decoded_data = base64.b64decode(self.word_file)
            doc = Document(BytesIO(decoded_data))
            doc.save(self.temp_path)
            try:
                doc = DocxTemplate(os.path.join(self.temp_path))
                context = {'fecha' : '7 de marzo, 2023',
                            'empleador':self.employer.name,
                            'empleado':self.employees.name,
                            'empleador_email':self.employer.email,
                            'empleado_email':self.employees.email,
                            'puesto':self.employees.function,
                            'actividades':'Desarrollador de Python para Odoo',
                            'dias_antes_terminacion_empleador':'14',
                            'dias_antes_terminacion_empleado':'14',
                            'periodo_empleado':'4',
                            'periodo_empleador':'5'}
            except Exception as e:
                self._logger.error(f'Error al crear el documento: {e}')
            doc.render(context)
            doc.save(self.temp_path.replace('temp-doc.docx','result.docx'))
            pdf_path = self.convert_to_pdf(self.temp_path.replace('temp-doc.docx','result.docx'))
            if self.pdf_file:
                with open(pdf_path, 'rb') as file:
                    pdf_contents = bytes(file.read())
                    pdf_data = base64.b64encode(pdf_contents)
                my_record = self.env['fillers_module.pdf_generator'].search([('id','=',self.id)])
                my_record.write({'pdf_file':False})
                my_record.write({'pdf_file':pdf_data})
                print(self.id)
            else:
                with open(pdf_path, 'rb') as file:
                    pdf_contents = bytes(file.read())
                    pdf_data = base64.b64encode(pdf_contents)
                my_record = self.env['fillers_module.pdf_generator'].search([('id','=',self.id)])
                my_record.write({'pdf_file':pdf_data})
                print(self.id)
                #else:
                #    self._logger.info('Archivo no encontrado')
        else:
            self._logger.info('Upload a document1')
        return self._logger.info('Finish')