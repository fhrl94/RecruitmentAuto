import xadmin
from xadmin import views
from xadmin.views import CommAdminView

from recruitment.models import IntervieweeInformation, InterviewResult, IntervieweeEnterInformation, IntervieweeRecord, \
    Company, PositionChargeInformation, Position, InterviewType, InterviewChannel, InterviewRecord
from recruitment.resources import IntervieweeInformationResource, InterviewResultResource, \
    IntervieweeEnterInformationResource
from recruitment.views import parse_interviewee_info, parse_company, parse_position_charge_info, parse_position, \
    parse_interviewer, parse_interview_channel, parse_interview_result


@xadmin.sites.register(IntervieweeInformation)
class IntervieweeInformationAdmin(object):
    import_export_args = {'import_resource_class': IntervieweeInformationResource, }
    list_display = ('interviewee_name', 'interviewee_gender', 'interviewee_tel', 'interview_position', 'interview_date',
                    'interview_time_slot', 'interview_channel', 'internal_recommended', 'company',
                    'position_charge_name', 'position_charge_tel', 'invitation_situation', )
    search_fields = ['interviewee_name', 'interviewee_tel']
    list_filter = ['interview_date', 'interview_position', 'company', 'interviewee_gender', 'interview_time_slot',
                   'position_charge_name', 'interview_channel'
                   ]
    actions = ['parse_action', ]

    def parse_action(self, request, queryset,):
        parse_interviewee_info()
        parse_company()
        parse_position_charge_info()
        parse_position()
        parse_interview_channel()
        parse_interviewer()
        parse_interview_result()

    parse_action.short_description = '人员解析'

@xadmin.sites.register(InterviewResult)
class InterviewResultAdmin(object):
    import_export_args = {'import_resource_class': InterviewResultResource, }
    list_display = ('interview_date', 'interview_date_time', 'interview_position', 'company', 'interview_channel',
                    'internal_recommended', 'interviewee_name', 'interviewee_gender', 'interviewee_tel',
                    'graduation_status', 'interviewer_first', 'interview_first_grade', 'interview_first_elimination',
                    'interviewer_second', 'interview_second_grade', 'interview_second_elimination',
                    'interview_second_result')
    search_fields = ['interviewee_name', 'interviewee_tel']
    list_filter = ['interview_date', 'interview_date_time', 'interview_position', 'company', 'interviewee_gender',
                   'graduation_status', 'interview_second_result', 'interview_channel',
                   ]


@xadmin.sites.register(IntervieweeEnterInformation)
class IntervieweeEnterInformationAdmin(object):
    import_export_args = {'import_resource_class': IntervieweeEnterInformationResource, }
    list_display = ('interviewee_enter_date', 'interviewee_name', 'company', 'interview_channel', 'internal_recommended',
                    'interviewee_department', 'interviewee_group', 'interviewee_gender', 'interview_position',
                    'graduation_status', 'interviewee_tel', 'invitation_situation', 'position_charge_name',
                    'position_charge_tel',
                    )
    search_fields = ['interviewee_name', 'interviewee_tel']
    list_filter = ['interviewee_enter_date', 'company', 'interview_channel', 'internal_recommended',
                   'interviewee_department', 'interviewee_group', 'interviewee_gender', 'interview_position',
                   'graduation_status',
                   ]

@xadmin.sites.register(IntervieweeRecord)
class IntervieweeRecordAdmin(object):
    list_display = ('interviewee_name', 'interviewee_gender', 'interviewee_tel', 'graduation_status',
                    )
    list_filter = ['interviewee_gender', 'interviewee_tel', 'graduation_status', ]
    search_fields = ['interviewee_name', ]

@xadmin.sites.register(Company)
class CompanyAdmin(object):
    list_display = ('company_name', 'company_coding', 'company_status',
                    )

@xadmin.sites.register(PositionChargeInformation)
class PositionChargeInformationAdmin(object):
    list_display = ('position_charge_name', 'position_charge_gender', 'position_charge_tel', 'position_charge_email',
                    'position_charge_status',
                    )


@xadmin.sites.register(Position)
class PositionAdmin(object):
    list_display = ('belong_company', 'position_name', 'position_coding', 'position_status',
                    )
    ordering = ['belong_company', 'position_name']


@xadmin.sites.register(InterviewType)
class InterviewTypeAdmin(object):
    list_display = ('interview_type', 'interview_type_coding', 'interview_type_status'
                    )

@xadmin.sites.register(InterviewChannel)
class InterviewChannelAdmin(object):
    list_display = ('interview_channel_name', 'interview_channel_coding', 'interview_channel_status'
                    )

@xadmin.sites.register(InterviewRecord)
class InterviewChannelAdmin(object):
    list_display = ('interview_date', 'interview_date_time', 'interview_position', 'interview_channel',
                    'interviewee_name', 'interviewer', 'interview_type', 'interview_result'
                    )
    ordering = ('interview_date', )
    list_filter = ('interview_position__belong_company', 'interviewer__interviewer_name',
                   'interview_position__position_name',
                   'interview_date', 'interview_date_time', 'interview_channel',
                   'interview_type', 'interview_result',
                   )

class GlobalSetting(object):
    # 设置base_site.html的Title
    site_title = '面试者信息'
    # 设置base_site.html的Footer
    site_footer = '面试者信息'

@xadmin.sites.register(views.BaseAdminView)
class BaseSetting(object):
    """
    # 创建xadmin的最基本管理器配置，并与view绑定
    """
    enable_themes = True
    use_bootswatch = True


xadmin.site.register(CommAdminView, GlobalSetting)
