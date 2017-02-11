# -*- coding: utf-8 -*-

from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields

class work_package(models.Model):

    _name= "work.package"

    name = fields.Char(string='Work Package Name', required=True)
    work_package_cost = fields.Float(string='Work Package Cost', compute='_compute_cost', store=True)
    cost_header = fields.Many2many('cost.header', 'cost_header_to_work_package_rel', 'package_id', 'header_id', string="Cost Header")

    _defaults = {
        'name'  : 'Work Package'
    }
    @api.one
    @api.depends('cost_header')
    def _compute_cost(self):
        # import ipdb; ipdb.set_trace()
        work_package_cost = 0
        for cost_header_id in self.cost_header:
            work_package_cost=work_package_cost + cost_header_id.cost_header_cost
        self.work_package_cost = work_package_cost
