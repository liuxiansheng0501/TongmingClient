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
from ui.fiveyears_edit import Ui_fiveyears
import urls
import time
import dict_const
from contorler import Appointment
import re
import numpy as np

IDCARD_REGEX = '[1-9][0-9]{14}([0-9]{2}[0-9X])?'
SJXW=['通过','未通过','未检查']
SDXYZ=['可引出眼震','未引出眼震','不配合','未检查']
WYJC=['未见异常','泪道堵塞','结膜炎','其它：','未检查']
TKDGFS=['正常','异常','未检查']
YDHGFS=['正常','异常','未检查']
SLCS=['正常','无','不配合','未检查']
JCHZ=['是','否']
YXJY=['定期眼科检查：3个月复查','定期眼科检查：6个月复查', '眼科门诊就诊，进一步检查治疗']
JCJL=['所查项目未见异常','其它：']
YWJC=['正位','斜视','未检查']
YQZCJC=['无震颤','有震颤','未检查']
SLJC=['远视力','近视力','矫正视力','未检查']
YYEXZXZS=[str(value) for value in [0.1,0.15,0.20,0.25,0.30,0.40,0.50,0.60,'未检查']]
DZSLJC=[str(value) for value in [0.025,0.05,0.1,0.2,0.25,0.33,0.5,0.66,1.0,'未检查']]
YYESRDJC=[str(value) for value in [0.008,0.016,0.03,0.06,0.13,0.27,'未检查']]
ETTXSLK=[str(value) for value in [0.2,0.25,0.30,0.50,0.70,1.0,'未检查']]
YSL=[str(value) for value in [0.1,0.12,0.15,0.20,0.25,0.30,0.40,0.50,0.60,0.80,1.00,1.20,1.50,2.00,'未检查']]
JSL=[str(value) for value in [0.1,0.12,0.15,0.20,0.25,0.30,0.40,0.50,0.60,0.80,1.00,1.20,1.50,2.00,'未检查']]
JZSL=[str(value) for value in [0.1,0.12,0.15,0.20,0.25,0.30,0.40,0.50,0.60,0.80,1.00,1.20,1.50,2.00,'未检查']]
QGJC1=[]
for value in list(np.arange(-18,18.25,0.25)):
    if value>=0:
        value="+"+str(value)
    value = str(value) + "0"
    QGJC1.append(value[0:value.index('.')]+value[value.index('.'):value.index('.')+3]+"DS")
QGJC3=[]
for value in list(np.arange(6.00,-0.25,-0.25)):
    value = str(value) + "0"
    QGJC3.append(value[0:value.index('.')]+value[value.index('.'):value.index('.')+3]+"DC")
QGJC5=[str(value) for value in range(5,185)]
QGZT=['正常范围','可疑（近视 远视 散光）','异常（近视 远视 散光）','未检查']


