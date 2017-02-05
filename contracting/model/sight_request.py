#-*- coding:utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning

class sight_request(models.Model):
    _name = 'sight.request'
    _description = 'Sight Request'

    def create(self, cr, uid, vals, context=None):
        if vals.get('name','/')=='/':
            if vals.get('request_type') == 'material':
                name = self.pool.get('ir.sequence').get(cr, uid, 'sight.material.request') or '/'
            elif vals.get('request_type') == 'labour':
                name = self.pool.get('ir.sequence').get(cr, uid, 'sight.labour.request') or '/'
            elif vals.get('request_type') == 'asset':
                name = self.pool.get('ir.sequence').get(cr, uid, 'sight.asset.request') or '/'
            
            vals['name'] = name
        return super(sight_request, self).create(cr, uid, vals, context=context)

    @api.onchange('date')
    def onchange_date(self):
        self.requested_date = self.date



    name = fields.Char(string='Name', default='/', required=True)
    date = fields.Date(string='Date', required=True,default=fields.Datetime.now() )
    project_id = fields.Many2one('account.analytic.account',string="Project",required=True)
    requested_date = fields.Date(string='Requested Date')
    requested_user_id = fields.Many2one('res.users',string="Requested By",default=lambda self: self.env.user)
    material_lines = fields.One2many('sight.material.request.line','request_id',string='Material')
    labour_lines = fields.One2many('sight.labour.request.line','request_id',string='Labour')
    asset_lines = fields.One2many('sight.asset.request.line','request_id',string='Asset')
    request_type = fields.Selection([            ('material','Material'),
            ('labour','Labour'),
            ('asset','Asset')],string="Request Type",required=True)
    state = fields.Selection([
            ('draft','Draft'),
            ('submitted','Submitted'),
            ('approved','Approved'),
            ('cancel','Cancelled'),
            ('done','Done'),

        ], string='Status', index=True,default='draft', readonly=True)

class sight_material_request_line(models.Model):
    _name = 'sight.material.request.line'
    _description = 'Material Request'


    @api.onchange('product_id')
    def onchange_prodcut_id(self):
        self.name = self.product_id.name

    request_id = fields.Many2one('sight.request','Request',ondelete='cascade')
    name = fields.Char('Description', required=True)
    cost_code_id = fields.Many2one('cost.code',string="Cost Code",required=True)
    partner_id = fields.Many2one('res.partner',string='Partner')
    bom_id = fields.Many2one('mrp.bom',string = 'BOM')
    product_id = fields.Many2one('product.product',string='Product',required=True)
    
    qty = fields.Float('Qty')


class sight_labour_request_line(models.Model):
    _name = 'sight.labour.request.line'
    _description = 'Labour Request'


    @api.onchange('product_id')
    def onchange_prodcut_id(self):
        self.name = self.product_id.name

    request_id = fields.Many2one('sight.request','Request',ondelete='cascade')
    name = fields.Char('Description', required=True)
    cost_code_id = fields.Many2one('cost.code',string="Cost Code",required=True)
    partner_id = fields.Many2one('res.partner',string='Partner')
    product_id = fields.Many2one('product.product',string='Product',required=True)
    
    qty = fields.Float('Qty')

class sight_asset_request_line(models.Model):
    _name = 'sight.asset.request.line'
    _description = 'Asset Request'


    @api.onchange('product_id')
    def onchange_prodcut_id(self):
        self.name = self.product_id.name

    request_id = fields.Many2one('sight.request','Request',ondelete='cascade')
    name = fields.Char('Description', required=True)
    cost_code_id = fields.Many2one('cost.code',string="Cost Code",required=True)
    partner_id = fields.Many2one('res.partner',string='Partner')
    asset_id = fields.Many2one('account.asset.asset',string='Asset')
    product_id = fields.Many2one('product.product',string='Product',required=True)
    qty = fields.Float('Qty')


