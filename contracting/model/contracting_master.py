#-*- coding:utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning

class contracting_attachment_type(models.Model):
    _name = 'contracting.attachment.type'
    _description = 'Contracting Attachment Type'
   
    name = fields.Char(string='Name',size=128,required="1")
    code = fields.Char(string='Code',size=10,required="1")
    description = fields.Text(string='Description')

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Code must be unique...!'),
    ]

class contracting_job_type(models.Model):
    _name = 'contracting.job.type'
    _description = 'Contracting Job Type'
   
    name = fields.Char(string='Name',size=128,required="1")
    code = fields.Char(string='Code',size=10,required="1")
    description = fields.Text(string='Description')

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Code must be unique...!'),
    ]

class contracting_enquiry_stage(models.Model):
    _name = 'contracting.enquiry.stage'
    _description = 'Contracting Enquiry Stage'
    _order = 'sequence'

    name = fields.Char(string='Enquiry Stage', required=True, size=64, translate=True)
    description = fields.Text(string='Description')
    sequence = fields.Integer(string='Sequence')
    fold = fields.Boolean(string='Folded in Kanban View',
                               help='This stage is folded in the kanban view when'
                               'there are no records in that stage to display.')


class cost_code(models.Model):
    _name = 'cost.code'
    _description = 'Cost Code'

    name = fields.Char(string='Name', required=True,)
    code = fields.Char(string='Code',size=10,required="1")
    description = fields.Text(string='Description')
   

