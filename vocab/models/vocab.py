# -*- coding: utf-8 -*-

from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields

class vocab_mean(models.Model):

    _name = 'vocab.mean'
    _description = 'Form for updating Vocab weekly'
    name=fields.Char(string='ID')
    english=fields.Char(string='English', required=True)
    arabic=fields.Char(string='Arabic', required=True)
    published_date=fields.Date(string='Published Date')
    day = fields.Integer(string='Day')
    week_id=fields.Many2one('vocab.week', 'Week', readonly=True)
