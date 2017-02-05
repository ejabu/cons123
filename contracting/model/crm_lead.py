# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning

class crm_lead(models.Model):
    _inherit = 'crm.lead'

    def view_tender(self,cr,uid,ids,context=None):
        res = {
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'res_model': 'contracting.enquiry',
            'domain': [('lead_id', '=',ids[0])],
            'context':{'default_lead_id':ids[0]}
        }
        return res
