from odoo import fields, models, api

class StockPicking(models.Model):
    _inherit = "stock.picking"

    volume = fields.Float(string="Volume", compute="_compute_volume")

    @api.depends('move_ids')
    def _compute_volume(self):
        for record in self:
            counted_volume = sum(
                transfer.product_id.product_tmpl_id.volume * transfer.quantity
                for transfer in record.move_ids
                if transfer.product_id and transfer.product_id.product_tmpl_id.volume
            )
            record.volume = counted_volume
