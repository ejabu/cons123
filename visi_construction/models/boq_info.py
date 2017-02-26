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
    estimated_cost_before_markup = fields.Float(string='Estimated Cost')
    markup_cost = fields.Float(string='Markup Cost(in %)')
    revision = fields.Integer(string='Revision')
    is_active = fields.Boolean(string='Active')

    line_ids = fields.One2many('boq.info.line', 'boq_id', 'Boq Line', copy=True)
    display_name = fields.Char(string='Name', compute='_compute_display_name')

    _defaults = {
        'is_active'  : True,
    }

    @api.depends('project.name')
    def _compute_display_name(self):
        names = self.project.name
        self.display_name = names

    @api.one
    def write(self, vals):
        res = super(boq_info, self).write(vals)
        if 'line_ids' in vals:
            #only if line_ids has changed
            if 'markup_cost' in vals:
                markup_cost = vals['markup_cost']
            else:
                markup_cost = self.markup_cost
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

            estimated_cost_before_markup = material_cost + subcontract_cost + labor_cost + equipment_cost + wk_package_cost
            estimated_cost = estimated_cost_before_markup * ((markup_cost+100.00)/100.00)
            new_vals['material_cost']=material_cost
            new_vals['subcontract_cost']=subcontract_cost
            new_vals['labor_cost']=labor_cost
            new_vals['equipment_cost']=equipment_cost
            new_vals['wk_package_cost']=wk_package_cost
            new_vals['estimated_cost_before_markup']=estimated_cost_before_markup
            new_vals['estimated_cost']=estimated_cost
            self.project.write({'markup_amt': markup_cost, 'estimated_cost': estimated_cost  })
            res = super(boq_info, self).write(new_vals)
        elif 'markup_cost' in vals:
            new_vals={}
            estimated_cost = self.estimated_cost_before_markup * ((vals['markup_cost']+100.00)/100.00)
            new_vals['estimated_cost']=estimated_cost
            self.project.write({'markup_amt': vals['markup_cost'], 'estimated_cost': estimated_cost  })

            res = super(boq_info, self).write(new_vals)
        return res

    @api.model
    def create(self, vals):
        def merge_two_dicts(x, y):
            """Given two dicts, merge them into a new dict as a shallow copy."""
            z = x.copy()
            z.update(y)
            return z
        if 'line_ids' in vals:
            #only if line_ids has changed
            #markup_cost always in vals
            markup_cost = vals['markup_cost']

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

            estimated_cost_before_markup = material_cost + subcontract_cost + labor_cost + equipment_cost + wk_package_cost
            estimated_cost = estimated_cost_before_markup * ((markup_cost+100.00)/100.00)
            new_vals['material_cost']=material_cost
            new_vals['subcontract_cost']=subcontract_cost
            new_vals['labor_cost']=labor_cost
            new_vals['equipment_cost']=equipment_cost
            new_vals['wk_package_cost']=wk_package_cost
            new_vals['estimated_cost_before_markup']=estimated_cost_before_markup
            new_vals['estimated_cost']=estimated_cost
            import ipdb; ipdb.set_trace()
            self.env['project.project'].browse(vals['project']).write({'markup_amt': markup_cost, 'estimated_cost': estimated_cost  })
            res_vals = merge_two_dicts(vals, new_vals)
            res = super(boq_info, self).create(res_vals)
        return res


    @api.multi
    def create_revision(self):
        data_copy = super(boq_info, self).copy_data()[0]
        data_copy.update({
         'revision': data_copy['revision']+1,
        })
        self.write({'is_active': False})

        res =self.create(data_copy)
        course_form = self.env.ref('visi_construction.boq_info_form', False)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'boq.info',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': res.id,
            'target': 'current',
            'nodestroy': True,
            'views': [(course_form.id, 'form')],
            'view_id': 'course_form.id',
        }
