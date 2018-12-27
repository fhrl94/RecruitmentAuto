import xadmin
from xadmin import views
from xadmin.views import CommAdminView

from recruitment.models import IntervieweeInformation, InterviewResult, IntervieweeEnterInformation
from recruitment.resources import IntervieweeInformationResource, InterviewResultResource, \
    IntervieweeEnterInformationResource


@xadmin.sites.register(IntervieweeInformation)
class IntervieweeInformationAdmin(object):
    import_export_args = {'import_resource_class': IntervieweeInformationResource, }
    list_display = ('interviewee_name', 'interviewee_gender', 'interviewee_tel', 'interview_position', 'interview_date',
                    'interview_time_slot', 'interview_channel', 'internal_recommended', 'company',
                    'position_charge_name', 'position_charge_tel', 'invitation_situation', )
    search_fields = ['interviewee_name', 'interviewee_tel']
    list_filter = ['interview_date', 'interview_position', 'company', 'interviewee_gender', 'interview_time_slot',
                   'position_charge_name',
                   ]

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
