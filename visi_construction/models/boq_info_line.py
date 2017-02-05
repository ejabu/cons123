# -*- coding: utf-8 -*-

from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields

class boq_info_line(models.Model):

    _name= "boq.info.line"


    boq_id = fields.Many2one('boq.info', 'Related Boq')
    # ref = fields.Integer(string='Key')
    ref = fields.Reference(selection='_reference_models', string="Key")
    type = fields.Integer(string='Type')
    desc = fields.Char(string='Desc')
    unit = fields.Char(string='Unit')
    quantity = fields.Float(string='Qty', required=True)
    unit_rate = fields.Float(string='Rate', required=True)
    total = fields.Float(string='Total')
    is_product = fields.Boolean(string='Is Product')
    is_employee = fields.Boolean(string='Is Employee')
    is_asset = fields.Boolean(string='Is Asset')
    is_subcontract = fields.Boolean(string='Is Subcontract')
    is_work_package = fields.Boolean(string='Is Work Package')


    # def material_id_change(self, cr, uid, ids, ref):
    #     import ipdb; ipdb.set_trace()
    #     return


    @api.onchange('ref')
    # @api.depends("ref")
    def check_change(self):
        if self.ref:
            self.is_asset = False
            self.is_employee = False
            self.is_product = False
            self.is_subcontract = False
            self.is_work_package = False
            chosen_object = self.ref._name
            # import ipdb; ipdb.set_trace()
            if chosen_object == 'account.asset.asset':
                self.is_asset = True
            elif chosen_object == 'hr.employee':
                self.is_employee = True
            elif chosen_object == 'product.product':
                self.is_product = True
            elif chosen_object == 'product.template':
                self.is_subcontract = True
                self.is_product = True
            elif chosen_object == 'work.package':
                self.is_work_package = True
            else :
                pass
    #     #
    #     # if self.field1 < self.field2:
    #     #     self.field3 = True
    @api.model
    def _reference_models(self):
        selection = [('account.asset.asset', 'Equipment'),
                    ('hr.employee', 'Labor'),
                    ('product.product', 'Material'),
                    ('product.template', 'Subcontract'),
                    ('work.package', 'Work Package'),]
        return selection
