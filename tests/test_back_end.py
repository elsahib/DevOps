import unittest
import flask_login
import pytest
from flask import abort, url_for
from flask_testing import TestCase
from application import app, db
from application.models import Users, Players, Stats
from os import getenv
from application import login_manager
class TestBase(TestCase):

    def create_app(self):

        # pass in configurations for test database
        config_name = 'testing'
        app.config.update(SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URI3'))
        return app

    def setUp(self):
        """
        Will be called before every test
        """
        # ensure there is no data in the test database when the test starts
        db.session.commit()
        db.drop_all()
        db.create_all()

        # create test admin user
        admin = Users(first_name="admin", last_name="admin", email="admin@admin.com", password="admin2016")

        # create test non-admin user
        employee = Users(first_name="test", last_name="user", email="test@user.com", password="test2016")

        # save users to database
        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()

class TestViews(TestBase):

    def test_homepage_view(self):
        """
        Test that homepage is accessible without login
        """
        response = self.client.get(url_for('home'))
        self.assertEqual(response.status_code, 200)

    def test_loginview(self):
        response = self.client.get(url_for('login'))
        self.assertEqual(response.status_code, 200)

    def test_aboutview(self):
        response = self.client.get(url_for('about'))
        self.assertEqual(response.status_code, 200)
    
    def test_registerview(self):
        response = self.client.get(url_for('register'))
        self.assertEqual(response.status_code, 200)
    

    #test for login required
    def test_account(self):
        response = self.client.get(url_for('account'))
        self.assertEqual(response.status_code, 302)
    def test_addplayer(self):
        response = self.client.get(url_for('addplayer'))
        self.assertEqual(response.status_code, 302)

    def test_vlayers(self):
        response = self.client.get(url_for('vplayers'))
        self.assertEqual(response.status_code, 302)

    def test_addstats(self):
        response = self.client.get(url_for('addstats'))
        self.assertEqual(response.status_code, 302)

    def test_view(self):
        response = self.client.get(url_for('view'))
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        response = self.client.get(url_for('logout'))
        self.assertEqual(response.status_code, 302)

    def test_delete_account(self):
        response = self.client.get(url_for('account_delete'))
        self.assertEqual(response.status_code, 302)

    def test_account(self):
        response = self.client.get(url_for('account'))
        self.assertEqual(response.status_code, 302)

#trying to test login protected pages
    # def test_login(self):
    #     self.client.post('/login', data=dict(
    #     email='admin@admin.com',
    #     password='admin2016'
    #     ), follow_redirects=True)

    #     res = self.client.get("/")

    #     assert "adding" in res.data


# class TestViews2(TestBase):

#     @pytest.fixture
#     def authenticated_request(self):
#         with app.test_request_context():
#             # user = db.session.query(Users).select_from(Users).filter_by(id = 1 ).first()
            
#             yield flask_login.login_user('email', 'admin@admin.com', remember=True)

#     @pytest.mark.usefixtures("authenticated_request")
#     def test_view(self):
#         response = self.client.get(url_for('addplayer'))
#         self.assertEqual(response.status_code, 200)

