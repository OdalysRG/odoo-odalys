from odoo import http
from odoo.http import request
import base64

class PdfController(http.Controller):
    @http.route('/fillers_module/pdf_reports/', type='http', auth='public', website=True, sitemap=False)
    def pdf_report(self, **kw):
        pdf_generator = request.env['fillers_module.pdf_generator'].search([])
        pdf_data = pdf_generator.generate_pdf_report(kw).get('pdf_data')
        if pdf_data:
            pdf_base64 = base64.b64decode(pdf_data)
            return request.make_response(
                pdf_base64,
                headers=[('Content-Type', 'application/pdf')]
            )
        else:
            return request.not_found()
