#-*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning

class product_category(models.Model):
    _inherit = 'product.category'
    status = fields.Selection([('material','Material'),('labour','Labour'),('asset','Asset')],'Type')
