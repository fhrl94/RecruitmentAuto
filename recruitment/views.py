import pandas as pd
from django.db.models import Q
from django_pandas.io import read_frame

from recruitment.models import IntervieweeInformation, InterviewResult, IntervieweeEnterInformation, IntervieweeRecord, \
    gender_choices, Company, PositionChargeInformation, InterviewChannel, Position, InterviewRecord, Interviewer, \
    interview_date_time_choices, InterviewType

# Create your views here.
#  解析<IntervieweeInformation/InterviewResult/IntervieweeEnterInformation>
#  中的数据, 生成相应的原始数据


def parse_interviewee_info():
    """
    获取人员信息, 从<IntervieweeInformation/InterviewResult/IntervieweeEnterInformation>, 与<IntervieweeRecord>去重,
    存储到<IntervieweeRecord>
    :return:
    """
    df_interview_info = read_frame(IntervieweeInformation.objects.all(),
                                   fieldnames=['interviewee_name', 'interviewee_gender', 'interviewee_tel'],)
    df_interview_result = read_frame(InterviewResult.objects.all(),
                                     fieldnames=['interviewee_name', 'interviewee_gender', 'interviewee_tel',
                                                 'graduation_status'], )
    df_interview_enter_info = read_frame(IntervieweeEnterInformation.objects.all(),
                                         fieldnames=['interviewee_name', 'interviewee_gender', 'interviewee_tel',
                                                     'graduation_status'], )
    df_interview_record = read_frame(IntervieweeRecord.objects.all(),
                                     fieldnames=['interviewee_name', 'interviewee_gender', 'interviewee_tel',
                                                 'graduation_status', 'id'], )
    # df = df_interview_info.append(df_interview_result, sort=True).append(
    #     df_interview_enter_info, sort=True).reset_index(drop=True).drop_duplicates(
    #     subset=['interviewee_name', 'interviewee_gender', 'interviewee_tel'])
    df = pd.concat(
        [df_interview_result, df_interview_info, df_interview_enter_info], ignore_index=True, sort=False
    ).drop_duplicates(
            subset=['interviewee_name', 'interviewee_gender', 'interviewee_tel'])
    df_records = pd.concat([df, df_interview_record], sort=True, keys=['new', 'old']).drop_duplicates(
        keep=False, subset=['interviewee_name', 'interviewee_gender', 'interviewee_tel'])
    # df_records.to_clipboard()
    # 删除旧数据
    model_storage_old_delete(df_records, IntervieweeRecord, 'id')
    # 新数据保存
    try:
        interviewee_record_ins_list = []
        _choices = [one for one in zip(*gender_choices)]
        for index, row in df_records.loc['new'].iterrows():
            interviewee_record_ins = IntervieweeRecord()
            interviewee_record_ins.interviewee_name = row['interviewee_name']
            if row['interviewee_gender'] in _choices[1]:
                interviewee_record_ins.interviewee_gender = _choices[0][_choices[1].index(row['interviewee_gender'])]
            interviewee_record_ins.interviewee_tel = row['interviewee_tel']
            if pd.isnull(row['graduation_status']):
                interviewee_record_ins.graduation_status = None
            else:
                interviewee_record_ins.graduation_status = row['graduation_status']
            interviewee_record_ins_list.append(interviewee_record_ins)
        IntervieweeRecord.objects.bulk_create(interviewee_record_ins_list)
    except KeyError:
        pass
    print("人员信息已解析")

