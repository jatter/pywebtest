# -*- coding: utf-8 -*-
#coding=utf-8
import web,time
from action.base import base as baseAction
import model
import HTMLParser
from mako.template import Template
class testcase(baseAction):
    def __init__(self):
        if self.isLogin() != True:
            raise web.seeother('/')
        baseAction.__init__(self)
        settings = self.getSettings()
        self.assignTplDir(settings.ADMIN_TPL_DIR)

    def add(self):
        return self.display('caseAdd')

    def save(self):
        userInput = self.getInput()
        html_parser = HTMLParser.HTMLParser()
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        casedata = {
            'CASE_NAME': userInput['casename'],
            'FILE_NAME': userInput['filename'],
            'PAGE_URL': userInput['pageurl'],
            'ELE_NUM': userInput['elenum'],
            'CREATE_TIME': date
        }
        mytemplate = Template(filename='caseTemplate1.txt', output_encoding='utf-8')
        result = mytemplate.render(pageurl=userInput['pageurl'], casename=userInput['casename'],casedesc=userInput['casedesc'])
        f = open("testcase/" + userInput['filename'], 'w')
        f.write(result)
        f.close()
        status1 = model.testcase().insert(casedata)
        condition = {'CASE_NAME': userInput['casename']}
        atl = model.testcase().getOne('*', condition)
        elenum  = int(userInput['elenum'])
        for i in range(0,elenum):
            m = str(i)
            type = userInput['eletype' + m + '']
            if type == u"文本框":
                f = open("testcase/" + userInput['filename'], 'a')
                mytemplate = Template(filename='inputTemplate.txt', output_encoding='utf-8')
                elelpath1 = userInput['elexpath' + m + '']
                elepath2 = html_parser.unescape(elelpath1)
                result = mytemplate.render(elexpath=elepath2, elevalue=userInput['elevalue'+m+''])
                f.write(result)
                f.close()
            elif type == u"按钮":
                f = open("testcase/" + userInput['filename'], 'a')
                mytemplate = Template(filename='clickTemplate.txt', output_encoding='utf-8')
                elelpath1 = userInput['elexpath' + m + '']
                elepath2 = html_parser.unescape(elelpath1)
                result = mytemplate.render(elexpath=elepath2)
                f.write(result)
                f.close()

            eledata = {
                'ELEMENT_TYPE': type,
                'ELEMENT_XPATH': userInput['elexpath'+m+''],
                'ELEMENT_VALUE': userInput['elevalue'+m+''],
                'CASE_ID': atl['CASE_ID']
            }
            status2 = model.pageelement().insert(eledata)
        status = status1 and status2
        fadd = open("caseTemplate2.txt",'r')
        f = open("testcase/"+userInput['filename'], 'a')
        f.write(fadd.read())
        fadd.close()
        f.close()
        if status:
            return self.success('保存成功',self.makeUrl('testcase','list'))
        else:
            return self.error('保存失败')

    def list(self):
        inputParams = self.getInput()
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        settings = self.getSettings()
        count = settings.PER_PAGE_COUNT
        offset= (page-1)*count if page > 0 else 0
        caseObj = model.testcase()
        condition = {}
        listData = caseObj.getOne('COUNT(*) AS `total`',condition)
        totalCount = listData['total']
        caseList = caseObj.getList('*',condition,'CASE_ID desc',str(offset)+','+str(count))
        self.assign('caseList',caseList)
        pageString = self.getPageStr(self.makeUrl('testcase','list'),page,count,totalCount)
        self.assign('pageString',pageString)
        return self.display('caseList')

    def edit(self):
        inputParams = self.getInput()
        if not inputParams.has_key('id') :
            return self.error('测试用例不存在')
        id=inputParams['id']
        condition={'CASE_ID':str(id)}
        atl=model.testcase().getOne('*',condition)
        elelist = model.pageelement().getList('*',condition)
        self.assign('atl',atl)
        self.assign('elelist',elelist)
        return self.display('caseEdit')

    def modify(self):
        userInput= self.getInput()
        data={
            'CASE_NAME': userInput['casename'],
            'FILE_NAME': userInput['filename'],
            'PAGE_URL': userInput['pageurl']
        }
        condition = {'CASE_ID':userInput['id']}
        status = model.testcase().update(data,condition)
        if status:
            return self.success('修改成功',self.makeUrl('testcase','list'))
        else:
            return self.error('修改失败')

    def delete(self):
        inputParams = self.getInput()
        if not inputParams.has_key('id') :
            return self.error('测试用例不存在')
        id=inputParams['id']
        condition={'CASE_ID':str(id)}
        result=model.testcase().delete(condition)
        if result:
            return self.success('删除成功',self.makeUrl('testcase','list'))
        else:
            return self.error('删除失败')