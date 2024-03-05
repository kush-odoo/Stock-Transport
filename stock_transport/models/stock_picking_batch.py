from odoo import api, fields, models, _

class StockPickingBatch(models.Model):
    _inherit = 'stock.picking.batch'

    dock_id = fields.Many2one('stock.dock', 'Dock')   
    vehicle_id = fields.Many2one('fleet.vehicle', 'Vehicle', required=True, store=True)
    category_id = fields.Many2one('fleet.vehicle.model.category', 'Category', related='vehicle_id.category_id',store=True)
    load_weight = fields.Float(string = 'Load Weight', compute = '_compute_product_weight', store = True)
    load_volume = fields.Float(string = 'Load Volume', compute = '_compute_product_volume', store = True)
    max_category_volume = fields.Float(related='category_id.max_volume', store=True)
    max_category_weight = fields.Float(related='category_id.max_weight', store=True)
    volume_percentage = fields.Float(string='Volume Percentage', compute='_compute_percentage', store=True)
    weight_percentage = fields.Float(string='Weight Percentage', compute='_compute_percentage', store=True)
    driver_id = fields.Many2one('res.partner', related= 'vehicle_id.driver_id')
    transfer_count = fields.Integer(string='Transfer',compute='_compute_transfers',store=True)
    line_count = fields.Integer(string='Line',compute='_compute_lines',store=True)


    @api.depends('load_volume', 'load_weight', 'max_category_volume', 'max_category_weight')
    def _compute_percentage(self):
        for load in self:
            if load.max_category_volume and load.load_volume:
                load.volume_percentage = (load.load_volume / load.max_category_volume) * 100.0
            else:
                load.volume_percentage = 0.0

            if load.max_category_weight and load.load_weight:
                load.weight_percentage = (load.load_weight / load.max_category_weight) * 100.0
            else:
                load.weight_percentage = 0.0

    @api.depends('move_line_ids.product_id','move_line_ids.quantity')
    def _compute_product_weight(self):
        for load in self:
            load_weight = 0.0
            for move_line in load.move_line_ids:
                load_weight += move_line.product_id.weight*move_line.quantity
            load.load_weight = load_weight    
    
    @api.depends('move_line_ids.product_id', 'move_line_ids.quantity')
    def _compute_product_volume(self):
        for load in self:
            load_volume = 0.0
            for move_line in load.move_line_ids:
                load_volume += move_line.product_id.volume * move_line.quantity
            load.load_volume = load_volume
    
    @api.depends('picking_ids')
    def _compute_transfers(self):
        for record in self:
            record.transfer_count=len(record.picking_ids)

    @api.depends('move_line_ids')
    def _compute_lines(self):
        for record in self:
            record.line_count=len(record.move_line_ids)