def parse_company():
    """
    公司解析
    :return:
    """
    df_interview_info = read_frame(IntervieweeInformation.objects.all(), fieldnames=['company', ], )
    df_interview_result = read_frame(InterviewResult.objects.all(), fieldnames=['company', ], )
    df_interview_enter_info = read_frame(IntervieweeEnterInformation.objects.all(), fieldnames=['company', ], )
    df_company = read_frame(
        Company.objects.all(), fieldnames=['company_name', 'id'], ).rename(columns={'company_name': 'company'})
    df = pd.concat(
        [df_interview_result, df_interview_info, df_interview_enter_info], ignore_index=True, sort=False
    ).drop_duplicates(
            subset=['company', ])
    df_records = pd.concat([df, df_company], sort=True, keys=['new', 'old']).drop_duplicates(
        keep=False, subset=['company', ])
    # 删除旧数据
    model_storage_old_delete(df_records, Company, 'id')
    # 新数据保存
    try:
        company_ins_list = []
        for index, row in df_records.loc['new'].iterrows():
            company_ins = Company()
            company_ins.company_name = row['company']
            company_ins.company_status = True
            company_ins_list.append(company_ins)
        Company.objects.bulk_create(company_ins_list)
    except KeyError:
        pass
    print("公司名称已解析")
    pass

def parse_position_charge_info():
    """
    解析招聘人员信息
    :return:
    """
    df_interview_info = read_frame(IntervieweeInformation.objects.all(),
                                   fieldnames=['position_charge_name', 'position_charge_tel'], )
    df_interview_enter_info = read_frame(IntervieweeEnterInformation.objects.all(),
                                         fieldnames=['position_charge_name', 'position_charge_tel'], )
    df_position_charge_info = read_frame(PositionChargeInformation.objects.all(),
                                         fieldnames=['position_charge_name', 'position_charge_tel', 'id'], )
    df = pd.concat(
        [df_interview_info, df_interview_enter_info], ignore_index=True, sort=False
    ).drop_duplicates(
            subset=['position_charge_name', 'position_charge_tel'])
    df_records = pd.concat([df, df_position_charge_info], sort=True, keys=['new', 'old']).drop_duplicates(
        keep=False, subset=['position_charge_name', 'position_charge_tel'])
    # 删除旧数据
    model_storage_old_delete(df_records, PositionChargeInformation, 'id')
    # 新数据保存
    try:
        position_charge_info_ins_list = []
        for index, row in df_records.loc['new'].iterrows():
            position_charge_info_ins = PositionChargeInformation()
            position_charge_info_ins.position_charge_name = row['position_charge_name']
            position_charge_info_ins.position_charge_tel = row['position_charge_tel']
            position_charge_info_ins.position_charge_status = True
            position_charge_info_ins_list.append(position_charge_info_ins)
        PositionChargeInformation.objects.bulk_create(position_charge_info_ins_list)
    except KeyError:
        pass
    print("招聘人员信息已解析")
    pass

def parse_position():
    """
    解析岗位
    :return:
    """
    df_interview_info = read_frame(IntervieweeInformation.objects.all(),
                                   fieldnames=['interview_position', 'company'], )
    df_interview_result = read_frame(InterviewResult.objects.all(),
                                     fieldnames=['interview_position', 'company', ], )
    df_interview_enter_info = read_frame(IntervieweeEnterInformation.objects.all(),
                                         fieldnames=['interview_position', 'company'], )
    df_position = read_frame(Position.objects.all(),
                             fieldnames=['position_name', 'belong_company__company_name', 'id'], )
    df_position = df_position.rename(columns={'position_name': 'interview_position',
                                              'belong_company__company_name': 'company',
                                              })
    df = pd.concat(
        [df_interview_info, df_interview_result, df_interview_enter_info], ignore_index=True, sort=False
    ).drop_duplicates(
            subset=['interview_position', 'company'])
    df_records = pd.concat([df, df_position], sort=True, keys=['new', 'old']).drop_duplicates(
        keep=False, subset=['interview_position', 'company'])
    # 删除旧数据
    model_storage_old_delete(df_records, Position, 'id')
    # 新数据保存
    try:
        position_ins_list = []
        for index, row in df_records.loc['new'].iterrows():
            position_ins = Position()
            position_ins.position_name = row['interview_position']
            position_ins.belong_company = Company.objects.get(company_name=row['company'])
            position_ins.position_status = True
            position_ins_list.append(position_ins)
        Position.objects.bulk_create(position_ins_list)
    except KeyError:
        pass
    print("岗位信息已解析")

