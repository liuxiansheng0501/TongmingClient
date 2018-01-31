#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
------------------------------------------------------
    Project : TongmingClient
    File    : conf.py 
    Time    : 2018/01/18 
    Author  : liulijun
    Site    : https://github.com/markliu666/
------------------------------------------------------
"""

unchecklist_head={
    'child_name':'儿童姓名',
    'parent_name':'家长姓名',
    'parent_tele':'家长电话',
    'appointment_item':'预约项目',
    'appointment_doctor_name':'预约医生',
    'recorder_name':'记录人',
    'record_datetime':'记录时间'
}

query_checked_head={
    'check_item':'检查项目',
    'check_datetime':'检查日期',
    'checked_child_name':'儿童姓名',
    'checked_child_parent_name':'家长姓名',
    'result':'检查结论',
}

stat_checked_head={
    'check_hospital':'检查医院',
    'check_doctor':'检查医生',
    'check_item':'检查项目',
    'check_child_name':'检查数目',
}

staff_manage={
    'staff_name':'医护姓名',
    'staff_type':'医护类型',
    'staff_id':'联系方式',
    'staff_passwd':'登录密码',
}

hospital_manage={
    'hospital_id':'医院编号',
    'hospital_name':'医院名称',
    'admin_name':'管理员',
    'admin_tele':'联系方式',
    'admin_id':'管理员账号',
    'admin_psw':'登录密码',
}

if __name__=="__main__":
    print(unchecklist_head.keys())