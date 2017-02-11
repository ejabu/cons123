# -*- coding: utf-8 -*-

from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields

class cost_header(models.Model):

    _name= "cost.header"

    cost_header_number = fields.Integer(string='Cost Header Number', required=True)
    name = fields.Char(string='Cost Header Name', required=True)
    cost_header_cost = fields.Float(string='Cost of Header', compute='_compute_cost', store=True)
    cost_code = fields.Many2many('cost.code', 'cost_code_to_header_rel', 'header_id', 'code_id', string="Cost Code")
    work_package = fields.Many2many('work.package', 'cost_header_to_work_package_rel', 'header_id', 'package_id', string="Work Package")

    _defaults = {
        'name'  : 'Cost Header'
    }
    @api.one
    @api.depends('cost_code')
    def _compute_cost(self):
        # import ipdb; ipdb.set_trace()
        cost_header_cost = 0
        for cost_code_id in self.cost_code:
            cost_header_cost=cost_header_cost + cost_code_id.quantity*cost_code_id.unit_price
        self.cost_header_cost = cost_header_cost
