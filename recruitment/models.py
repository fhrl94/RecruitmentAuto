from django.core.validators import RegexValidator
from django.db import models

# Create your models here.

class IntervieweeInformation(models.Model):

    interviewee_name = models.CharField(verbose_name='面试者姓名', max_length=10)
    interviewee_gender = models.CharField(verbose_name='面试者性别', max_length=2)
    interviewee_tel = models.CharField(verbose_name='面试者手机号码', max_length=11, validators=[RegexValidator(r'^[\d]{11}')])
    interview_position = models.CharField(verbose_name='应聘岗位', max_length=30)
    interview_date = models.DateField(verbose_name='面试预约日期')
    interview_time_slot = models.TimeField(verbose_name='邀约面试时间点', blank=True, null=True, )
    invitation_situation = models.CharField(verbose_name='邀约情况', max_length=100, blank=True, null=True, )
    interview_channel = models.CharField(verbose_name='应聘渠道', max_length=10)
    internal_recommended = models.CharField(verbose_name='内部推荐人', max_length=10, blank=True, null=True, )
    company = models.CharField(verbose_name='岗位所属公司名称', max_length=20)
    position_charge_name = models.CharField(verbose_name='应聘岗位负责人称呼', max_length=10)
    position_charge_tel = models.CharField(verbose_name='应聘岗位负责人电话', max_length=11)

    def __str__(self):
        return self.interviewee_name

    class Meta:
        verbose_name = '电话通知表'
        verbose_name_plural = verbose_name
        unique_together = ('interviewee_tel', 'interview_position')


class InterviewResult(models.Model):
    interview_date = models.DateField(verbose_name='面试日期', )
    interview_date_time = models.CharField(verbose_name='面试时间(上午/下午)', choices=(('0', '上午'), ('1', '下午')),
                                           max_length=2)
    interview_position = models.CharField(verbose_name='应聘岗位', max_length=30)
    company = models.CharField(verbose_name='岗位所属公司名称', max_length=20)
    interview_channel = models.CharField(verbose_name='应聘渠道', max_length=10)
    internal_recommended = models.CharField(verbose_name='内部推荐人', max_length=10, blank=True, null=True, )
    interviewee_name = models.CharField(verbose_name='面试者姓名', max_length=10)
    interviewee_gender = models.CharField(verbose_name='面试者性别', max_length=2)
    interviewee_tel = models.CharField(verbose_name='面试者手机号码', max_length=11, validators=[RegexValidator(r'^[\d]{11}')])
    graduation_status = models.BooleanField(verbose_name='是否毕业', )
    interviewer_first = models.CharField(verbose_name='初试官', max_length=10, blank=True, null=True, )
    interview_first_grade = models.IntegerField(verbose_name='初试评分', blank=True, null=True, )
    interview_first_elimination = models.CharField(verbose_name='初试淘汰原因', max_length=100, blank=True, null=True, )
    interviewer_second = models.CharField(verbose_name='复试官', max_length=10, blank=True, null=True, )
    interview_second_grade = models.IntegerField(verbose_name='复试评分', blank=True, null=True, )
    interview_second_elimination = models.CharField(verbose_name='复试淘汰原因', max_length=100, blank=True, null=True, )
    interview_second_result = models.CharField(verbose_name='面试结果', max_length=20)

    def __str__(self):
        return self.interview_second_result

    class Meta:
        verbose_name = '面试汇总表'
        verbose_name_plural = verbose_name
        unique_together = ('interviewee_tel', 'interview_position')

class IntervieweeEnterInformation(models.Model):
    interviewee_enter_date = models.DateField(verbose_name='入职日期')
    interviewee_name = models.CharField(verbose_name='面试者姓名', max_length=10)
    company = models.CharField(verbose_name='岗位所属公司名称', max_length=20)
    interview_channel = models.CharField(verbose_name='应聘渠道', max_length=10)
    internal_recommended = models.CharField(verbose_name='内部推荐人', max_length=10, blank=True, null=True, )
    interviewee_department = models.CharField(verbose_name='部门', max_length=30, )
    interviewee_group = models.CharField(verbose_name='组别', max_length=30,)
    interviewee_gender = models.CharField(verbose_name='面试者性别', max_length=2)
    interview_position = models.CharField(verbose_name='应聘岗位', max_length=30)
    graduation_status = models.BooleanField(verbose_name='是否毕业', )
    interviewee_tel = models.CharField(verbose_name='面试者手机号码', max_length=11, validators=[RegexValidator(r'^[\d]{11}')])
    invitation_situation = models.CharField(verbose_name='备注', max_length=100, blank=True, null=True, )
    position_charge_name = models.CharField(verbose_name='应聘岗位负责人称呼', max_length=10)
    position_charge_tel = models.CharField(verbose_name='应聘岗位负责人电话', max_length=11)

    def __str__(self):
        return self.interviewee_name

    class Meta:
        verbose_name = '待入职员工信息'
        verbose_name_plural = verbose_name
        unique_together = ('interviewee_enter_date', 'interviewee_tel', 'interview_position')
