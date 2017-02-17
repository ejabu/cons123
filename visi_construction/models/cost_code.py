# -*- coding: utf-8 -*-

from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields

class visi_cost_code(models.Model):

    _inherit= "cost.code"

    unit_price = fields.Float(string='Unit Price', required=True)
    quantity = fields.Float(string='Quantity', required=True)
    cost_header = fields.Many2many('cost.header', 'cost_code_to_header_rel', 'code_id', 'header_id', string="Cost Header")
    # display_name = fields.Char(string='Name', compute='_compute_display_name')
    #
    #
    # @api.depends('code')
    # def _compute_display_name(self):
    #     import ipdb; ipdb.set_trace()
    #     self.display_name = self.code

    # @api.one
    # def name_get(self):
    #     return (self.id, self.code)
    # def name_search(name='', args=None, operator='ilike', limit=100)


    @api.multi
    def name_get(self):
        if not len(self.ids):
            return []
        resuhh = []
        product_name = []
        for record in self:
            s = resuhh.append((record.id, record.code))
        return resuhh

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search((args + ['|', ('code', 'ilike', name), ('name', 'ilike', name)]),
                               limit=limit)
        if not recs:
            recs = self.search([('name', operator, name)] + args, limit=limit)
        return recs.name_get()
