# -*- coding: utf-8 -*-
#coding=utf-8
import web,time
from action.base import base as baseAction
import model
class pageelement(baseAction):
    def __init__(self):
        if self.isLogin() != True:
            raise web.seeother('/')
        baseAction.__init__(self)
        settings = self.getSettings()
        self.assignTplDir(settings.ADMIN_TPL_DIR)

    def add(self):
        return self.display('elementAdd')

    def save(self):
        userInput = self.getInput()
        data = {
            'ELEMENT_TYPE': userInput['eletype'],
            'ELEMENT_XPATH': userInput['elexpath'],
            'ELEMENT_VALUE': userInput['elevalue'],
            'CASE_ID': userInput['caseid']
        }
        status = model.pageelement().insert(data)
        if status:
            return self.success('保存成功',self.makeUrl('pageelement','list'))
        else:
            return self.error('保存失败')

    def list(self):
        inputParams = self.getInput()
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        settings = self.getSettings()
        count = settings.PER_PAGE_COUNT
        offset= (page-1)*count if page > 0 else 0
        elementObj = model.pageelement()
        condition = {}
        listData = elementObj.getOne('COUNT(*) AS `total`',condition)
        totalCount = listData['total']
        elementList = elementObj.getList('*',condition,'ELEMENT_ID desc',str(offset)+','+str(count))
        self.assign('elementList',elementList)
        pageString = self.getPageStr(self.makeUrl('pageelement','list'),page,count,totalCount)
        self.assign('pageString',pageString)
        return self.display('elementList')

    def edit(self):
        inputParams = self.getInput()
        if not inputParams.has_key('id') :
            return self.error('测试用例不存在')
        id=inputParams['id']
        condition={'ELEMENT_ID':str(id)}
        atl=model.pageelement().getOne('*',condition)
        self.assign('atl',atl)
        return self.display('elementEdit')

    def modify(self):
        userInput= self.getInput()
        data={
            'ELEMENT_TYPE': userInput['eletype'],
            'ELEMENT_XPATH': userInput['elexpath'],
            'ELEMENT_VALUE': userInput['elevalue'],
        }
        condition = {'ELEMENT_ID':userInput['id']}
        status = model.pageelement().update(data,condition)
        if status:
            return self.success('修改成功',self.makeUrl('pageelement','list'))
        else:
            return self.error('修改失败')

    def delete(self):
        inputParams = self.getInput()
        if not inputParams.has_key('id') :
            return self.error('测试用例不存在')
        id=inputParams['id']
        condition={'ELEMENT_ID':str(id)}
        result=model.pageelement().delete(condition)
        if result:
            return self.success('删除成功',self.makeUrl('pageelement','list'))
        else:
            return self.error('删除失败')