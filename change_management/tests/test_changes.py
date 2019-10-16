# Copyright 2017 Matmoz d.o.o. (<http://www.matmoz.si>).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestChanges(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        """***setup change tests***"""
        super(TestChanges, cls).setUpClass()
        cls.change_model = cls.env['change.management.change']
        cls.project_model = cls.env['project.project']
        cls.task_model = cls.env['project.task']
        cls.user_model = cls.env['res.users']
        cls.test_project_id = cls.project_model.create(
            {'name': 'ChangeTestProject'}
        )
        cls.change_owner_id = cls.env.ref('change_management.user_change_user')
        cls.change_second_author_id = cls.change_owner_id.copy()
        cls.change_manager_id = \
            cls.env.ref('change_management.user_change_manager')
        cls.change_partner_manager = cls.env.ref(
            'change_management.partner_change_manager')
        cls.test_change_id = cls.change_model.create({
            'name': 'ChangeTest0001',
            'description': 'TestChange_SkyPaintBlue',
            'change_category_id': 1,
            'project_id': cls.test_project_id.id,
            'author_id': cls.change_owner_id.id,
            'change_owner_id': cls.change_manager_id.id
        })

    def test_change_owner_and_creator_added_to_followers_for_change(self):
        change = self.test_change_id
        followers = [follower.id for follower in change.message_follower_ids]
        self.assertTrue(
            len(followers) == 1,
            msg='Expecting 3 followers - got:%s' % len(followers)
        )

    def test_saving_a_change_in_users_as_followers_works(self):
        self.test_change_id.write(
            {'author_id': self.change_second_author_id.id}
        )
        change = self.test_change_id
        followers = [follower.id for follower in change.message_follower_ids]
        self.assertTrue(
            len(followers) == 2,
            msg='Expecting 4 followers - got:%s' % len(followers)
        )

    def test_adding_a_task_on_a_change(self):
        change = self.test_change_id.read(['message_follower_ids'])
        followers = self.env['mail.followers'].browse(
            change[0]['message_follower_ids'])
        self.test_change_id.write({
            'change_response_ids': [(0, 0,
                                     {'remaining_hours': 0,
                                      'stage_id': 1,
                                      'planned_hours': 0,
                                      'user_id': self.env.uid,
                                      'name': 'My New Task',
                                      'date_deadline': False,
                                      'sequence': 10,
                                      'date_end': False,
                                      'date_start': False,
                                      'company_id': 1,
                                      'message_follower_ids':
                                      [(4, followers.id)],
                                      'project_id': 1,
                                      'partner_id': False,
                                      'message_ids': False,
                                      'description': 'A new Task'})]
        })
        self.assertNotEqual(
            followers,
            self.test_change_id.change_response_ids[0].message_follower_ids,
            msg='Followers are not set on the associated action'
        )
