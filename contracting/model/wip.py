from openerp import models, fields, api, _
from openerp.osv import osv
from openerp.tools.translate import _
class wip(models.Model):
    _name = 'wip'
    name = fields.Char(string='Title', required=True,readonly=True, states={'draft': [('readonly', False)]})
    date = fields.Date(required=True,readonly=True, states={'draft': [('readonly', False)]})
    project_id = fields.Many2one('account.analytic.account','Project/Contract',required=True,readonly=True, states={'draft': [('readonly', False)]})
    wip_account_balance = fields.Float(string='WIP Balance',required=True,readonly=True, states={'draft': [('readonly', False)]})
    wip_account_id = fields.Many2one('account.account','WIP Account',required=True,readonly=True, states={'draft': [('readonly', False)]})
    invoice_amount = fields.Float(string="Invoice Amount",readonly=True,states={'draft': [('readonly', False)]},copy=False)
    provision_account_id = fields.Many2one('account.account','Provision Account',readonly=True, states={'draft': [('readonly', False)]})
    journal_id = fields.Many2one('account.journal','Journal',required=True,readonly=True,states={'draft': [('readonly', False)]})
    expense_account_id = fields.Many2one('account.account','Expense Account',required=True,readonly=True,states={'draft': [('readonly', False)]})
    provision_percentage = fields.Float('Provision %',readonly=True, states={'draft': [('readonly', False)]},copy=False)
    provision_amount = fields.Float(string='Provision Amount',readonly=True, states={'draft': [('readonly', False)]},copy=False)
    project_cost = fields.Float(string="Project Cost",readonly=True,states={'draft': [('readonly', False)]},copy=False)
    invoice_account_id  = fields.Many2one('account.account','Invoice Account',required=True,readonly=True,states={'draft': [('readonly', False)]})
    income_account_id = fields.Many2one('account.account','Income Account',required=True,readonly=True,states={'draft': [('readonly', False)]})
    move = fields.Many2one('account.move','Journal Entry',readonly=True,copy=False)
    state = fields.Selection([('draft','Draft'),('done','Done')],default='draft',string='State')
    provision = fields.Boolean('Provision',readonly=True,states={'draft': [('readonly', False)]},copy=False)
    profit = fields.Float(string='Profit',compute='get_profit',store=True)
    
    @api.one
    @api.depends('invoice_amount','project_cost')
    def get_profit(self):
        self.profit = self.invoice_amount - self.project_cost
    @api.one
    def unlink(self):
        if self.state != 'draft':
            raise osv.except_osv(_('User Error!'), _('You can only delete draft Wip'))
        return super(wip, self).unlink()

    
    def onchange_analytic_account(self,cr,uid,ids,analytic_acc_id,wip_acc_id,invoice_account_id,context=None):
        invoice_amount=0.0
        wip_balance = 0.0
        if analytic_acc_id and wip_acc_id and invoice_account_id:
            query_param1 = (wip_acc_id,analytic_acc_id,)
            query_param2 = (invoice_account_id,analytic_acc_id,)
            # analytic_acc_ids=self.pool.get('account.analytic.account').search(cr,uid,[('id','child_of',analytic_acc_id)])
            #WIP
            query1 = ("select sum(debit) - sum(credit) from account_move_line mvl left join account_move mv on mvl.move_id = mv.id  where account_id =%s and analytic_account_id = %s and  mv.state = 'posted' "%query_param1)
        #Invoice
            query2 = ("select sum(credit) - sum(debit) from account_move_line mvl left join account_move mv on mvl.move_id = mv.id where account_id =%s and analytic_account_id = %s and mv.state = 'posted' "%query_param2)
            # if len(analytic_acc_ids) > 1:
            #     query_param1 = (wip_acc_id,tuple(analytic_acc_ids),)
            #     query_param2 = (invoice_account_id,tuple(analytic_acc_ids),)
            #WIP
            #     query1 = ("select sum(debit) - sum(credit) from account_move_line where account_id = %s and analytic_account_id in %s and state='valid'"%query_param1)
            # #Invoice
            #     query2 = "select sum(credit) - sum(debit) from account_move_line where account_id = %s and analytic_account_id in %s and state='valid'"%query_param2
            cr.execute(query1)
            wip_balance = cr.fetchone()[0]
            cr.execute(query2)
            invoice_amount = cr.fetchone()[0]
        else:
            invoice_amount =0.0
            wip_balance =0.0
        return {'value':{'invoice_amount':invoice_amount,'wip_account_balance':wip_balance}}

    @api.onchange('wip_account_balance','invoice_amount','provision_percentage')
    def onchange_invoice_amount(self):
        invoice_amount = self.invoice_amount
        wip_amount = self.wip_account_balance
        prov_perc = self.provision_percentage
        self.project_cost = wip_amount + (invoice_amount*prov_perc/100)
        self.provision_amount = invoice_amount*prov_perc/100
    
  
       
    @api.one
    def validate(self):
            date = self.date
            # period_obj = self.env['account.period']
            # period_id = period_obj.find(date).id
            journal_id = self.journal_id and self.journal_id.id
            wip_acc_id = self.wip_account_id and self.wip_account_id.id
            expense_acc_id = self.expense_account_id and self.expense_account_id.id
            inv_acc_id = self.invoice_account_id and self.invoice_account_id.id 
            income_acc_id = self.income_account_id and self.income_account_id.id
            prov_acc_id = self.provision_account_id and self.provision_account_id.id
            analytic_acc_id = self.project_id and self.project_id.id
            wip_balance = self.wip_account_balance
            cost = self.project_cost
            invoice_amount = self.invoice_amount
            provision_amount = self.provision_amount
            name =self.name
            line_name = self.name
            
            l1 = {
                'name': line_name,
                'credit': wip_balance,
                'debit':0.0,
                'account_id': wip_acc_id,
                'analytic_account_id':analytic_acc_id,
                'date':self.date,
            }
            l2 = {
                'name':line_name,
                'debit': cost,
                'credit':0.0 ,
                'account_id': expense_acc_id ,
                'analytic_account_id':analytic_acc_id,
                'date':self.date,
            }
            l4= {
                'name':line_name,
                'debit': invoice_amount,
                'credit':0.0 ,
                'account_id': inv_acc_id ,
                'analytic_account_id':analytic_acc_id,
                'date':self.date,
                 
                 }
            l5= {
                'name':line_name,
                'debit': 0.0,
                'credit':invoice_amount,
                'account_id': income_acc_id,
                'analytic_account_id':analytic_acc_id,
                'date':self.date,
                 
                 }
            if prov_acc_id:
                l3 = {
                    'name':line_name,
                    'credit':provision_amount,
                    'debit':0.0,
                    'account_id':prov_acc_id,
                    'analytic_account_id':analytic_acc_id,
                    'date':self.date
                    }
                line_ids = [(0,0,l1),(0, 0, l2),(0, 0, l3),(0,0,l4),(0,0,l5)]
            else:
                line_ids = [(0,0,l1),(0, 0, l2),(0,0,l4),(0,0,l5)]
            move = self.env['account.move'].create({
                'narration':name,
                'line_id': line_ids,
                'journal_id': journal_id,
                # 'period_id': period_id,
                'date': self.date,
            })
            self.move = move
            self.state = 'done'
            return self.write({})
        
