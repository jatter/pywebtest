# -*- coding: utf-8 -*-
#coding=utf-8
import web,time
from action.base import base as baseAction
import model
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
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        data = {
            'CASE_NAME': userInput['casename'],
            'FILE_NAME': userInput['filename'],
            'PAGE_URL': userInput['pageurl'],
            'CREATE_TIME': date,
        }
        status = model.testcase().insert(data)
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
        pageString = self.getPageStr(self.makeUrl('case','list'),page,count,totalCount)
        self.assign('pageString',pageString)
        return self.display('caseList')

    def edit(self):
        inputParams = self.getInput()
        if not inputParams.has_key('CASE_ID') :
            return self.error('测试用例不存在')
        id=inputParams['CASE_ID']
        condition={'CASE_ID':str(id)}
        atl=model.testcase().getOne('*',condition)
        self.assign('atl',atl)
        return self.display('caseEdit')

    def modify(self):
        userInput= self.getInput()
        data={
            'CASE_NAME': userInput['casename'],
            'FILE_NAME': userInput['filename'],
            'PAGE_URL': userInput['pageurl'],
        }
        condition = {'id':userInput['CASE_ID']}
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
        condition={'id':str(id)}
        result=model.testcase().delete(condition)
        if result:
            return self.success('删除成功',self.makeUrl('testcase','list'))
        else:
            return self.error('删除失败')