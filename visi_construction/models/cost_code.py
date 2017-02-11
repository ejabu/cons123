# -*- coding: utf-8 -*-

from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields

class visi_cost_code(models.Model):

    _inherit= "cost.code"

    unit_price = fields.Float(string='Unit Price', required=True)
    quantity = fields.Float(string='Quantity', required=True)
    cost_header = fields.Many2many('cost.header', 'cost_code_to_header_rel', 'code_id', 'header_id', string="Cost Header")
