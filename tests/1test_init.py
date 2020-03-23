import unittest
import time
from flask import url_for
from urllib.request import urlopen

from os import getenv
from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from application import app, db, bcrypt
from application.models import Users

# Set test variables for test admin user
test_admin_first_name = "admin"
test_admin_last_name = "admin"
test_admin_email = "admin@email.com"
test_admin_password = "admin2020"

# Set player variables
test_player_name = 'player1'
test_player_team = 'team1'
test_player_age = '33'
# Set Stats variables
test_player_goals = '1'
test_player_assists = '20'
test_player_chances = '12'
test_player_shots = '20'
test_player_minutes = '50'
test_player_date = '02-02-2020'

class TestBase(LiveServerTestCase):

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI3')
        app.config['SECRET_KEY'] = getenv('SECRET_KEY')
        return app

    def setUp(self):
        """Setup the test driver and create test users"""
        print("--------------------------NEXT-TEST----------------------------------------------")
        chrome_options = Options()
        chrome_options.binary_location = "/usr/bin/google-chrome"
        #chrome_options.add_argument("--headless") WAY MUCH COOLER WITHOUT THIS :)
        self.driver = webdriver.Chrome(executable_path="/home/student/Documents/DevOps/chromedriver", chrome_options=chrome_options)
        self.driver.get("http://localhost:5000")
        db.session.commit()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        self.driver.quit()
        print("--------------------------END-OF-TEST----------------------------------------------\n\n\n-------------------------UNIT-AND-SELENIUM-TESTS----------------------------------------------")

    def test_server_is_up_and_running(self):
        response = urlopen("http://localhost:5000")
        self.assertEqual(response.code, 200)


class TestRegistration(TestBase):

    def test_zlogin(self):
        #click register menu link
        self.driver.find_element_by_xpath("/html/body/div/header/nav/ul/li[2]/a").click()
        time.sleep(1)

        # Fill in registration form
        self.driver.find_element_by_xpath('//*[@id="email"]').send_keys(test_admin_email)
        self.driver.find_element_by_xpath('//*[@id="first_name"]').send_keys(
            test_admin_first_name)
        self.driver.find_element_by_xpath('//*[@id="last_name"]').send_keys(
            test_admin_last_name)
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(
            test_admin_password)
        self.driver.find_element_by_xpath('//*[@id="confirm_password"]').send_keys(
            test_admin_password)
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        time.sleep(1)

        #click login menu link
        self.driver.find_element_by_xpath("/html/body/div/header/nav/ul/li[3]/a").click()
        time.sleep(1)
        #fill in the login form
        self.driver.find_element_by_xpath('//*[@id="email"]').send_keys(test_admin_email)
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(test_admin_password)
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        time.sleep(1)
        assert url_for('home') in self.driver.current_url    

    def test_registration(self):
        """
        Test that a user can create an account using the registration form
        if all fields are filled out correctly, and that they will be 
        redirected to the login page
        """

        # Click register menu link
        self.driver.find_element_by_xpath("/html/body/div/header/nav/ul/li[2]/a").click()
        time.sleep(1)

        # Fill in registration form
        self.driver.find_element_by_xpath('//*[@id="email"]').send_keys(test_admin_email)
        self.driver.find_element_by_xpath('//*[@id="first_name"]').send_keys(
            test_admin_first_name)
        self.driver.find_element_by_xpath('//*[@id="last_name"]').send_keys(
            test_admin_last_name)
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(
            test_admin_password)
        self.driver.find_element_by_xpath('//*[@id="confirm_password"]').send_keys(
            test_admin_password)
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        time.sleep(1)

        # Assert that browser redirects to login page
        assert url_for('login') in self.driver.current_url
    
    def test_addplayer(self):
        #click register menu link
        self.driver.find_element_by_xpath("/html/body/div/header/nav/ul/li[2]/a").click()
        time.sleep(1)

        # Fill in registration form
        self.driver.find_element_by_xpath('//*[@id="email"]').send_keys(test_admin_email)
        self.driver.find_element_by_xpath('//*[@id="first_name"]').send_keys(
            test_admin_first_name)
        self.driver.find_element_by_xpath('//*[@id="last_name"]').send_keys(
            test_admin_last_name)
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(
            test_admin_password)
        self.driver.find_element_by_xpath('//*[@id="confirm_password"]').send_keys(
            test_admin_password)
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        time.sleep(1)

        #click login menu link
        self.driver.find_element_by_xpath("/html/body/div/header/nav/ul/li[3]/a").click()
        time.sleep(1)
        #fill in the login form
        self.driver.find_element_by_xpath('//*[@id="email"]').send_keys(test_admin_email)
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(test_admin_password)
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        time.sleep(1)
        # Add Player link
        self.driver.find_element_by_xpath('//*[@id="nav-list"]/li[4]/a').click()
        # Add a Player Form
        self.driver.find_element_by_xpath('//*[@id="player_name"]').send_keys(test_player_name)
        self.driver.find_element_by_xpath('//*[@id="player_age"]').send_keys(
            test_player_age)
        self.driver.find_element_by_xpath('//*[@id="player_team"]').send_keys(
            test_player_team)
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        time.sleep(1)
        # click the link to add stats
        self.driver.find_element_by_xpath("/html/body/div/header/nav/ul/li[6]/a").click()
        # Add Stats
        self.driver.find_element_by_xpath('//*[@id="goals"]').send_keys(test_player_goals)
        self.driver.find_element_by_xpath('//*[@id="assists"]').send_keys(test_player_assists)
        self.driver.find_element_by_xpath('//*[@id="chances"]').send_keys(test_player_chances)
        self.driver.find_element_by_xpath('//*[@id="shots"]').send_keys(test_player_shots)
        self.driver.find_element_by_xpath('//*[@id="minutes"]').send_keys(test_player_minutes)
        self.driver.find_element_by_xpath('//*[@id="date"]').send_keys(test_player_date)
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()

        #assert that the browser displays the add player page
        assert url_for('addstats') in self.driver.current_url    
