#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
------------------------------------------------------
    Project : TongmingClient
    File    : Newborn_edit.py 
    Time    : 2018/02/01 
    Author  : liulijun
    Site    : https://github.com/markliu666/
------------------------------------------------------
"""

import sys
import os
import requests
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from datetime import datetime
import configparser
from ui.newborn_edit import Ui_newborn
import urls
import time
import dict_const
from contorler import Appointment,Newborn
import re

IDCARD_REGEX = '[1-9][0-9]{14}([0-9]{2}[0-9X])?'
GZFY=['正常','弱','无反应','未检查']
SDXYZ=['可引出眼震','未引出眼震','不配合','未检查']
WYJC=['未见异常','泪道堵塞','结膜炎','其它：','未检查']
TKDGFS=['正常','异常','未检查']
YDHGFS=['正常','异常','未检查']
JCHZ=['是','否']
YXJY=['定期眼科检查：下次检查时间：42天','眼科门诊就诊，进一步检查治疗']
JCJL=['所查项目未见异常','其它：']


class Edit(QDialog, Ui_newborn): #显示
    def __init__(self,doctor_info, parent=None):
        super(Edit, self).__init__(parent)
        self.setupUi(self)
        self.setFixedHeight(800)
        self.setFixedWidth(1191)
        self.doctor_info=doctor_info
        self.initial_warning_info()
        self.initial_archives_info()
        self.initial_check_info()
        self.setLineEditOrder()
        self.initial_visible()

    def setLineEditOrder(self):  # 设置光标顺序
        self.setTabOrder(self.lineEdit_child_name, self.comboBox_child_sex)
        self.setTabOrder(self.comboBox_child_sex, self.dateEdit_child_birthday)
        self.setTabOrder(self.dateEdit_child_birthday, self.lineEdit_gestational_age)
        self.setTabOrder(self.lineEdit_gestational_age, self.lineEdit_weight_born)
        self.setTabOrder(self.lineEdit_weight_born, self.lineEdit_parent_name)
        self.setTabOrder(self.lineEdit_parent_name, self.lineEdit_parent_id)
        self.setTabOrder(self.lineEdit_parent_id, self.lineEdit_parent_tele)
        self.setTabOrder(self.lineEdit_parent_tele, self.comboBox_address1)
        self.setTabOrder(self.comboBox_address1, self.comboBox_address2)
        self.setTabOrder(self.comboBox_address2, self.comboBox_address3)
        self.setTabOrder(self.comboBox_address3, self.lineEdit_address_info)
        self.setTabOrder(self.lineEdit_address_info, self.textEdit_mother_pregnancy_history)
        self.setTabOrder(self.textEdit_mother_pregnancy_history, self.textEdit_past_medical_history)
        self.setTabOrder(self.textEdit_past_medical_history, self.textEdit_family_genetic_disease)

    def initial_archives_info(self): # 初始化基本信息
        if self.doctor_info['appointed']!=1:
            # 出生年月
            self.dateEdit_child_birthday.setDate(QDate.fromString(time.strftime("%Y-%m-%d", time.localtime()), 'yyyy-MM-dd'))
            # 性别选项
            self.comboBox_child_sex.addItems(list(Appointment.sex.keys()))
            # 家庭住址
            self.comboBox_address1.addItem(u'北京市')
            self.comboBox_address2.addItem(u'北京市')
            self.comboBox_address3.addItems(list(dict_const.BEIJING_TOWN.keys()))
        else:
            res = requests.get(urls.archives_get,data={'child_name':self.doctor_info['child_name'],'parent_id':self.doctor_info['parent_id']})
            if res.ok:
                child_info = res.json()
                self.lineEdit_child_name.setText(child_info['child_name'])
                self.comboBox_child_sex.addItems(list(Appointment.sex.keys()))
                self.comboBox_child_sex.setCurrentIndex(Appointment.sex[child_info['child_sex']])
                self.dateEdit_child_birthday.setDate(QDate.fromString(child_info['child_birthday']))
                self.lineEdit_gestational_age.setText(child_info['gestational_age'])
                self.lineEdit_weight_born.setText(child_info['weight_born'])
                self.lineEdit_parent_name.setText(child_info['parent_name'])
                self.lineEdit_parent_id.setText(child_info['parent_id'])
                self.lineEdit_parent_tele.setText(child_info['parent_tele'])
                self.comboBox_address1.addItem(u'北京市')
                self.comboBox_address2.addItem(u'北京市')
                self.comboBox_address3.addItems(list(dict_const.BEIJING_TOWN.keys()))
                self.comboBox_address3.setCurrentIndex(dict_const.BEIJING_TOWN[child_info['address'][6:9]])
                self.lineEdit_address_info.setText(child_info['address'][9:])
                self.textEdit_mother_pregnancy_history.setText(child_info['mother_pregnancy_history'])
                self.textEdit_past_medical_history.setText(child_info['past_medical_history'])
                self.textEdit_family_genetic_disease.setText(child_info['family_genetic_disease'])

    def initial_warning_info(self):
        self.label_v_child_name.setText(u"*必填项")
        self.label_v_gestational_age.setText(u"*必填项")
        self.label_v_weight_born.setText(u"*必填项")
        self.label_v_parent_name.setText(u"*必填项")
        self.label_v_parent_id.setText(u"*必填项")
        self.label_v_parent_tele.setText(u"*必填项")

    def initial_check_info(self):
        self.comboBox_gzfy_right.addItems(GZFY)
        self.comboBox_gzfy_left.addItems(GZFY)

        self.comboBox_sdxyz_right.addItems(SDXYZ)
        self.comboBox_sdxyz_left.addItems(SDXYZ)

        self.comboBox_wyjc_right.addItems(WYJC)
        self.comboBox_wyjc_left.addItems(WYJC)

        self.comboBox_tkdgfs_right.addItems(TKDGFS)
        self.comboBox_tkdgfs_left.addItems(TKDGFS)

        self.comboBox_ydhgfs_right.addItems(YDHGFS)
        self.comboBox_ydhgfs_left.addItems(YDHGFS)

        self.comboBox_jchz.addItems(JCHZ)
        self.comboBox_jcjl.addItems(JCJL)
        self.comboBox_yxjy.addItems(YXJY)

    def initial_visible(self):
        self.textEdit_wyjc_left.setVisible(False)
        self.textEdit_wyjc_right.setVisible(False)
        self.textEdit_jcjl.setVisible(False)

    def verification_queue_unique(self,cn,pid):#验证当天排队唯一性
        payload = (('child_name', cn), ('parent_id', pid))
        res = requests.get(urls.unique_queue, data=payload)
        if len(res.json())==0:
            return {'data':{},'appointed':False}
        else:
            return {'data':res.json(),'appointed':True}

    def archives_unique(self,cn,parent_id):#档案唯一性验证
        payload = (('child_name', cn),('parent_id', parent_id))
        res = requests.get(urls.archives_unique_url, data=payload)
        if len(res.json()) == 0:
            return {'data':{},'bool':True}
        else:
            return {'data':res.json(),'bool':False}

    def workbench_newborn_appoint_check(self,child_id,check_datetime):
        res=requests.post(urls.check_queue,data={'child_id':child_id,'check_time':check_datetime})
        if res.ok:
            pass

    def is_base_archives_valid(self):
        if self.label_v_child_name.text()=="":
            rt1=True
        else:
            rt1 = False
        if self.label_v_child_birthday.text()=="":
            rt2=True
        else:
            rt2 = False
        if self.label_v_gestational_age.text()=="":
            rt3=True
        else:
            rt3 = False
        if self.label_v_parent_id.text()=="":
            rt4=True
        else:
            rt4 = False
        if self.label_v_parent_name.text()=="":
            rt5=True
        else:
            rt5 = False
        if self.label_v_parent_tele.text()=="":
            rt6=True
        else:
            rt6 = False
        if self.label_v_weight_born.text()=="":
            rt7=True
        else:
            rt7 = False
        if rt1 and rt2 and rt3 and rt4 and rt5 and rt6 and rt7:
            return True
        else:
            return False

    def archives_save(self):#若第一次录入档案信息新建档案并保存
        if not self.is_base_archives_valid():
            QMessageBox.information(self, '提示', '请按要求填写儿童基本档案信息')
            return {'bool':False,'type':0}
        else:
            self.base_info={'doctor_name': self.doctor_info['doctor_name'],
                           'hospital_name': self.doctor_info['hospital_name'],
                           'child_name': self.lineEdit_child_name.text(),
                           'child_sex': self.comboBox_child_sex.currentText(),
                           'child_birthday': self.dateEdit_child_birthday.text(),
                           'gestational_age': self.lineEdit_gestational_age.text(),
                           'weight_born': self.lineEdit_weight_born.text(),
                           'parent_name': self.lineEdit_parent_name.text(),
                           'parent_id': self.lineEdit_parent_id.text(),
                           'parent_tele': self.lineEdit_parent_tele.text(),
                           'address': self.comboBox_address1.currentText()+self.comboBox_address2.currentText()+self.comboBox_address3.currentText()+self.lineEdit_address_info.text()}
            if self.textEdit_mother_pregnancy_history.toPlainText() in ['','\n']:
                self.base_info['mother_pregnancy_history']='无'
            else:
                self.base_info['mother_pregnancy_history'] = self.textEdit_mother_pregnancy_history.toPlainText()
            if self.textEdit_past_medical_history.toPlainText() in ['','\n']:
                self.base_info['past_medical_history']='无'
            else:
                self.base_info['past_medical_history'] = self.textEdit_past_medical_history.toPlainText()
            if self.textEdit_family_genetic_disease.toPlainText() in ['','\n']:
                self.base_info['family_genetic_disease']='无'
            else:
                self.base_info['family_genetic_disease'] = self.textEdit_family_genetic_disease.toPlainText()
            archives_info = {}
            res=self.archives_unique(self.base_info['child_name'],self.base_info['parent_id'])
            if res['bool']:
                res = requests.get(urls.child_id_max)
                if res.ok:
                    archives_info["child_id"] = "C" + str(int(res.json()["child_id"][1:]) + 1)
                else:
                    archives_info["child_id"] = "C1000001"
            else:
                archives_info["child_id"] = res['data'][0]['child_id']
            archives_info["child_name"] = self.base_info['child_name']
            archives_info["child_sex"] = self.base_info['child_sex']
            archives_info["child_birthday"] = self.base_info['child_birthday']
            archives_info["parent_id"] = self.base_info['parent_id']
            archives_info["parent_name"] = self.base_info['parent_name']
            archives_info["parent_tele"] = self.base_info['parent_tele']
            archives_info["address"] = self.base_info['address']
            archives_info["gestational_age"] = self.base_info['gestational_age']
            archives_info["weight_born"] = self.base_info['weight_born']
            archives_info["mother_pregnancy_history"] = self.base_info['mother_pregnancy_history']
            archives_info["past_medical_history"] = self.base_info['past_medical_history']
            archives_info["family_genetic_disease"] = self.base_info['family_genetic_disease']
            conf = configparser.ConfigParser()
            conf.read("./config")
            archives_info["recorder"] = conf.get('user', 'name')
            archives_info["record_hospital"] = conf.get('user', 'hospital')
            archives_info["record_datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return {'bool': True, 'type': archives_info}
            # res = requests.post(urls.archives_update, data=archives_info)
            # if res.ok:
            #     return {'bool': True, 'type': 0}
            # else:
            #     return {'bool': False, 'type': 1}

    def save_check_record(self):
        res = self.verification_queue_unique(self.base_info['child_name'],self.base_info['parent_id'])  # 档案中已保存有记录，只添加排队信息
        conf = configparser.ConfigParser()
        conf.read("./config")
        if res['appointed']:  # 预约了
            appoint_datetime = res['data'][0]['record_datetime']
            appoint_doctor_id = res['data'][0]['appointment_doctor_id']
            appoint_doctor_name = res['data'][0]['appointment_doctor_name']
            is_archives_unique=self.archives_unique(self.base_info['child_name'],self.base_info['parent_id'])
            self.workbench_newborn_appoint_check(is_archives_unique['data'][0]['child_id'],datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        else:  # 没有预约
            appoint_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            appoint_doctor_id = conf.get('user', 'account')
            appoint_doctor_name = self.base_info['doctor_name']
        check_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        check_doctor_id = conf.get('user', 'account')
        check_doctor_name = self.base_info['doctor_name']
        check_hospital_name = self.base_info['hospital_name']
        checked_child_name = self.base_info['child_name']
        checked_child_parent_id = self.base_info['parent_id']
        checked_child_parent_name = self.base_info['parent_name']
        # 检查内容
        light_response_left = self.comboBox_gzfy_left.currentText()
        light_response_right = self.comboBox_gzfy_right.currentText()

        optic_nystagmus_left = self.comboBox_sdxyz_left.currentText()
        optic_nystagmus_right = self.comboBox_sdxyz_right.currentText()

        outer_eye_check_left = self.comboBox_wyjc_left.currentText()+self.textEdit_wyjc_left.toPlainText()
        outer_eye_check_right = self.comboBox_wyjc_right.currentText()+self.textEdit_wyjc_right.toPlainText()

        pupil_reflects_on_light_left = self.comboBox_tkdgfs_left.currentText()
        pupil_reflects_on_light_right = self.comboBox_tkdgfs_right.currentText()

        reflex_red_eyes_left = self.comboBox_ydhgfs_left.currentText()
        reflex_red_eyes_right = self.comboBox_ydhgfs_right.currentText()

        other_item = self.textEdit_qtjc.toPlainText()

        is_cooperation = self.comboBox_jchz.currentText()

        result = self.comboBox_jcjl.currentText()+self.textEdit_jcjl.toPlainText()

        suggestion = self.comboBox_yxjy.currentText()

        save_contents = {'appoint_datetime': appoint_datetime,
                         'appoint_doctor_id': appoint_doctor_id,
                         'appoint_doctor_name': appoint_doctor_name,
                         'check_datetime': check_datetime,
                         'check_doctor_id': check_doctor_id,
                         'check_doctor_name': check_doctor_name,
                         'check_hospital_name': check_hospital_name,
                         'checked_child_name': checked_child_name,
                         'checked_child_parent_id': checked_child_parent_id,
                         'checked_child_parent_name': checked_child_parent_name,
                         'light_response_left': light_response_left,
                         'light_response_right': light_response_right,
                         'optic_nystagmus_left': optic_nystagmus_left,
                         'optic_nystagmus_right': optic_nystagmus_right,
                         'outer_eye_check_left': outer_eye_check_left,
                         'outer_eye_check_right': outer_eye_check_right,
                         'pupil_reflects_on_light_left': pupil_reflects_on_light_left,
                         'pupil_reflects_on_light_right': pupil_reflects_on_light_right,
                         'reflex_red_eyes_left': reflex_red_eyes_left,
                         'reflex_red_eyes_right': reflex_red_eyes_right,
                         'other_item': other_item,
                         'is_cooperation': is_cooperation,
                         'result': result,
                         'suggestion': suggestion}
        return save_contents
        # res = requests.post(urls.update_newborns, data=save_contents)
        # if res.ok:
        #     res=QMessageBox.information(self,'提示','保存成功')
        # else:
        #     res = QMessageBox.information(self, '提示', '请填写完全基本档案信息')
        # if res:
        #     self.accept()

    @pyqtSlot()
    def on_pushButton_save_clicked(self):
        # res=self.archives_save()
        # if res['bool']:
        #     self.save_check_record()
        # elif res['type']==1:
        #     QMessageBox.warning(self,'提示','儿童基本档案保存未成功')
        from contorler import Newborn
        res1 = self.archives_save()
        if res1['bool']:
            res2 = self.save_check_record()
            self.Newborn = Newborn.Display(user_type=u'医生', archives_info_from_eidt=res1['type'],check_info_from_eidt=res2)
            self.Newborn.setWindowModality(Qt.ApplicationModal)  # 只能编辑当前弹出的页面
            self.Newborn.show()
            result = self.Newborn.exec_()
            if result == QDialog.Accepted:
                self.accept()

    @pyqtSlot(str)
    def on_comboBox_wyjc_left_currentTextChanged(self,text):
        if text=="其它：":
            self.textEdit_wyjc_left.setVisible(True)
        else:
            self.textEdit_wyjc_left.setVisible(False)

    @pyqtSlot(str)
    def on_comboBox_wyjc_right_currentTextChanged(self, text):
        if text == "其它：":
            self.textEdit_wyjc_right.setVisible(True)
        else:
            self.textEdit_wyjc_right.setVisible(False)

    @pyqtSlot(str)
    def on_comboBox_jcjl_currentTextChanged(self, text):
        if text == "其它：":
            self.textEdit_jcjl.setVisible(True)
        else:
            self.textEdit_jcjl.setVisible(False)

    @pyqtSlot(str)
    def on_lineEdit_child_name_textChanged(self):  # 验证儿童姓名输入是否正确
        rt = True
        if self.lineEdit_child_name.text() == '':
            rt = False
            self.label_v_child_name.setText(u'*请输入儿童姓名！')
        else:
            for char in self.lineEdit_child_name.text():
                if char >= u"\u4e00" and char <= u"\u9fa6":
                    continue
                else:
                    rt = False
            if rt:
                self.label_v_child_name.clear()
            else:
                self.label_v_child_name.setText(u'*输入姓名中含有数字、英文字母等非法字符！')
        return rt

    @pyqtSlot(str)
    def on_lineEdit_child_sex_textChanged(self):
        rt=True
        if self.comboBox_child_sex.currentText()=='':
            rt=False
            self.label_v_child_sex.setText(u"*必填项")
        else:
            self.label_v_child_sex.clear()
        return rt

    @pyqtSlot(str)
    def on_dateEdit_child_birthday_dateChanged(self):#验证儿童生日输入是否正确
        rt=False
        if (datetime.strptime(self.dateEdit_child_birthday.text(),"%Y-%m-%d")-datetime.now()).days<-365*7:
            self.label_v_child_birthday.setText(u'*儿童出生日期应选择最近6年！')
        elif (datetime.strptime(self.dateEdit_child_birthday.text(),"%Y-%m-%d")-datetime.now()).days>=0:
            self.label_v_child_birthday.setText(u'*儿童出生日期大于当前日期！')
        else:
            self.label_v_child_birthday.clear()
            rt=True
        return rt

    @pyqtSlot(str)
    def on_lineEdit_gestational_age_textChanged(self):  #验证儿童胎龄输入是否正确
        rt = True
        if self.lineEdit_gestational_age.text()=='':
            rt=False
            self.label_v_gestational_age.setText(u'*请输入儿童胎龄！')
        else:
            if not self.lineEdit_gestational_age.text().__contains__('.'):
                if not self.lineEdit_gestational_age.text().isdigit():
                    rt=False
                    self.label_v_gestational_age.setText(u"*请输入正确格式，例如40或40.5！")
                else:
                    self.label_v_gestational_age.clear()
            else:
                if self.lineEdit_gestational_age.text().count('.')==1 and self.lineEdit_gestational_age.text()[-1]!='.':
                    for ch in self.lineEdit_gestational_age.text().split('.'):
                        if not ch.isdigit():
                            rt=False
                        else:
                            self.label_v_gestational_age.clear()
                else:
                    rt = False
            if rt:
                self.label_v_gestational_age.clear()
            else:
                self.label_v_gestational_age.setText(u'*请输入正确格式，例如40或40.5！')
        return rt

    @pyqtSlot(str)
    def on_lineEdit_weight_born_textChanged(self):#验证儿童出生体重输入是否正确
        rt = True
        if self.lineEdit_weight_born.text()=='':
            rt=False
            self.label_v_weight_born.setText(u'*请输入儿童出生体重！')
        else:
            if not self.lineEdit_weight_born.text().__contains__('.'):
                if not self.lineEdit_weight_born.text().isdigit():
                    rt = False
                    self.label_v_weight_born.setText(u"*请输入正确格式，例如3或3.5！")
                else:
                    self.label_v_weight_born.clear()
            else:
                if self.lineEdit_weight_born.text().count('.') == 1 and self.lineEdit_weight_born.text()[-1] != '.':
                    for ch in self.lineEdit_weight_born.text().split('.'):
                        if not ch.isdigit():
                            rt = False
                        else:
                            self.label_v_weight_born.clear()
                else:
                    rt = False
            if rt:
                self.label_v_weight_born.clear()
            else:
                self.label_v_weight_born.setText(u'*请输入正确格式，例如3或3.5！')
        return rt

    @pyqtSlot(str)
    def on_lineEdit_parent_name_textChanged(self):  #验证家长姓名输入是否正确
        rt = True
        if self.lineEdit_parent_name.text()=='':
            rt = False
            self.label_v_parent_name.setText(u'*请输入家长姓名！')
        else:
            for char in self.lineEdit_parent_name.text():
                if char >= u"\u4e00" and char <= u"\u9fa6":
                    continue
                else:
                    rt = False
            if rt:
                self.label_v_parent_name.clear()
            else:
                self.label_v_parent_name.setText(u'*输入姓名中含有数字、英文字母等非法字符！')
        return rt

    @pyqtSlot(str)
    def on_lineEdit_parent_id_textChanged(self):#验证家长身份证输入是否正确
        rt = True
        if self.lineEdit_parent_id.text()=='':
            rt = False
            self.label_v_parent_id.setText(u'*请输入家长身份证号！')
        elif not is_valid_idcard(self.lineEdit_parent_id.text()):
            rt= False
            self.label_v_parent_id.setText(u'*请输入家长正确身份证号！')
        else:
            self.label_v_parent_id.clear()
        return rt

    @pyqtSlot(str)
    def on_lineEdit_parent_tele_textChanged(self):#验证家长联系方式输入是否正确
        rt = True
        if self.lineEdit_parent_tele.text()=='':
            rt = False
            self.label_v_parent_tele.setText(u'*请输入家长联系方式！')
        else:
            ph=re.findall(r"1\d{10}", self.lineEdit_parent_tele.text())
            if len(ph)==0:
                rt=False
                self.label_v_parent_tele.setText(u'*请输入家长正确联系方式！')
            else:
                self.lineEdit_parent_tele.setText(ph[0])
                self.label_v_parent_tele.clear()
        return rt

def is_valid_idcard(idcard):#身份证验证
    if isinstance(idcard, int):
        idcard = str(idcard)
    if not re.match(IDCARD_REGEX, idcard):
        return False
    factors = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    items = [int(item) for item in idcard[:-1]]
    copulas = sum([a * b for a, b in zip(factors, items)])
    ckcodes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
    return ckcodes[copulas % 11].upper() == idcard[-1].upper()

if __name__=="__main__":
    transfer_data = {'doctor_name': '莫哈哈',
                     'hospital_name': 'frfr'}
    app = QApplication(sys.argv)
    loginWindow=Edit(transfer_data)
    loginWindow.show()
    sys.exit(app.exec_())