#  渠道解析
def parse_interview_channel():
    """
    解析渠道信息
    :return:
    """
    fieldnames = ['interview_channel', ]
    df_interview_info = read_frame(IntervieweeInformation.objects.all(),
                                   fieldnames=fieldnames, )
    df_interview_result_info = read_frame(InterviewResult.objects.all(),
                                          fieldnames=fieldnames, )
    df_interview_enter_info = read_frame(IntervieweeEnterInformation.objects.all(),
                                         fieldnames=fieldnames, )
    df_interview_channel_info = read_frame(InterviewChannel.objects.all(),
                                           fieldnames=['interview_channel_name', 'id'], ).rename(
        columns={'interview_channel_name': 'interview_channel'})
    df = pd.concat(
        [df_interview_info, df_interview_result_info, df_interview_enter_info], ignore_index=True, sort=False
    ).drop_duplicates(
            subset=fieldnames)
    df_records = pd.concat([df, df_interview_channel_info], sort=True, keys=['new', 'old']).drop_duplicates(
        keep=False, subset=fieldnames)
    # 删除旧数据
    model_storage_old_delete(df_records, InterviewChannel, 'id')
    # 新数据保存
    try:
        interview_channel_info_ins_list = []
        for index, row in df_records.loc['new'].iterrows():
            interview_channel_ins = InterviewChannel()
            interview_channel_ins.interview_channel_name = row['interview_channel']
            interview_channel_ins.interview_channel_status = True
            interview_channel_info_ins_list.append(interview_channel_ins)
        InterviewChannel.objects.bulk_create(interview_channel_info_ins_list)
    except KeyError:
        pass
    # print(df_records)
    print("渠道解析信息已解析")

def parse_interviewer():
    df_interviewer_first = read_frame(InterviewResult.objects.filter(
        ~Q(interviewer_first='')).all(), fieldnames=['interviewer_first', ], ).rename(
        columns={'interviewer_first': 'interviewer'})
    df_interviewer_second = read_frame(InterviewResult.objects.filter(
        ~Q(interviewer_second='')).all(), fieldnames=['interviewer_second', ], ).rename(
        columns={'interviewer_second': 'interviewer'})
    df_interviewer = read_frame(Interviewer.objects.all(), fieldnames=['interviewer_name', 'id']).rename(
        columns={'interviewer_name': 'interviewer'})
    df = pd.concat(
        [df_interviewer_first, df_interviewer_second, ], ignore_index=True, sort=False
    ).drop_duplicates(
            subset=['interviewer', ])
    df_records = pd.concat([df, df_interviewer], sort=True, keys=['new', 'old']).drop_duplicates(
        keep=False, subset=['interviewer', ])
    # 删除旧数据
    model_storage_old_delete(df_records, Interviewer, 'id')
    # 新数据保存
    try:
        interviewer_ins_list = []
        for index, row in df_records.loc['new'].iterrows():
            interviewer_ins = Interviewer()
            interviewer_ins.interviewer_name = row['interviewer']
            interviewer_ins.interviewer_status = True
            interviewer_ins_list.append(interviewer_ins)
        Interviewer.objects.bulk_create(interviewer_ins_list)
    except KeyError:
        pass
    print('面试官解析完成')
    pass

