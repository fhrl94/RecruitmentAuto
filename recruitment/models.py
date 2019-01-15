from django.core.validators import RegexValidator
from django.db import models

# Create your models here.

gender_choices = (('0', '男'), ('1', '女'))
interview_date_time_choices = (('0', '上午'), ('1', '下午'))

class IntervieweeInformation(models.Model):

    interviewee_name = models.CharField(verbose_name='面试者姓名', max_length=10)
    interviewee_gender = models.CharField(verbose_name='面试者性别', max_length=2, choices=gender_choices,)
    interviewee_tel = models.CharField(verbose_name='面试者手机号码', max_length=11, validators=[RegexValidator(r'^[\d]{11}')])
    interview_channel = models.CharField(verbose_name='应聘渠道', max_length=10)
    internal_recommended = models.CharField(verbose_name='内部推荐人', max_length=10, blank=True, null=True, )
    company = models.CharField(verbose_name='岗位所属公司名称', max_length=20)
    interview_position = models.CharField(verbose_name='应聘岗位', max_length=30)
    interview_date = models.DateField(verbose_name='面试预约日期')
    interview_time_slot = models.TimeField(verbose_name='邀约面试时间点', blank=True, null=True, )
    invitation_situation = models.CharField(verbose_name='邀约情况', max_length=100, blank=True, null=True, )
    position_charge_name = models.CharField(verbose_name='电话邀约负责人称呼', max_length=10)
    position_charge_tel = models.CharField(verbose_name='电话邀约负责人电话', max_length=11)

    def __str__(self):
        return self.interviewee_name

    class Meta:
        verbose_name = '电话通知表'
        verbose_name_plural = verbose_name
        unique_together = ('interviewee_tel', 'interview_position')


class InterviewResult(models.Model):
    interview_date = models.DateField(verbose_name='面试日期', )
    interview_date_time = models.CharField(verbose_name='面试时间(上午/下午)', choices=interview_date_time_choices,
                                           max_length=2)
    company = models.CharField(verbose_name='岗位所属公司名称', max_length=20)
    interview_position = models.CharField(verbose_name='应聘岗位', max_length=30)
    interview_channel = models.CharField(verbose_name='应聘渠道', max_length=10)
    internal_recommended = models.CharField(verbose_name='内部推荐人', max_length=10, blank=True, null=True, )
    interviewee_name = models.CharField(verbose_name='面试者姓名', max_length=10)
    interviewee_gender = models.CharField(verbose_name='面试者性别', max_length=2, choices=gender_choices, )
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
    interviewee_gender = models.CharField(verbose_name='面试者性别', max_length=2, choices=gender_choices, )
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

class IntervieweeRecord(models.Model):
    """
    提取面试者信息
    """

    interviewee_name = models.CharField(verbose_name='面试者姓名', max_length=10)
    interviewee_gender = models.CharField(verbose_name='面试者性别', max_length=2, choices=gender_choices, )
    interviewee_tel = models.CharField(verbose_name='面试者手机号码', max_length=11, validators=[RegexValidator(r'^[\d]{11}')])
    graduation_status = models.BooleanField(verbose_name='是否毕业', null=True)

    def __str__(self):
        return self.interviewee_name

    class Meta:
        verbose_name = '面试者人员档案'
        verbose_name_plural = verbose_name
        unique_together = ('interviewee_name', 'interviewee_tel')

class Company(models.Model):
    company_name = models.CharField(verbose_name='公司名称', max_length=100, unique=True)
    company_coding = models.CharField(verbose_name='公司编码', max_length=20, unique=True, null=True)
    company_status = models.BooleanField(verbose_name='是否存在', )

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = '公司信息'
        verbose_name_plural = verbose_name