class Edit(QDialog, Ui_fiveyears): #显示
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

        self.setTabOrder(self.lineEdit_qgjc_right_1, self.lineEdit_qgjc_right_2)
        self.setTabOrder(self.lineEdit_qgjc_right_2, self.lineEdit_qgjc_right_3)
        self.setTabOrder(self.lineEdit_qgjc_right_3, self.lineEdit_qgjc_right_5)
        self.setTabOrder(self.lineEdit_qgjc_right_5, self.lineEdit_qgjc_left_1)
        self.setTabOrder(self.lineEdit_qgjc_left_1, self.lineEdit_qgjc_left_2)
        self.setTabOrder(self.lineEdit_qgjc_left_2, self.lineEdit_qgjc_left_3)
        self.setTabOrder(self.lineEdit_qgjc_left_3, self.lineEdit_qgjc_left_5)

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

    def initial_visible(self):
        self.textEdit_jcjl.setVisible(False)

    def initial_check_info(self):
        self.comboBox_sjxw.addItems(SJXW)

        self.comboBox_sljc_right_ysl.addItems(YSL)
        self.comboBox_sljc_right_jsl.addItems(JSL)
        self.comboBox_sljc_right_jzsl.addItems(JZSL)
        self.comboBox_sljc_left_ysl.addItems(YSL)
        self.comboBox_sljc_left_jsl.addItems(JSL)
        self.comboBox_sljc_left_jzsl.addItems(JZSL)

        self.comboBox_ettxslk_right.addItems(ETTXSLK)
        self.comboBox_ettxslk_left.addItems(ETTXSLK)

        self.comboBox_dzsljc_right.addItems(DZSLJC)
        self.comboBox_dzsljc_left.addItems(DZSLJC)

        self.comboBox_wyjyqjjc.addItems(YDHGFS)
        self.comboBox_ydjc.addItems(YDHGFS)

        self.comboBox_ywjc.addItems(YWJC)
        self.comboBox_qgjc_status.addItems(QGZT)
        self.comboBox_yqzcjc.addItems(YQZCJC)

        self.comboBox_jchz.addItems(JCHZ)
        self.comboBox_jcjl.addItems(JCJL)
        self.comboBox_yxjy.addItems(YXJY)

        self.lineEdit_qgjc_right_1.setCompleter(QCompleter(QGJC1))  # 将字典添加到lineEdit中
        self.lineEdit_qgjc_left_1.setCompleter(QCompleter(QGJC1))  # 将字典添加到lineEdit中
        self.lineEdit_qgjc_right_2.setCompleter(QCompleter(['+', '-']))  # 将字典添加到lineEdit中
        self.lineEdit_qgjc_right_3.setCompleter(QCompleter(QGJC3))  # 将字典添加到lineEdit中
        self.lineEdit_qgjc_left_3.setCompleter(QCompleter(QGJC3))  # 将字典添加到lineEdit中
        self.lineEdit_qgjc_right_5.setCompleter(QCompleter(QGJC5))  # 将字典添加到lineEdit中
        self.lineEdit_qgjc_left_5.setCompleter(QCompleter(QGJC5))  # 将字典添加到lineEdit中

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
        visual_behavior = self.comboBox_sjxw.currentText()

        dot_vision_check_left = self.comboBox_dzsljc_left.currentText()
        dot_vision_check_right = self.comboBox_dzsljc_right.currentText()

        if self.checkBox_qgjc_xtyg.isChecked():
            refraction_check_xtyg = self.checkBox_qgjc_xtyg.text()
        else:
            refraction_check_xtyg = ''
        if self.checkBox_qgjc_styg.isChecked():
            refraction_check_styg = self.checkBox_qgjc_styg.text()
        else:
            refraction_check_styg = ''
        refraction_check_status=self.comboBox_qgjc_status.currentText()
        refraction_check_left_1=self.lineEdit_qgjc_left_1.text()
        refraction_check_left_2 = self.lineEdit_qgjc_left_2.text()
        refraction_check_left_3 = self.lineEdit_qgjc_left_3.text()
        refraction_check_left_4 = self.lineEdit_qgjc_left_4.text()
        refraction_check_left_5 = self.lineEdit_qgjc_left_5.text()
        refraction_check_right_1 = self.lineEdit_qgjc_right_1.text()
        refraction_check_right_2 = self.lineEdit_qgjc_right_2.text()
        refraction_check_right_3 = self.lineEdit_qgjc_right_3.text()
        refraction_check_right_4 = self.lineEdit_qgjc_right_4.text()
        refraction_check_right_5 = self.lineEdit_qgjc_right_5.text()

        nystagmus_check = self.comboBox_yqzcjc.currentText()
        eye_direction = self.comboBox_ywjc.currentText()

        other_item = self.textEdit_qtjc.toPlainText()

        is_cooperation = self.comboBox_jchz.currentText()

        result = self.comboBox_jcjl.currentText()+self.textEdit_jcjl.toPlainText()

        suggestion = self.comboBox_yxjy.currentText()

        eye_sight_check_left_ysl=self.comboBox_sljc_left_ysl.currentText()
        eye_sight_check_left_jsl = self.comboBox_sljc_left_jsl.currentText()
        eye_sight_check_left_jzsl = self.comboBox_sljc_left_jzsl.currentText()
        eye_sight_check_right_ysl = self.comboBox_sljc_right_ysl.currentText()
        eye_sight_check_right_jsl = self.comboBox_sljc_right_ysl.currentText()
        eye_sight_check_right_jzsl = self.comboBox_sljc_right_ysl.currentText()
        if self.checkBox_sljc_peihe.isChecked():
            eye_sight_check_is_peihe=self.checkBox_sljc_peihe.currentText()
        else:
            eye_sight_check_is_peihe = ''

        children_graphics_vision_card_left=self.comboBox_ettxslk_left.currentText()
        children_graphics_vision_card_right = self.comboBox_ettxslk_right.currentText()
        outer_eye_anterior_segment_check=self.comboBox_wyjyqjjc.currentText()
        fundus_check=self.comboBox_ydjc.currentText()

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

                         'visual_behavior': visual_behavior,
                         'eye_sight_check_left_ysl': eye_sight_check_left_ysl,
                         'eye_sight_check_left_jsl': eye_sight_check_left_jsl,
                         'eye_sight_check_left_jzsl': eye_sight_check_left_jzsl,
                         'eye_sight_check_right_ysl': eye_sight_check_right_ysl,
                         'eye_sight_check_right_jsl': eye_sight_check_right_jsl,
                         'eye_sight_check_right_jzsl': eye_sight_check_right_jzsl,
                         'eye_sight_check_is_peihe':eye_sight_check_is_peihe,
                         'dot_vision_check_left': dot_vision_check_left,
                         'dot_vision_check_right': dot_vision_check_right,
                         'children_graphics_vision_card_left':children_graphics_vision_card_left,
                         'children_graphics_vision_card_right': children_graphics_vision_card_right,
                         'outer_eye_anterior_segment_check':outer_eye_anterior_segment_check,
                         'refraction_check_xtyg':refraction_check_xtyg,
                         'refraction_check_styg':refraction_check_styg,
                         'refraction_check_status': refraction_check_status,
                         'refraction_check_left_1': refraction_check_left_1,
                         'refraction_check_left_2': refraction_check_left_2,
                         'refraction_check_left_3': refraction_check_left_3,
                         'refraction_check_left_4': refraction_check_left_4,
                         'refraction_check_left_5': refraction_check_left_5,
                         'refraction_check_right_1': refraction_check_right_1,
                         'refraction_check_right_2': refraction_check_right_2,
                         'refraction_check_right_3': refraction_check_right_3,
                         'refraction_check_right_4': refraction_check_right_4,
                         'refraction_check_right_5': refraction_check_right_5,

                        'nystagmus_check': nystagmus_check,
                        'eye_direction': eye_direction,
                         'fundus_check': fundus_check,
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
    def on_lineEdit_qgjc_right_1_returnPressed(self):  # 屈光输入框跳转
        self.lineEdit_qgjc_right_2.setFocus(True)

    @pyqtSlot()
    def on_lineEdit_qgjc_right_2_returnPressed(self):  # 屈光输入框跳转
        self.lineEdit_qgjc_right_3.setFocus(True)

    @pyqtSlot()
    def on_lineEdit_qgjc_right_3_returnPressed(self):  # 屈光输入框跳转
        self.lineEdit_qgjc_right_4.setFocus(True)

    @pyqtSlot()
    def on_lineEdit_qgjc_right_4_returnPressed(self):  # 屈光输入框跳转
        self.lineEdit_qgjc_right_5.setFocus(True)

    @pyqtSlot()
    def on_lineEdit_qgjc_right_5_returnPressed(self):  # 屈光输入框跳转
        self.lineEdit_qgjc_left_1.setFocus(True)

    @pyqtSlot()
    def on_lineEdit_qgjc_left_1_returnPressed(self):  # 屈光输入框跳转
        self.lineEdit_qgjc_left_2.setFocus(True)

    @pyqtSlot()
    def on_lineEdit_qgjc_left_2_returnPressed(self):  # 屈光输入框跳转
        self.lineEdit_qgjc_left_3.setFocus(True)

    @pyqtSlot()
    def on_lineEdit_qgjc_left_3_returnPressed(self):  # 屈光输入框跳转
        self.lineEdit_qgjc_left_4.setFocus(True)

    @pyqtSlot()
    def on_lineEdit_qgjc_left_4_returnPressed(self):  # 屈光输入框跳转
        self.lineEdit_qgjc_left_5.setFocus(True)

    def keyPressEvent(self, event):  # 重载按下回车键事件
        pass

    @pyqtSlot()
    def on_pushButton_save_clicked(self):
        # res=self.archives_save()
        # if res['bool']:
        #     self.save_check_record()
        # elif res['type']==1:
        #     QMessageBox.warning(self,'提示','儿童基本档案保存未成功')
        from contorler import Fiveyears
        res1 = self.archives_save()
        if res1['bool']:
            res2 = self.save_check_record()
            self.Fiveyears = Fiveyears.Display(user_type=u'医生', archives_info_from_eidt=res1['type'],check_info_from_eidt=res2)
            self.Fiveyears.setWindowModality(Qt.ApplicationModal)  # 只能编辑当前弹出的页面
            self.Fiveyears.show()
            result = self.Fiveyears.exec_()
            if result == QDialog.Accepted:
                self.accept()

    @pyqtSlot(str)
    def on_comboBox_wyjc_left_currentTextChanged(self, text):
        if text == "其它：":
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

    @pyqtSlot(int)
    def on_checkBox_qgjc_xtyg_stateChanged(self):
        if self.checkBox_qgjc_xtyg.isChecked():
            self.checkBox_qgjc_styg.setCheckState(Qt.Unchecked)

    @pyqtSlot(int)
    def on_checkBox_qgjc_styg_stateChanged(self):
        if self.checkBox_qgjc_styg.isChecked():
            self.checkBox_qgjc_xtyg.setCheckState(Qt.Unchecked)

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
        rt = True
        if self.comboBox_child_sex.currentText() == '':
            rt = False
            self.label_v_child_sex.setText(u"*必填项")
        else:
            self.label_v_child_sex.clear()
        return rt

    @pyqtSlot(str)
    def on_dateEdit_child_birthday_dateChanged(self):  # 验证儿童生日输入是否正确
        rt = False
        if (datetime.strptime(self.dateEdit_child_birthday.text(), "%Y-%m-%d") - datetime.now()).days < -365 * 7:
            self.label_v_child_birthday.setText(u'*儿童出生日期应选择最近6年！')
        elif (datetime.strptime(self.dateEdit_child_birthday.text(), "%Y-%m-%d") - datetime.now()).days >= 0:
            self.label_v_child_birthday.setText(u'*儿童出生日期大于当前日期！')
        else:
            self.label_v_child_birthday.clear()
            rt = True
        return rt

    @pyqtSlot(str)
    def on_lineEdit_gestational_age_textChanged(self):  # 验证儿童胎龄输入是否正确
        rt = True
        if self.lineEdit_gestational_age.text() == '':
            rt = False
            self.label_v_gestational_age.setText(u'*请输入儿童胎龄！')
        else:
            if not self.lineEdit_gestational_age.text().__contains__('.'):
                if not self.lineEdit_gestational_age.text().isdigit():
                    rt = False
                    self.label_v_gestational_age.setText(u"*请输入正确格式，例如40或40.5！")
                else:
                    self.label_v_gestational_age.clear()
            else:
                if self.lineEdit_gestational_age.text().count('.') == 1 and self.lineEdit_gestational_age.text()[
                    -1] != '.':
                    for ch in self.lineEdit_gestational_age.text().split('.'):
                        if not ch.isdigit():
                            rt = False
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
    def on_lineEdit_weight_born_textChanged(self):  # 验证儿童出生体重输入是否正确
        rt = True
        if self.lineEdit_weight_born.text() == '':
            rt = False
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
    def on_lineEdit_parent_name_textChanged(self):  # 验证家长姓名输入是否正确
        rt = True
        if self.lineEdit_parent_name.text() == '':
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
    def on_lineEdit_parent_id_textChanged(self):  # 验证家长身份证输入是否正确
        rt = True
        if self.lineEdit_parent_id.text() == '':
            rt = False
            self.label_v_parent_id.setText(u'*请输入家长身份证号！')
        elif not is_valid_idcard(self.lineEdit_parent_id.text()):
            rt = False
            self.label_v_parent_id.setText(u'*请输入家长正确身份证号！')
        else:
            self.label_v_parent_id.clear()
        return rt

    @pyqtSlot(str)
    def on_lineEdit_parent_tele_textChanged(self):  # 验证家长联系方式输入是否正确
        rt = True
        if self.lineEdit_parent_tele.text() == '':
            rt = False
            self.label_v_parent_tele.setText(u'*请输入家长联系方式！')
        else:
            ph = re.findall(r"1\d{10}", self.lineEdit_parent_tele.text())
            if len(ph) == 0:
                rt = False
                self.label_v_parent_tele.setText(u'*请输入家长正确联系方式！')
            else:
                self.lineEdit_parent_tele.setText(ph[0])
                self.label_v_parent_tele.clear()
        return rt


def is_valid_idcard(idcard):  # 身份证验证
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
                     'hospital_name': 'frfr',
                     'child_name': '莫哈哈',
                     'child_sex': ';p;p',
                     'child_birthday': ';;p;p',
                     'gestational_age': 'frfr',
                     'weight_born': 'lolol;o',
                     'parent_name': 'frfr',
                     'parent_id': '431022199112203671',
                     'parent_tele': 'frfr',
                     'address': 'frffrgrh',
                     'mother_pregnancy_history': 'kiklili',
                     'past_medical_history': 'ujukuk',
                     'family_genetic_disease': 'gththyjhy'}
    app = QApplication(sys.argv)
    loginWindow=Edit(transfer_data)
    loginWindow.show()
    sys.exit(app.exec_())