def parse_interview_result():
    # 定义所有的面试信息
    interview_record_ins_list = []
    # interviewer_second_query = ~Q(interviewer_second='') or Q(interviewer_second__isnull=False)
    interviewer_second_query = Q()
    df_interview_result = read_frame(InterviewResult.objects.filter(interviewer_second_query), )
    df_interviewee_record = read_frame(IntervieweeRecord.objects.all(),
                                       fieldnames=['interviewee_name', 'interviewee_tel', 'id'], )
    # 匹配人员信息
    df_interview_result = df_interview_result.merge(
        df_interviewee_record,
        on=('interviewee_name', 'interviewee_tel'), how='left', suffixes=('', '_interview_record_ins'))
    #  提示没有匹配的人员 (基本不会出现)

    # 匹配岗位信息
    df_position = read_frame(Position.objects.all(), fieldnames=['position_name', 'belong_company__company_name', 'id'], )
    df_position = df_position.rename(columns={'position_name': 'interview_position',
                                              'belong_company__company_name': 'company',
                                              })
    df_interview_result = df_interview_result.merge(
        df_position,
        on=('interview_position', 'company'), how='left', suffixes=('', '_position_ins')
    )
    #  提示没有匹配的岗位

    # 匹配渠道信息
    df_interview_channel_info = read_frame(InterviewChannel.objects.all(),
                                           fieldnames=['interview_channel_name', 'id'], ).rename(
        columns={'interview_channel_name': 'interview_channel'})
    df_interview_result = df_interview_result.merge(
        df_interview_channel_info,
        on=('interview_channel', ), how='left', suffixes=('', '_interview_channel_ins')
    )
    #  提示没有匹配的渠道

    #  分初试和复试

    # 匹配<复试面试官>信息
    df_interviewer = read_frame(Interviewer.objects.all(), fieldnames=['interviewer_name', 'id']).rename(
        columns={'interviewer_name': 'interviewer_second'})
    df_interview_result = df_interview_result.merge(
        df_interviewer,
        on=('interviewer_second', ), how='left', suffixes=('', '_interviewer_second_ins')
    )
    #  提示没有匹配的<复试面试官>

    # 匹配<初试面试官>信息
    df_interviewer = read_frame(Interviewer.objects.all(), fieldnames=['interviewer_name', 'id']).rename(
        columns={'interviewer_name': 'interviewer_first'})
    df_interview_result = df_interview_result.merge(
        df_interviewer,
        on=('interviewer_first', ), how='left', suffixes=('', '_interviewer_first_ins')
    )
    #  提示没有匹配的<初试面试官>

    # 将 InterviewRecord 数据整合为 原始表
    df_interview_record_first = read_frame(InterviewRecord.objects.filter(
        interview_type=InterviewType.objects.get(interview_type='初试')).all(), verbose=False)
    df_interview_record_second = read_frame(InterviewRecord.objects.filter(
        interview_type=InterviewType.objects.get(interview_type='复试')).all(), verbose=False)
    df_interview_record = df_interview_record_first.merge(
        df_interview_record_second,
        on=('interview_date', 'interview_date_time', 'interview_position', 'interview_channel', 'interviewee_name'),
        how='left',
        suffixes=('_first_ins', '_second_ins')
    )
    # 数据和原始表保持统一
    df_interview_record['interview_date_time'].replace({'0': '上午', '1': '下午'}, inplace=True)
    df_interview_record.rename(
        columns={
            'interview_position': 'id_position_ins',
            'interview_channel': 'id_interview_channel_ins',
            'interviewee_name': 'id_interview_record_ins',
            # 'interview_result': 'interview_second_result',
            'interviewer_first_ins': 'id_interviewer_first_ins',
            'interviewer_second_ins': 'id_interviewer_second_ins',
         }, inplace=True
    )
    # 有复试结果, 第二次面试结果就是复试结果, 否则就是初试结果
    df_interview_record['interview_second_result'] = pd.np.where(
        pd.isnull(df_interview_record['interview_result_second_ins']),
        df_interview_record['interview_result_first_ins'],
        df_interview_record['interview_result_second_ins']
    )

    # 将 <原始表>和 <InterviewRecord 整合原始表> 进行比对, 删除重复
    difference_col = ['interview_date', 'interview_date_time', 'id_position_ins', 'id_interview_channel_ins',
                      'id_interview_record_ins', 'id_interviewer_first_ins', 'id_interviewer_second_ins',
                      'interview_second_result', ]
    id_col = ['id_first_ins', 'id_second_ins', ]
    difference_df = pd.concat(
        [df_interview_result[difference_col], df_interview_record[difference_col + id_col]],
        keys=['new', 'old'], sort=False,
    ).drop_duplicates(keep=False, subset=difference_col)

    #  删除不存在的旧数据
    try:
        for index, row in difference_df.loc['old'].iterrows():
            print("错误数据删除")
            print(difference_df.loc['old'].loc[index])
            for one in id_col:
                if pd.isnull(row[one]) is False:
                    InterviewRecord.objects.get(pk=row[one]).delete()
    except KeyError:
        print("无数据删除")
        pass

    try:
        #  复试结果创建
        interview_record_ins_list += interview_second_storage(difference_df.loc['new'])
        #  初试结果创建
        interview_record_ins_list += interview_first_storage(difference_df.loc['new'])
        #  存储新增数据
        print("新增{num}条数据".format(num=len(interview_record_ins_list)))
        InterviewRecord.objects.bulk_create(interview_record_ins_list)
    except KeyError:
        print("无新增数据")

    # df_interview_result.to_clipboard()
    pass


