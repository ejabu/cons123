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

    @api.one
    def write(self, vals):
        # vals['material_cost']=9999
        res = super(boq_info, self).write(vals)
        if 'line_ids' in vals:
            #only if line_ids has changed
            new_vals={}
            material_cost = 0.0
            subcontract_cost = 0.0
            labor_cost = 0.0
            equipment_cost = 0.0
            wk_package_cost = 0.0
            for line in self.line_ids:
                if line.is_product == True:
                    material_cost += line.total
                elif line.is_subcontract == True:
                    subcontract_cost += line.total
                elif line.is_employee == True:
                    labor_cost += line.total
                elif line.is_asset == True:
                    equipment_cost += line.total
                elif line.is_work_package == True:
                    wk_package_cost += line.total

            estimated_cost = material_cost + subcontract_cost + labor_cost + equipment_cost + wk_package_cost
            new_vals['material_cost']=material_cost
            new_vals['subcontract_cost']=subcontract_cost
            new_vals['labor_cost']=labor_cost
            new_vals['equipment_cost']=equipment_cost
            new_vals['wk_package_cost']=wk_package_cost
            new_vals['estimated_cost']=estimated_cost
            res = super(boq_info, self).write(new_vals)
            # import ipdb; ipdb.set_trace()
        return res

    @api.model
    def create(self, vals):
        def merge_two_dicts(x, y):
            """Given two dicts, merge them into a new dict as a shallow copy."""
            z = x.copy()
            z.update(y)
            return z
        if 'line_ids' in vals:
            new_vals={}
            material_cost = 0.0
            subcontract_cost = 0.0
            labor_cost = 0.0
            equipment_cost = 0.0
            wk_package_cost = 0.0
            for line in vals['line_ids']:
                line = line[2]
                if line['is_product'] == True:
                    material_cost += line['total']
                elif line['is_subcontract'] == True:
                    subcontract_cost += line['total']
                elif line['is_employee'] == True:
                    labor_cost += line['total']
                elif line['is_asset'] == True:
                    equipment_cost += line['total']
                elif line['is_work_package'] == True:
                    wk_package_cost += line['total']

            estimated_cost = material_cost + subcontract_cost + labor_cost + equipment_cost + wk_package_cost
            new_vals['material_cost']=material_cost
            new_vals['subcontract_cost']=subcontract_cost
            new_vals['labor_cost']=labor_cost
            new_vals['equipment_cost']=equipment_cost
            new_vals['wk_package_cost']=wk_package_cost
            new_vals['estimated_cost']=estimated_cost
            res_vals = merge_two_dicts(vals, new_vals)
            res = super(boq_info, self).create(res_vals)
        return res
