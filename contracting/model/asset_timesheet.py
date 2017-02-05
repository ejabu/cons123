# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning

class asset_timesheet(models.Model):
    _name = "asset.timesheet"
    _description = "Asset Timesheet"


    @api.multi
    def unlink(self):
        for sheet in self:
            if sheet.state == 'done':
                raise except_orm(_('Warning!'), _('Posted Timesheet cannot be deleted!'))
        return models.Model.unlink(self)

            

    #Onchange of product will update the cost price(standard_price) from the product master
    @api.onchange('name')
    def on_change_product(self):
        if self.name:
            self.cost = self.name.standard_price or 0.0

    @api.one
    @api.depends('cost','total_time')
    def _compute_total(self):
        self.total_amount = self.cost * self.total_time


    asset_id = fields.Many2one('account.asset.asset',string="Asset",required=True,readonly=True,states={'draft': [('readonly', False)]})
    date_from = fields.Date('From',required=True,readonly=True,states={'draft': [('readonly', False)]})
    date_to = fields.Date('To',required=True,readonly=True,states={'draft': [('readonly', False)]})
    name = fields.Many2one('product.product',string='Usage',required=True,readonly=True,states={'draft': [('readonly', False)]})
    account_analytic_id = fields.Many2one('account.analytic.account',string="Project",required=True,readonly=True,states={'draft': [('readonly', False)]})
    total_time = fields.Float('Hours',required=True,readonly=True,states={'draft': [('readonly', False)]})
    cost = fields.Float('Cost',required=True,readonly=True,states={'draft': [('readonly', False)]})
    total_amount = fields.Float('Total',compute='_compute_total',store=True)
    state = fields.Selection([('draft','Draft'),('done','Done')], string='Status', index=True, readonly=True, default='draft')


    @api.multi
    def create_entries(self,journal,date_from,date_to):
        """ Print the invoice and mark it as sent, so that we can see more
            easily the next step of the workflow
        """
        # date_from = period.date_start
        # date_to = period.date_stop
        # period_id = period and period.id or False
        journal_id = journal and journal.id or False
        
        move_lines = []

        for timesheet in self.search([('date_to','<=',date_to),('date_to','>=',date_from),('state','=','draft')]):
            product = timesheet.name
            debit_acc_id = product and product.property_account_expense and product.property_account_expense.id or product.categ_id and product.categ_id.property_account_expense_categ and product.categ_id.property_account_expense_categ.id or False
            credit_acc_id = timesheet.name and product.property_account_income and product.property_account_income.id or product.categ_id and product.categ_id.property_account_income_categ and product.categ_id.property_account_income_categ.id or False
            analytic_acc_id = timesheet.account_analytic_id and timesheet.account_analytic_id.id or False

            if not debit_acc_id or not credit_acc_id:
                raise except_orm(_('Warning!'), _('Account not set!\nPlease set Income and Expense Accounts in Product'))

            amt = (timesheet.total_time * timesheet.cost) or 0.0
            line_debit={
                'name': 'Asset: '+timesheet.asset_id.name+' ['+product.name+']',
                # 'period_id': period_id,
                
                'date':date_to,
                'journal_id': journal_id,
                'account_id': debit_acc_id,
                'analytic_account_id':analytic_acc_id,
                'credit':0,
                'debit':amt,
            }
            line_credit={
                'name':'Asset: '+timesheet.asset_id.name+' ['+product.name+']',
                # 'period_id': period_id,
                'date':date_to,
                'journal_id': journal_id,
                'account_id': credit_acc_id,
                'analytic_account_id':analytic_acc_id,
                'credit':amt,
                'debit':0,
            }
            timesheet.state='done'
            move_lines.append([0,0,line_debit])
            move_lines.append([0,0,line_credit])


        print "#############",move_lines


        vals={
            'date':date_to,
            'journal_id':journal and journal.id,
            # 'period_id':period and period.id,
            'ref':'Asset Timesheet for '+ date_from + 'To' + date_to,
            'line_id':move_lines

            }

            
        self.env['account.move'].create(vals)            

        return True

        
