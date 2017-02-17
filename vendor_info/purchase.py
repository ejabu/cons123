from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields

class res_partner_vendor_info(models.Model):
    _inherit = 'res.partner'

    kesesuaian = fields.Selection([('A', 'A'),('B', 'B'),('C', 'C'),], string="Kesesuaian")
    ketepatan = fields.Selection([('A', 'A'),('B', 'B'),('C', 'C'),], string="Ketepatan")
    komunikasi = fields.Selection([('A', 'A'),('B', 'B'),('C', 'C'),], string="Komunikasi")
    terms_of_payment = fields.Selection([('A', 'A'),('B', 'B'),('C', 'C'),], string="Terms of Payment")
