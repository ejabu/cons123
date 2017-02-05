# -*- coding: utf-8 -*-

from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields

class project_project(models.Model):

    _inherit= "project.project"

    markup_amt=fields.Char(string='markup_amt')
    estimated_cost=fields.Char(string='estimated_cost')
    planned_hours=fields.Char(string='planned_hours')
    effective_hours=fields.Char(string='effective_hours')
    total_hours=fields.Char(string='total_hours')
    sale_ids=fields.Char(string='sale_ids')
    purchase_ids=fields.Char(string='purchase_ids')
    project_task_ids=fields.Char(string='project_task_ids')
    product_used_ids=fields.Char(string='product_used_ids')
    type_ids=fields.Char(string='type_ids')
    boq_ids=fields.Char(string='boq_ids')
    product_used_ids=fields.Char(string='product_used_ids')
    
