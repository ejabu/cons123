# -*- coding: utf-8 -*-

from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields

class cost_header(models.Model):

    _name= "cost.header"

    cost_header_number = fields.Integer(string='Cost Header Number')
    name = fields.Char(string='Cost Header Name')
    cost_header_cost = fields.Float(string='Cost of Header')
    cost_code = fields.Many2many('cost.code', 'cost_code_to_header_rel', 'header_id', 'code_id', string="Cost Code")
