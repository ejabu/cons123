# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class popup_quiz(osv.osv_memory):

    _name = 'popup.quiz'
    _columns = {
        'question_index': fields.char(string='Question Index'),
        'correct': fields.char(string='Correct Answer'),
    }
    def default_get(self, cr, uid, fields, context=None):
        res = super(popup_quiz, self).default_get(cr, uid, fields, context=context)
        res.update({'question_index':context['question_index']})
        return res

    def take_quiz(self, cr, uid, ids, context=None):
        dummy, view_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'vocab', 'popup_quiz_form') #in model name replace . with _ Example sale.order become sale_order
        return {
            'name':"Quiz",
            'view_mode': 'form',
            'view_id': view_id,
            'view_type': 'form',
            'res_model': 'popup.quiz',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'nodestroy': False,
        }
    def answer_quiz(self, cr, uid, ids, context=None):
        question_index = self.browse(cr,uid, ids, context).question_index
        dummy, view_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'vocab', 'popup_quiz_form')
        answer_index=int(context['answer_index'])
        question_index=int(context['question_index'])

        context['question_index']=int(context['question_index']) + 1
        if 'evaluation' not in context:
            context['evaluation']=[]
        if question_index+1 > context['total_question']:
            print "question_index > total_question"
            if answer_index == context['question_ids'][question_index - 1]:
                context['evaluation'].append("1")
            else:
                context['evaluation'].append("0")
            import collections
            final_score = collections.Counter(context['evaluation'])['1'] * 100 / context['total_question']
            context['final_score']=final_score
            dummy, view_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'vocab', 'popup_result_form')
            return {
                'name':"Congratulations, Task Completed!",
                'view_mode': 'form',
                'view_id': view_id,
                'view_type': 'form',
                'res_model': 'popup.result',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'context': context,
            }
        if answer_index == context['question_ids'][question_index - 1]:
            context['evaluation'].append("1")
            return {
                'name':"Quiz",
                'view_mode': 'form',
                'view_id': view_id,
                'view_type': 'form',
                'res_model': 'popup.quiz',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'context': context,
            }
        else:
            context['evaluation'].append("0")
            return {
                'name':"Quiz",
                'view_mode': 'form',
                'view_id': view_id,
                'view_type': 'form',
                'res_model': 'popup.quiz',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'context': context,
            }

    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context={}, toolbar=False):
        try:
            import random
            result = super(popup_quiz, self).fields_view_get(cr, uid, view_id, view_type, context=context, toolbar=toolbar)

            week_covered_ids = context["week_covered_ids"]
            vocab_covered_ids = context["vocab_covered_ids"]
            removed_vocab_covered_ids = context["vocab_covered_ids"]
            question_ids = context["question_ids"]
            question_index = context["question_index"]
            total_question = context["total_question"]
            question_to_ask = question_ids[question_index-1]
            removed_vocab_covered_ids.remove(question_to_ask)
            random.shuffle(removed_vocab_covered_ids)
            false_option = removed_vocab_covered_ids[:3]

            false_option.append(question_to_ask)
            mixed_options = false_option
            random.shuffle(mixed_options)


            lang_index = random.randint(0,1)
            question_lang = ['english','arabic'][lang_index]
            answer_lang = ['english','arabic'][0 if lang_index == 1 else 1]

            vocab_mean_obj = self.pool.get('vocab.mean')
            view_arch = result['arch']
            vocab_mean_doc = vocab_mean_obj.browse(cr,uid, question_to_ask, context=None)
            view_arch = view_arch.replace('SOALSOAL', vocab_mean_doc[str(question_lang)])
            view_arch = view_arch.replace('question_center','question_center ' + question_lang)
            for option in range(0,4):
                vocab_mean_doc = vocab_mean_obj.browse(cr,uid, mixed_options[option], context=None)
                context_to_append = '''" context="{'answer_index':'ANSWER_INDEX'} '''
                context_to_append = context_to_append.replace('ANSWER_INDEX', str(mixed_options[option]))
                view_arch = view_arch.replace(['Option A','Option B','Option C','Option D'][option],vocab_mean_doc[answer_lang]+context_to_append)

            result['arch']= view_arch
            view_arch = view_arch.replace('quiz_button','quiz_button ' + question_lang)

            return result

            pass
        except Exception as e:
            raise
