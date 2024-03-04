from odoo import models,fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_stock_transport = fields.Boolean("Dispatch Management System",help="Transport management: organize packs in your fleet, or carriers.")
