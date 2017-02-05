# -*- coding: utf-8 -*-
from openerp import tools
from openerp.osv import fields, osv
class report_budget_actual_view(osv.osv):
    _name = "report.budget.actual.view"
    _description = "Budget V/s Actual"
    _auto = False
    _rec_name = 'analytic_id'
    _columns = {
        'analytic_id': fields.many2one('account.analytic.account','Analytic',readonly=True),
        'actual': fields.float('Actual',readonly=True),
        'boq_budget': fields.float('BOQ Budget',readonly=True),
        'acc_budget': fields.float('Acc Budget',readonly=True),
        'boq_bud_bal': fields.float('BOQ Budget Balance',readonly=True),
        'acc_bud_bal': fields.float('Acc Budget Balance',readonly=True),
    }

    def init(self,cr):
        tools.drop_view_if_exists(cr, 'report_budget_actual_view')
        cr.execute("""create or replace view report_budget_actual_view as(
SELECT
        ROW_NUMBER () OVER (ORDER BY account_analytic_account.id ) AS id,
        account_analytic_account.id as analytic_id,
        COALESCE(SUM(contracting_budget_line.budget_amount),0) AS boq_budget,
        COALESCE(SUM(crossovered_budget_lines.planned_amount),0) AS acc_budget, 
        COALESCE(ABS(SUM(account_move_line.debit-account_move_line.credit)),0) AS actual,
        COALESCE(SUM(contracting_budget_line.budget_amount)-ABS(SUM(account_move_line.debit-account_move_line.credit)),0) AS boq_bud_bal,
        COALESCE(SUM(crossovered_budget_lines.planned_amount)-ABS(SUM(account_move_line.debit-account_move_line.credit)),0) AS acc_bud_bal
FROM
        account_analytic_account
LEFT JOIN crossovered_budget_lines ON account_analytic_account."id" = crossovered_budget_lines.analytic_account_id
LEFT JOIN contracting_budget_line ON account_analytic_account."id" = contracting_budget_line.account_analytic_id
LEFT JOIN account_move_line ON account_analytic_account."id" = account_move_line.analytic_account_id
GROUP BY account_analytic_account.id


)""")

        

##    def init(self, cr):
##        tools.drop_view_if_exists(cr, 'od_contracting_budget_line_bom_view')
##        cr.execute("""create or replace view od_contracting_budget_line_bom_view as
##(

##SELECT
##    ROW_NUMBER () OVER (ORDER BY
##       "bom".id
##     ) AS ID,
##budget_line.bom_id AS bom_id,
##budget_line.product_id AS cc_product_id,
##budget_line.qty AS cc_qty,
##"bom".product_id AS product_id,
##"bom".product_qty AS product_qty,
##"bom".product_uom AS uom_id
##FROM
##"public".od_contracting_budget_line AS budget_line
##LEFT OUTER JOIN "public".mrp_bom AS "bom" ON budget_line.bom_id = "bom".bom_id 



##)""")
