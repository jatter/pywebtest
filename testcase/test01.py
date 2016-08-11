# coding=utf-8

from pyse import Pyse, TestRunner

from nose.tools import with_setup

from time import sleep





def my_setup_function():

    print "test case start:"





def my_teardown_function():

    print "test case end."





@with_setup(my_setup_function, my_teardown_function)

def test01():

	''' testlogin '''

driver = Pyse("chrome")

driver.open("http://tb2c.qicolor.cn/#/login")

driver.type("xpath=>.//*[@id='login_box']/form/div[1]/input", u"15951819465")

driver.type("xpath=>.//*[@id='login_box']/form/div[2]/input", u"123456")

driver.click("xpath=>.//*[@id='login_box']/form/a")

sleep(3)
driver.quit()



if __name__ == '__main__':
    TestRunner().run()