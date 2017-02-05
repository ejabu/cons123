# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from datetime import datetime
class asset_timesheet_inv_wizard(models.TransientModel):
    _name = "asset.timesheet.inv.wizard"
    _description = "Asset Invoice"
    
    # period_id = fields.Many2one('account.period',domain=[('state', '!=', 'done')],string='Period',required=True)
    journal_id = fields.Many2one('account.journal',string='Journal',required=True) 
    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")

    @api.multi
    def generate_entries(self):
        self.env['asset.timesheet'].create_entries(self.journal_id,self.date_from,self.date_to)
        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
