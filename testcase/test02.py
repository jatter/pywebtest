# coding=utf-8
from pyse import Pyse, TestRunner
from nose.tools import with_setup
from time import sleep


def my_setup_function():
    print "test case start:"


def my_teardown_function():
    print "test case end."


@with_setup(my_setup_function, my_teardown_function)
def test02():
	''' testsearch '''
driver = Pyse("chrome")
driver.open("http://tb2c.qicolor.cn")
driver.type("xpath=>.//*[@id='keywords']", u"包")
driver.click("xpath=>html/body/div[2]/div[3]/div/div[1]/div/input[2]")
sleep(3)
driver.quit()



if __name__ == '__main__':
    TestRunner().run()