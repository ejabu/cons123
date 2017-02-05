# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
class stock_picking(osv.osv):
    _inherit = "stock.picking"
    _columns = {
        'analytic_account_id':fields.many2one('account.analytic.account','Analytic Account')
    }

class stock_quant(osv.osv):
    _inherit = "stock.quant"

    def _prepare_account_move_line(self, cr, uid, move, qty, cost, credit_account_id, debit_account_id, context=None):
        """
        Generate the account.move.line values to post to track the stock valuation difference due to the
        processing of the given quant.
        """
        picking_id = move.picking_id and move.picking_id.id
        pick_obj = self.pool.get('stock.picking')
        res = super(stock_quant,self)._prepare_account_move_line(cr, uid, move, qty, cost, credit_account_id, debit_account_id, context=context)
        if picking_id:
            analytic_id = pick_obj.browse(cr,uid,picking_id).analytic_account_id and pick_obj.browse(cr,uid,picking_id).analytic_account_id.id
            if analytic_id:
                for x in res:
                    x[2]['analytic_account_id']=analytic_id
        return res

