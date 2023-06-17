# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ClassRoomallocateStudent(models.TransientModel):
    _name = 'classroom.allocate.student'
    _description = 'Allocate students to class room'

    batch_id = fields.Many2one('res.batch', string="Batch")
    student_ids = fields.Many2many('res.partner', string="Student")
    # admission_ids = fields.Many2many('res.admission', string="Admision")
    class_id = fields.Many2one('res.class', string="Class")

    @api.onchange('batch_id')
    def onchange_batch_id(self):
        print('nnnnn', self.batch_id)
        for k in self:
            k.student_ids.write({
                'class_ids': k.ids,

            })
            print(k.student_ids)

        if self.batch_id:
            batch = self.env['res.admission'].search([('batch_id', '=', self.batch_id.id)])
            class_ids = self.env['res.class'].search([('batch_id', '=', self.batch_id.id)])
            student_line_ids = self.env['student.lines'].search([('line_id', 'in', class_ids.ids)])
            student_ids = student_line_ids.mapped('student_id')
            batch_list = []
            for i in batch:
                batch_list.append(i.partner_id.id)
            return {'domain': {'student_ids': [('id', 'in', batch_list), ('id', 'not in', student_ids.ids)]}}

    def action_allocation(self):
        for student in self.student_ids:
            admission= self.env['res.admission'].search([('partner_id','=',student.id),('batch_id', '=',self.batch_id.id)])
            for k in admission:
                x=self.env['student.lines'].create({
                    'student_id': student.id,
                    'line_id': self.class_id.id,
                    'batch_id': self.batch_id.id,
                    'ad_id': k.id,
                    # 'pending_fee': self.pending_fee
                    })
                x.onchange_ad_id()
            # x.update({
            #
            # })
