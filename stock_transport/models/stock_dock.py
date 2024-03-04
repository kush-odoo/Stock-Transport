from odoo import fields, models, api

class StockDock(models.Model):
    _name = 'stock.dock'
    _description = "DockYard Name for the Stock"

    dock_ids = fields.One2many("stock.picking.batch","dock_id" , string = "Docks")
    name = fields.Char(string = "Dockyard Name")
