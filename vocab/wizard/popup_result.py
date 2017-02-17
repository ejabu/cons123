# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class popup_result(osv.osv_memory):

    _name = 'popup.result'
    _columns = {
        'name': fields.char(string='Correct Answer'),
    }
    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context={}, toolbar=False):
        result = super(popup_result, self).fields_view_get(cr, uid, view_id, view_type, context=context, toolbar=toolbar)
        vocab_task_doc = self.pool.get('vocab.task').browse(cr, uid, context['active_id'], context=None)
        final_score = context['final_score']
        if final_score<10:
            final_score= 10
        test_taken = vocab_task_doc.test_taken + 1
        if vocab_task_doc.quiz_id.due_date != False:
            import datetime
            diff = datetime.datetime.today() - datetime.datetime.strptime(vocab_task_doc.quiz_id.due_date,"%Y-%m-%d")
            self.pool.get('vocab.task').write(cr, uid, context['active_id'], {'state':'done', 'done_aging': diff.days, 'test_taken':test_taken, 'score': final_score} )

        else:
            self.pool.get('vocab.task').write(cr, uid, context['active_id'], {'state':'done', 'test_taken':test_taken, 'score': final_score} )
        if vocab_task_doc.top_score < final_score:
            self.pool.get('vocab.task').write(cr, uid, context['active_id'], {'top_score': final_score} )


        view_arch = result['arch']
        view_arch = view_arch.replace('SELAMAT','Congrats you have Done this , your score is  ' + str(final_score))
        result['arch']= view_arch
        return result

    def complete(self, cr, uid, ids, context=None):
        return
