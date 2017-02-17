# -*- coding: utf-8 -*-

from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields

class vocab_week(models.Model):

    _name = 'vocab.week'
    _description = 'Form for updating Vocab weekly'

    name=fields.Char(string='Week Name')
    published_date=fields.Date(string='Published Date')
    vocab_ids=fields.One2many('vocab.mean', 'week_id', 'Vocabularies')
    total_vocab = fields.Integer(string='Total Vocabularies', compute='_compute_total_vocab', store=True)

    @api.one
    @api.depends('vocab_ids')
    def _compute_total_vocab(self):
        self.total_vocab = len(self.vocab_ids)

    _defaults = {
        'published_date': Fields.datetime.now,
    }