def interview_second_storage(df_interview_result):
    """
    unique_together = ('interview_date', 'interviewee_name', 'interview_position', 'interview_type')
    :param df_interview_result:
    :return:
    """
    _choices = [one for one in zip(*interview_date_time_choices)]
    interview_record_ins_list = []
    for index, row in df_interview_result.iterrows():
        if pd.isnull(row['id_interviewer_second_ins']):
            continue
        interview_record_ins = InterviewRecord()
        interview_record_ins.interview_date = row['interview_date']
        interview_record_ins.interview_date_time = _choices[0][_choices[1].index(row['interview_date_time'])]
        interview_record_ins.interview_position = Position.objects.get(pk=row['id_position_ins'])
        interview_record_ins.interview_channel = InterviewChannel.objects.get(pk=row['id_interview_channel_ins'])
        interview_record_ins.interviewee_name = IntervieweeRecord.objects.get(pk=row['id_interview_record_ins'])
        interview_record_ins.interviewer = Interviewer.objects.get(pk=row['id_interviewer_second_ins'])
        interview_record_ins.interview_type = InterviewType.objects.get(interview_type='复试')
        interview_record_ins.interview_result = row['interview_second_result']
        interview_record_ins_list.append(interview_record_ins)
    # InterviewRecord.objects.bulk_create(interview_record_ins_list)
    print("复试结果已解析")
    return interview_record_ins_list
    pass

def interview_first_storage(df_interview_result):
    """
    unique_together = ('interview_date', 'interviewee_name', 'interview_position', 'interview_type')
    :param df_interview_result:
    :return:
    """
    _choices = [one for one in zip(*interview_date_time_choices)]
    interview_record_ins_list = []
    for index, row in df_interview_result.iterrows():
        interview_record_ins = InterviewRecord()
        interview_record_ins.interview_date = row['interview_date']
        interview_record_ins.interview_date_time = _choices[0][_choices[1].index(row['interview_date_time'])]
        interview_record_ins.interview_position = Position.objects.get(pk=row['id_position_ins'])
        interview_record_ins.interview_channel = InterviewChannel.objects.get(pk=row['id_interview_channel_ins'])
        interview_record_ins.interviewee_name = IntervieweeRecord.objects.get(pk=row['id_interview_record_ins'])
        interview_record_ins.interviewer = Interviewer.objects.get(pk=row['id_interviewer_first_ins'])
        interview_record_ins.interview_type = InterviewType.objects.get(interview_type='初试')
        if pd.isnull(row['id_interviewer_second_ins']):
            interview_record_ins.interview_result = row['interview_second_result']
        else:
            interview_record_ins.interview_result = '通过'
        interview_record_ins_list.append(interview_record_ins)
    # InterviewRecord.objects.bulk_create(interview_record_ins_list)
    print("初试结果已解析")
    return interview_record_ins_list
    pass

def model_storage_old_delete(difference_df, model, f_id):
    """
    删除错误信息
    :param difference_df:
    :param model:
    :param f_id:
    :return:
    """
    try:
        for index, row in difference_df.loc['old'].iterrows():
            print("错误数据删除")
            print(difference_df.loc['old'].loc[index])
            model.objects.get(pk=row[f_id]).delete()
        print("新增{num}条数据".format(num=len(difference_df.loc['old'])))
    except KeyError:
        print("无数据删除")
        pass
    pass
