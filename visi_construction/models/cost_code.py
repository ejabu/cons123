# -*- coding: utf-8 -*-

from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields

class cost_code(models.Model):

    _name= "cost.code"

    code = fields.Char(string='Code')
    name = fields.Char(string='Name')
    unit_price = fields.Float(string='Unit Price')
    quantity = fields.Float(string='Quantity')
    cost_header = fields.Many2many('cost.header', 'cost_code_to_header_rel', 'code_id', 'header_id', string="Cost Header")