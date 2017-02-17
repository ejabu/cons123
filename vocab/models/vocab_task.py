# -*- coding: utf-8 -*-

from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields
from openerp.exceptions import except_orm, Warning, RedirectWarning

class vocab_task(models.Model):

    _name = 'vocab.task'
    _inherit = ['mail.thread']
    _description = 'Assigned Task for Student'

    quiz_id=fields.Many2one('vocab.quiz', 'Related Quiz')
    era_id=fields.Many2one('mahad.era', 'Era', compute='_fetch_era', store=True)
    student_id=fields.Many2one('mahad.student', 'Name')
    done_aging = fields.Integer(string='Done Aging', track_visibility='always',)
    test_taken = fields.Integer(string='Test Taken', track_visibility='always',)
    due_date=fields.Date(string='Due Date')
    avg_score = fields.Integer(string='Average Score %', compute='_compute_avg_score', store=False)
    score = fields.Integer(string='Score %', track_visibility='always',)
    top_score = fields.Integer(string='Top Score %', track_visibility='onchange',)
    remark=fields.Char(string='Remark')
    display_name=fields.Char(string='Name', compute='_compute_display_name',)
    state=fields.Selection([('open', 'Open'), ('done', 'Done')], string='Status')

    @api.one
    @api.depends('student_id.name', 'quiz_id.name')
    def _compute_display_name(self):
        names = [self.student_id.name, self.quiz_id.name]
        self.display_name = ' / '.join(filter(None, names))

    @api.one
    @api.depends('quiz_id.average_score')
    def _compute_avg_score(self):
        self.avg_score = self.quiz_id.average_score

    @api.one
    @api.depends('student_id.era_id')
    def _fetch_era(self):
        self.era_id = self.student_id.era_id


    _defaults = {
        'state': 'open',
        'test_taken': 0,
    }

    def unlink(self, cr, uid, ids, context=None):
        for task in self.browse(cr, uid, ids, context=context):
            if task.state =="done":
                raise except_orm('Action Aborted','You cannot delete a complete task. Please repeat your changes after pressing Discard Button')
        return super(vocab_task, self).unlink(cr, uid, ids, context=context)


    def take_quiz(self, cr, uid, ids, context=None):
        import random;
        current_task = self.browse(cr, uid, ids, context=None)
        question_ids = []
        week_covered_ids = set()
        for quiz_line in current_task.quiz_id.line_ids:
            week_id = quiz_line.week_id
            week_covered_ids.add(week_id.id)
            day = quiz_line.day
            frequency = quiz_line.frequency
            vocab_options = week_id.vocab_ids.filtered(lambda r: r.day == day)
            for i in range(0,frequency):
                rand_index = random.randint(1,len(vocab_options))
                chosen_vocab_id = vocab_options[rand_index-1].id
                question_ids.append(chosen_vocab_id)

        week_covered_ids = list(week_covered_ids)
        vocab_covered_ids = self.pool.get('vocab.mean').search(cr, uid, [("week_id","in",week_covered_ids)])
        pass_context = {
            'question_ids' : question_ids,
            'week_covered_ids' : week_covered_ids,
            'vocab_covered_ids' : vocab_covered_ids,
            'question_index' : 1,
            'total_question' : len(question_ids),
            'student_id' : current_task.student_id.id,
            'student_name' : current_task.student_id.nick,
            'quiz_id' : current_task.quiz_id.id,
        }
        dummy, view_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'vocab', 'popup_quiz_form')
        return {
            'name':"Quiz",
            'view_mode': 'form',
            'view_id': view_id,
            'view_type': 'form',
            'res_model': 'popup.quiz',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context':pass_context,
        }
