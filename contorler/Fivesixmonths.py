#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
------------------------------------------------------
    Project : TongmingClient
    File    : Newborn.py 
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
from ui.fivesixmonths import Ui_fivesixmonths
import urls

class Display(QDialog, Ui_fivesixmonths): #显示
    def __init__(self,user_type,archives_info_from_eidt='',check_info_from_eidt='', info_stat='', parent=None):
        super(Display, self).__init__(parent)
        self.setupUi(self)
        self.user_type = user_type
        self.archives_info_from_eidt = archives_info_from_eidt
        self.check_info_from_eidt = check_info_from_eidt
        self.info_stat = info_stat
        self.initial_button()
        self.base_archives_info()
        self.checked_result_info()
        self.display()
        self.pushButton_2.setVisible(False)
        self.has_saved = False

    def initial_button(self):
        if self.user_type != '医生':
            self.pushButton.setVisible(False)
            self.pushButton.setDisabled(True)

    def base_archives_info(self):
        if self.archives_info_from_eidt == '':  # 统计入口点击
            res = requests.get(url=urls.archives_get, data=self.info_stat)
            if res.ok:
                self.archives_info = res.json()
        else:
            self.archives_info = self.archives_info_from_eidt

    def checked_result_info(self):
        if self.archives_info_from_eidt == '':  # 统计入口点击
            res = requests.get(url=urls.get_56months, data=self.info_stat)
            if res.ok:
                self.result_info = res.json()
        else:
            self.result_info = self.check_info_from_eidt

    def display(self):
        self.label_child_name.setText(self.archives_info['child_name'])
        self.label_child_sex.setText(self.archives_info['child_sex'])
        self.label_child_birthday.setText(self.archives_info['child_birthday'])
        self.label_child_cstl.setText(self.archives_info['gestational_age'])
        self.label_child_cstz.setText(self.archives_info['weight_born'])
        self.label_child_mother_name.setText(self.archives_info['parent_name'])
        self.label_child_mother_id.setText(self.archives_info['parent_id'])
        self.label_child_mother_tele.setText(self.archives_info['parent_tele'])
        self.label_child_mother_address.setText(self.archives_info['address'])
        self.label_child_mother_mys.setText(self.archives_info['mother_pregnancy_history'])
        self.label_child_mother_jwbs.setText(self.archives_info['past_medical_history'])
        self.label_child_mother_jzycbs.setText(self.archives_info['family_genetic_disease'])

        self.label_item.setText('5-6月')
        self.label_hospital.setText(self.result_info['check_hospital_name'])
        self.label_doctor.setText(self.result_info['check_doctor_name'])
        self.label_datetime.setText(self.result_info['check_datetime'])
        self.label_sjxw.setText(self.result_info['visual_behavior'])
        self.label_yyexzxzs_left.setText(self.result_info['infants_selective_gaze_left'])
        self.label_yyexzxzs_right.setText(self.result_info['infants_selective_gaze_right'])
        self.label_sdxyz_right.setText(self.result_info['optic_nystagmus_right'])
        self.label_sdxyz_left.setText(self.result_info['optic_nystagmus_left'])
        self.label_wyjc_left.setText(self.result_info['outer_eye_check_left'])
        self.label_wyjc_right.setText(self.result_info['outer_eye_check_right'])
        self.label_ywjc.setText(self.result_info['eye_direction'])
        self.label_yqzcjc.setText(self.result_info['nystagmus_check'])
        self.label_ydhgfs_left.setText(self.result_info['reflex_red_eyes_left'])
        self.label_ydhgfs_right.setText(self.result_info['reflex_red_eyes_right'])
        self.textBrowser_qtjc.setText(self.result_info['other_item'])
        self.label_jchz.setText(self.result_info['is_cooperation'])
        self.textBrowser_jcjl.setText(self.result_info['result'])
        self.textBrowser_yxjy.setText(self.result_info['suggestion'])

    @pyqtSlot()
    def on_pushButton_clicked(self):  # 保存基本档案和检查结果
        if self.archives_save() and self.save_check_record():
            QMessageBox.information(self, '提示', '保存成功')
            self.has_saved = True
        else:
            QMessageBox.information(self, '提示', '保存不成功')

    @pyqtSlot()
    def on_pushButton_2_clicked(self):  # 导出基本档案和检查结果为pdf格式
        pass

    def archives_save(self):  # 保存档案信息
        res = requests.post(urls.archives_update, data=self.archives_info)
        if res.ok:
            return True
        else:
            return False

    def save_check_record(self):
        res = requests.post(urls.save_56months, data=self.result_info)
        if res.ok:
            return True
        else:
            return False

    def closeEvent(self, QCloseEvent ):
        if self.has_saved:
            self.accept()
