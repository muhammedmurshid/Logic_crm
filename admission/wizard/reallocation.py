from odoo import models, fields, api


class ReallocateStudent(models.TransientModel):
    _name = 'classroom.reallocate.student'
    _description = 'Reallocate students to classroom'

    student_ids = fields.Many2many('res.partner', string="Student")
    batch_id = fields.Many2one('res.batch', string="Batch")
    class_id = fields.Many2one('res.class', string='From class')
    to_class_id = fields.Many2one('res.class', string='To class', required="1")

    @api.onchange('class_id')
    def onchange_class_id(self):
        print('nnnnn', self.class_id)
        if self.class_id:
            for classes in self.class_id:
                reallocation_list = []
                for allocation in classes.line_ids:
                    reallocation_list.append(allocation.student_id.id)
                    print(reallocation_list)
                return {'domain': {'student_ids': [('id', 'in', reallocation_list)]}}

    def classroom_reallocate_student_action(self):
        move_id = self.to_class_id
        from_id = self.class_id
        for student in self.student_ids:
            move_id.write({
                'line_ids': [(0, 0, {
                    'student_id': student.id
                })]
            })
            from_id = self.class_id
            for student in self.student_ids:
                for x in from_id.line_ids:
                    if x.student_id.id == student.id:
                        x.unlink()
