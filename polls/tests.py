from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
import random
import string
import time
from selenium.webdriver.support.ui import Select


class MySeleniumTests(StaticLiveServerTestCase):
    # carregar una BD de test
    # fixtures = ['testdb.json',]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)
        # creem superusuari
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()

    @classmethod
    def tearDownClass(cls):
        # tanquem browser
        # comentar la propera línia si volem veure el resultat de l'execució al navegador
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        # anem directament a la pàgina d'accés a l'admin panel
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))
        # comprovem que el títol de la pàgina és el que esperem
        self.assertEqual(self.selenium.title, "Log in | Django site admin")
        # introduïm dades de login i cliquem el botó "Log in" per entrar
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys('isard')
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('pirineus')
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()
        # testejem que hem entrat a l'admin panel comprovant el títol de la pàgina
        self.assertEqual(self.selenium.title, "Site administration | Django site admin")

        # Generar texto aleatorio
        def rand_text(n=12):
            return ''.join(random.choice(string.ascii_letters) for _ in range(n))

        # Crear una Question amb 1 Choice
        # Ir al boton Questions
        self.selenium.find_element(By.XPATH, '//a[text()="Questions"]').click()
        # Click en el boton Add (arriba derecha)
        self.selenium.find_element(By.XPATH, '//*[@id="content"]//a[contains(@class,"addlink")]').click()
        # Escribir texto aleatorio Question 1
        q1_text = rand_text(20)
        self.selenium.find_element(By.NAME, "question_text").send_keys(q1_text)
        # Escribir Date published (fecha y hora)
        self.selenium.find_element(By.NAME, "pub_date_0").send_keys("2026-02-01")
        self.selenium.find_element(By.NAME, "pub_date_1").send_keys("10:00:00")
        # Click en SAVE
        self.selenium.find_element(By.XPATH, '//input[contains(@value,"Save")]').click()

        # Ir al boton Choices
        self.selenium.find_element(By.XPATH, '//a[text()="Choices"]').click()
        # Click en el boton Add (arriba derecha)
        self.selenium.find_element(By.XPATH, '//*[@id="content"]//a[contains(@class,"addlink")]').click()
        # Seleccionar Question 1 en el desplegable
        Select(self.selenium.find_element(By.NAME, "question")).select_by_visible_text(q1_text)
        # Escribir texto aleatorio del Choice 1
        c1_text = rand_text(15)
        self.selenium.find_element(By.NAME, "choice_text").send_keys(c1_text)
        # Click en SAVE
        self.selenium.find_element(By.XPATH, '//input[contains(@value,"Save")]').click()

        # Crear una Question amb 100 Choices (bucle)
        # Ir al boton Questions
        self.selenium.find_element(By.XPATH, '//a[text()="Questions"]').click()
        # Click en el boton Add (arriba derecha)
        self.selenium.find_element(By.XPATH, '//*[@id="content"]//a[contains(@class,"addlink")]').click()
        # Escribir texto aleatorio Question 2
        q2_text = rand_text(20)
        self.selenium.find_element(By.NAME, "question_text").send_keys(q2_text)
        # Escribir Date published (fecha y hora)
        self.selenium.find_element(By.NAME, "pub_date_0").send_keys("2026-02-01")
        self.selenium.find_element(By.NAME, "pub_date_1").send_keys("11:00:00")
        # Click en SAVE
        self.selenium.find_element(By.XPATH, '//input[contains(@value,"Save")]').click()

        # Ir al boton Choices
        self.selenium.find_element(By.XPATH, '//a[text()="Choices"]').click()
        # Click en el boton Add (arriba derecha)
        self.selenium.find_element(By.XPATH, '//*[@id="content"]//a[contains(@class,"addlink")]').click()

        # Crear 100 choices con bucle usando "Save and add another"
        for i in range(100):
            # Seleccionar Question 2 en el desplegable
            Select(self.selenium.find_element(By.NAME, "question")).select_by_visible_text(q2_text)
            # Escribir texto aleatorio del Choice
            choice_text = rand_text(15)
            self.selenium.find_element(By.NAME, "choice_text").send_keys(choice_text)
            # Click en SAVE AND ADD ANOTHER
            self.selenium.find_element(By.XPATH, '//input[contains(@value,"Save and add another")]').click()

        # Comprova que anant al menú de Choices pots visualitzar 101
        # Ir al boton Choices (listado)
        self.selenium.find_element(By.XPATH, '//a[text()="Choices"]').click()
        # Comprobar que el texto visible del paginador indica 101
        paginator_text = self.selenium.find_element(By.XPATH, '//p[contains(@class,"paginator")]').text
        self.assertTrue("101" in paginator_text, paginator_text)
        # Pausa para ver
        time.sleep(10)
