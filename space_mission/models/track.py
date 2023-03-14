
from odoo import api, fields, models

class UtmMyTrack(models.Model):
    _name = 'space_mission.my_track'
    _description = 'My Tracking Object'

    name = fields.Char(string='Name', required=True)

class Track(models.Model):
    _name = 'space_mission.track'
    _inherit = ['utm.mixin']
    _description = 'My Tracked Object'

    target = fields.Many2one('space_mission.my_track','Target')
    @api.model
    def tracking_fields(self):
        result = super(Track, self).tracking_fields()
        result.append([
            #("URL_PARAMETER", "FIELD_NAME_MIXIN", "NAME_IN_COOKIES")
            ('target', 'target', 'odoo_utm_my_field')
        ])
        return result