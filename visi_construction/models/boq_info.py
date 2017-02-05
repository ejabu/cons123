# -*- coding: utf-8 -*-

from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields

class boq_info(models.Model):

    _name= "boq.info"

    project = fields.Many2one('project.project', 'Project', required=True)
    material_cost = fields.Float(string='Material Cost')
    subcontract_cost = fields.Float(string='Subcontract Cost')
    labor_cost = fields.Float(string='Labor Cost')
    equipment_cost = fields.Float(string='Equipment Cost')
    wk_package_cost = fields.Float(string='Work Package Cost')
    estimated_cost = fields.Float(string='Estimated Cost')
    markup_cost = fields.Float(string='Markup Cost(in %)')
    revision = fields.Integer(string='Revision')

    line_ids = fields.One2many('boq.info.line', 'boq_id', 'Boq Line')
    display_name = fields.Char(string='Name', compute='_compute_display_name')

    @api.depends('project.name')
    def _compute_display_name(self):
        names = self.project.name
        self.display_name = names
