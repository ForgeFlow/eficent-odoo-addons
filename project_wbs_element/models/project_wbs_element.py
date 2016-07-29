# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import api, fields, models, _
from openerp.exceptions import UserError


class ProjectWbsElement(models.Model):
    _name = "project.wbs_element"
    _description = "Project WBS Element"
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    code = fields.Char(string='Code')
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    project_id = fields.Many2one(
        comodel_name='project.project',
        string='Project',
        required=True,
        copy=True
    )
    parent_id = fields.Many2one(
        comodel_name='project.wbs_element',
        string='Parent WBS Element',
        required=False,
        copy=True
    )
    child_ids = fields.One2many(
        comodel_name='project.wbs_element',
        inverse_name='parent_id',
        string='Child WBS Elements',
        copy=True
    )
    task_ids = fields.One2many(
        comodel_name='project.task',
        inverse_name='wbs_element_id',
        string='Tasks',
        copy=True
    )
    nbr_tasks = fields.Integer(string='Number of Tasks',
                               compute='_count_tasks')
    nbr_childs = fields.Integer(string='Number of Child WBS Elements',
                                compute='_count_childs')
    nbr_docs = fields.Integer(string='Number of Documents',
                                compute='_count_attached_docs')
    color = fields.Integer(string='Color Index')

    @api.depends('task_ids')
    def _count_tasks(self):
        for record in self:
            record.nbr_tasks = len(record.task_ids)

    @api.depends('child_ids')
    def _count_childs(self):
        for record in self:
            record.nbr_childs = len(record.child_ids)

    def _count_attached_docs(self):
        attachment = self.env['ir.attachment']
        task = self.env['project.task']
        for record in self:
            project_attachments = attachment.search(
                [('res_model', '=', 'project.wbs_element'),
                 ('res_id', '=', record.id)])
            tasks = task.search([('wbs_element_id', '=', record.id)])
            task_attachments = attachment.search(
                [('res_model', '=', 'project.task'),
                 ('res_id', 'in', tasks.ids)])
            record.nbr_docs = \
                (len(project_attachments) or 0) + (len(task_attachments) or 0)

    @api.onchange('parent_id')
    def _onchange_parent_id(self):
        if self.parent_id:
            self.project_id = self.parent_id.project_id

    @api.multi
    @api.constrains('child_ids', 'task_ids')
    def _check_tasks_assigned(self):
        for record in self:
            if record.child_ids and record.task_ids:
                raise UserError(
                    _('A WBS Element that is parent of others cannot have '
                      'tasks assigned.'))

    @api.onchange('project_id')
    def _onchange_project_id(self):
        for record in self.child_ids:
            record.project_id = record.project_id

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            name = record.name
            if record.code:
                name = '[' + record.code + '] ' + name
            res.append((record.id, name))
        return res

    @api.multi
    def attachment_tree_view(self):
        tasks = self.env['project.task'].search([
            ('project_id', 'in', self.ids)])
        domain = [
            '|',
            '&', ('res_model', '=', 'project.wbs_element'), ('res_id', 'in',
                                                           self.ids),
            '&', ('res_model', '=', 'project.task'), ('res_id', 'in',
                                                      tasks.ids)
        ]
        res_id = self.ids and self.ids[0] or False
        return {
            'name': _('Attachments'),
            'domain': domain,
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (
            self._name, res_id)
        }
