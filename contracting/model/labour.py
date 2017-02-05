from openerp import models, fields, api, _
from openerp.osv import osv
from openerp.tools.translate import _
def simply(l):
    result = []
    for item in l :
        check = False
        # check item, is it exist in result yet (r_item)
        for r_item in result :
            if item['user_id'] == r_item['user_id'] and item['project_id'] == r_item['project_id'] :
                # if found, add all key to r_item ( previous record)
                check = True
                duration = r_item['duration'] + item['duration']
                amount = r_item['amount'] + item['amount']
                r_item['duration'] = duration
                r_item['amount'] = amount
        if check == False :
            # if not found, add item to result (new record)
            result.append( item )

    return result

class hr_contract(models.Model):
    _inherit = 'hr.contract'
    active = fields.Boolean('Active')

class labour(models.Model):
    _name = 'labour'
    name = fields.Char(string='Title', required=True,readonly=True, states={'draft': [('readonly', False)]})
    date = fields.Date(required=True,readonly=True, states={'draft': [('readonly', False)]},string='Entry Date')
    date_from = fields.Date(reuired=True,states={'draft': [('readonly', False)]},string='Date From',required=True)
    date_to = fields.Date(reuired=True,states={'draft': [('readonly', False)]},string='Date To',required=True)
    rate = fields.Selection([('overhead','Overhead Rate'),('actual','Actual Rate')],default='actual',string='State',required=True)
    wip_account_id = fields.Many2one('account.account','WIP Account',required=True,readonly=True, states={'draft': [('readonly', False)]})
    working_hour = fields.Float(string='Total W.hours',help="Total Working Hour in a month multiplied by working hour in a day ex (25*8 =200)",required=True)
    journal_id = fields.Many2one('account.journal','Journal',required=True,readonly=True,states={'draft': [('readonly', False)]})
    expense_account_id = fields.Many2one('account.account','Provision Account',required=True,readonly=True,states={'draft': [('readonly', False)]})
    move = fields.Many2one('account.move','Journal Entry',readonly=True)
    state = fields.Selection([('draft','Draft'),('done','Done')],default='draft',string='State')
    actual = fields.Boolean('Actual',readonly=True,states={'draft': [('readonly', False)]})
    labour_line = fields.One2many('labour.line','cost_id')
    @api.one
    def unlink(self):
        #add your code here
        if self.state != 'draft':
            raise osv.except_osv(_('User Error!'), _('You can only delete draft Labour Cost'))
        return super(labour, self).unlink()

    @api.one
    def create_move(self):
        # period_obj = self.env['account.period']
        move_obj = self.env['account.move']
        date = self.date
        # period_ids = period_obj.find(date).id
        ref = self.name
        journal_id = self.journal_id and self.journal_id.id
        debit_account = self.wip_account_id.id
        credit_account = self.expense_account_id.id
        actual = self.actual
        move_lines =[]
        
        for line in self.labour_line:
            partner_id = line.partner_id.id
            amount = line.amount
            if actual:
                amount = line.actual_amount
            vals1={
                'name': ref,
                'ref': ref,
                # 'period_id': period_ids ,
                'journal_id': journal_id,
                'date': date,
                'account_id': credit_account,
                'debit': 0.0,
                'credit': abs(amount),
                'partner_id': partner_id,
                'analytic_account_id': line.project_id.id,
              
            }
            vals2={
                'name': ref,
                'ref': ref,
                # 'period_id': period_ids ,
                'journal_id': journal_id,
                'date': date,
                'account_id': debit_account,
                'credit': 0.0,
                'debit': abs(amount),
                'partner_id': partner_id,
                'analytic_account_id': line.project_id.id,
              
            }
            move_lines.append([0,0,vals1])
            move_lines.append([0,0,vals2])
            line.state = 'done'
        move_vals = {
               
                'date': date,
                'ref': ref,
                # 'period_id': period_ids ,
                'journal_id': journal_id,
                'line_ids':move_lines

                } 
        move_id = move_obj.create(move_vals).id
        self.move = move_id
        self.state = 'done'
        return True
           

            
    @api.one
    def get_timesheet(self):
        employee_obj = self.env['hr.employee']
        contract_obj = self.env['hr.contract']
        labour_cost_line = self.env['labour.line']
        timesheet = self.env['account.analytic.line']
        working_hour = self.working_hour
        actual = self.actual
        date_from = self.date_from
        date_to = self.date_to
        t_ids  = timesheet.search([('date','>=',date_from), ('date','<=',date_to)])
        labour_cost_line.search([('cost_id', '=',self.ids[0])]).unlink()
        res = []
        for data in t_ids:
            employee_id =  employee_obj.search([('user_id','=',data.user_id.id)])
            contract_id = contract_obj.search([('employee_id','=',employee_id.id),('active','=',True)]) 
#            total_wage = contract_id.xo_total_wage
            if not contract_id:
                raise osv.except_osv(_('Config Warning!'), _('No contract is found'))
            contract_id = contract_id[0]

            total_wage = contract_id.wage
            partner_id = employee_id.address_home_id and employee_id.address_home_id.id
            if working_hour:
                unit_salary = total_wage/working_hour
            else:
                unit_salary = 0.0
            if not partner_id:
                partner_id = data.user_id and data.user_id.partner_id and data.user_id.partner_id.id
            vals = {
                    'cost_id':self.ids[0],
                    'project_id':data.account_id.id,
                    'user_id':data.user_id.id,
                    'partner_id': partner_id,
                    'duration':data.unit_amount,
                    'amount':abs(data.amount),
                    'actual_amount': abs(unit_salary * data.unit_amount)
                 }
            res.append(vals)
        result = simply(res)
        for vals in result:
            labour_cost_line.create(vals)
        
        return True
class labour_line(models.Model):
    _name = 'labour.line'
    cost_id = fields.Many2one('labour',string='Labour Cost')
    date = fields.Date()
    project_id = fields.Many2one('account.analytic.account','Project/Contract')
    user_id = fields.Many2one('res.users','User')
    partner_id = fields.Many2one('res.partner','Partner')
    duration = fields.Float(string='Duration')
    amount = fields.Float(string="Overhead")
    actual_amount = fields.Float(string='Actual Amount')
    move_id = fields.Many2one('account.move','Journal Voucher',readonly=True)
    state = fields.Selection([('draft','Draft'),('done','Done')],default='draft',string='State')
    journal_id = fields.Many2one('account.journal',string="Journal",related='cost_id.journal_id',store=True)

    @api.one
    def unlink(self):
        if self.state == 'done':
            raise osv.except_osv(_('User Error!'), _('You can only delete draft Cost Line'))
        return super(labour_line, self).unlink()