class PositionChargeInformation(models.Model):
    position_charge_name = models.CharField(verbose_name='应聘岗位负责人姓名', max_length=10, unique=True)
    position_charge_gender = models.CharField(verbose_name='岗位负责人性别', max_length=2, null=True, choices=gender_choices,)
    position_charge_tel = models.CharField(verbose_name='应聘岗位负责人电话', max_length=11, validators=[RegexValidator(r'^[\d]{11}')])
    position_charge_email = models.EmailField(verbose_name='应聘岗位负责人邮箱', null=True)
    position_charge_status = models.BooleanField(verbose_name='是否在职', )

    def __str__(self):
        return self.position_charge_name

    class Meta:
        verbose_name = '招聘负责人信息'
        verbose_name_plural = verbose_name


class Position(models.Model):
    belong_company = models.ForeignKey(Company, verbose_name='所属公司',
                                       on_delete=models.PROTECT, limit_choices_to={'company_status': True})
    position_name = models.CharField(verbose_name='应聘岗位名称', max_length=100)
    position_coding = models.CharField(verbose_name='应聘岗位编码', max_length=10, unique=True, null=True)
    # belong_position_charge = models.ForeignKey(PositionChargeInformation, verbose_name='所属负责人',
    #                                            to_field='position_charge_name', on_delete=models.PROTECT,
    #                                            limit_choices_to={'position_charge_status': True})
    position_status = models.BooleanField(verbose_name='应聘岗位是否启用', )

    def __str__(self):
        return self.position_name

    class Meta:
        verbose_name = '应聘岗位'
        verbose_name_plural = verbose_name
        unique_together = ('position_name', 'belong_company')


class InterviewChannel(models.Model):
    # TODO 分析渠道数据
    interview_channel_name = models.CharField(verbose_name='应聘渠道名称', max_length=100, unique=True)
    interview_channel_coding = models.CharField(verbose_name='应聘渠道编码', max_length=10, unique=True, null=True)
    interview_channel_status = models.BooleanField(verbose_name='是否使用', )

    def __str__(self):
        return self.interview_channel_name

    class Meta:
        verbose_name = '招聘渠道'
        verbose_name_plural = verbose_name


class Interviewer(models.Model):
    interviewer_name = models.CharField(verbose_name='面试官姓名', max_length=10)
    # #  面试官其他信息
    interviewer_status = models.BooleanField(verbose_name='是否在职')

    def __str__(self):
        return self.interviewer_name

    class Meta:
        verbose_name = '面试官档案'
        verbose_name_plural = verbose_name

class InterviewType(models.Model):
    interview_type = models.CharField(verbose_name='面试类型', max_length=20, unique=True)
    interview_type_coding = models.CharField(verbose_name='面试类型编码', max_length=10, unique=True)
    interview_type_status = models.BooleanField(verbose_name='是否使用')

    def __str__(self):
        return self.interview_type

    class Meta:
        verbose_name = '面试类型'
        verbose_name_plural = verbose_name


class InterviewRecord(models.Model):
    interview_date = models.DateField(verbose_name='面试日期', )
    interview_date_time = models.CharField(verbose_name='面试时间(上午/下午)', choices=interview_date_time_choices,
                                           max_length=2)
    interview_position = models.ForeignKey(Position, verbose_name='面试岗位', on_delete=models.PROTECT,
                                           limit_choices_to={'position_status': True},)
    interview_channel = models.ForeignKey(InterviewChannel, verbose_name='渠道', on_delete=models.PROTECT,
                                          limit_choices_to={'interview_channel_status': True},)
    interviewee_name = models.ForeignKey(IntervieweeRecord, verbose_name='面试者姓名', on_delete=models.CASCADE,)
    interviewer = models.ForeignKey(Interviewer, verbose_name='面试官', on_delete=models.PROTECT,
                                    limit_choices_to={'interviewer_status': True}, )
    interview_type = models.ForeignKey(InterviewType, verbose_name='面试类型', on_delete=models.PROTECT,
                                       limit_choices_to={'interview_type_status': True}, )
    interview_result = models.CharField(verbose_name='面试结果', max_length=20)
    # TODO 面试通过原因, 或未通过原因

    def __str__(self):
        return self.interview_result

    class Meta:
        verbose_name = '面试结果'
        verbose_name_plural = verbose_name
        unique_together = ('interview_date', 'interviewee_name', 'interview_position', 'interview_type')
