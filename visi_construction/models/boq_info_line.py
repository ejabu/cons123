# -*- coding: utf-8 -*-

from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields

class boq_info_line(models.Model):

    _name= "boq.info.line"


    boq_id = fields.Many2one('boq.info', 'Related Boq')
    # ref = fields.Integer(string='Key')
    ref = fields.Reference(selection='_reference_models', string="Key")
    type = fields.Char(string='Type')
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

    @api.onchange('quantity','unit_rate')
    # @api.depends("ref")
    def calculate_total(self):
        self.total = self.quantity * self.unit_rate

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
                self.type = 'Asset'
                self.desc = self.ref.name
                self.unit = ""
                self.quantity = 1
                self.unit_rate = 0
                self.total = 0
            elif chosen_object == 'hr.employee':
                self.is_employee = True
                self.type = 'Labor'
                self.desc = self.ref.name
                self.unit = ""
                self.quantity = 1
                self.total = 0
            elif chosen_object == 'product.product':
                self.is_product = True
                self.type = 'Material'
                self.desc = self.ref.name
                self.unit = self.ref.uom_id.name
                self.quantity = 1
                self.unit_rate = self.ref.standard_price
                self.total = 0
            elif chosen_object == 'product.template':
                self.is_subcontract = True
                self.type = 'Subcontract'
                self.desc = self.ref.name
                self.unit = self.ref.uom_id.name
                self.quantity = 1
                self.unit_rate = self.ref.standard_price
                self.total = 0
            elif chosen_object == 'work.package':
                self.is_work_package = True
                self.type = 'Work Package'
                self.desc = self.ref.name
                self.unit = ""
                self.quantity = 1
                self.unit_rate = self.ref.work_package_cost
            else :
                pass

    @api.model
    def _reference_models(self):
        selection = [('account.asset.asset', 'Equipment'),
                    ('hr.employee', 'Labor'),
                    ('product.product', 'Material'),
                    ('product.template', 'Subcontract'),
                    ('work.package', 'Work Package'),]
        return selection
