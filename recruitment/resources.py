import datetime

import xlrd
from import_export import resources
from import_export.widgets import Widget, IntegerWidget, CharWidget

from recruitment.models import IntervieweeInformation, InterviewResult, IntervieweeEnterInformation


class BooleanWidgetCustom(Widget):
    """
    将<是/否>转为<True/False>
    """
    # TODO 待修改为通用
    TRUE_VALUES = ["1", 1, '是']
    FALSE_VALUE = ["0", '否']

    def render(self, value, obj=None):
        if value is None:
            return ""
        return self.TRUE_VALUES[2] if value else self.FALSE_VALUE[1]

    def clean(self, value, row=None, *args, **kwargs):
        if value == "":
            return None
        return True if value in self.TRUE_VALUES else False

class ChoicesWidgetCustom(Widget):
    """
    将数据中<choices>翻译为<人类语言>
    """
    choices = (('0', '上午'), ('1', '下午'))

    def __init__(self, choices=None):
        if choices:
            assert choices[0][0], "必须是 2 维元组"
            self.choices = choices
        self.interview_date_time_choices = [one for one in zip(*choices)]
        pass

    def render(self, value, obj=None):
        if value is None:
            return ""
        if value in self.interview_date_time_choices[0]:
            return self.interview_date_time_choices[1][self.interview_date_time_choices[0].index(value)]

    def clean(self, value, row=None, *args, **kwargs):
        if value == "":
            return None
        if value in self.interview_date_time_choices[1]:
            return self.interview_date_time_choices[0][self.interview_date_time_choices[1].index(value)]
        raise UserWarning("<{value}>格式错误".format(value=value))


class IntegerWidgetCustom(IntegerWidget):
    """
    用<str>存储<int>
    """
    def render(self, value, obj=None):
        return value

    def clean(self, value, row=None, *args, **kwargs):
        if self.is_empty(value):
            return None
        return str(int(float(value)))


class ExcelDateWidget(CharWidget):
    """
    Excel date widget.

        * ``date_mode``
    """

    def __init__(self, date_mode, *args, **kwargs):
        self.date_mode = date_mode
        super().__init__(*args, **kwargs)

    def render(self, value, obj=None):
        if value is None:
            return None
        return datetime.date.strftime(value, '%Y-%m-%d')

    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return None
        try:
            return datetime.datetime.strptime(value, '%Y-%m-%d').date()
        except (ValueError, TypeError, ):
            return datetime.date(*xlrd.xldate.xldate_as_tuple(value, self.date_mode)[:3])


class ExcelTimeWidget(Widget):
    """
    Excel date widget.

        * ``date_mode``
    """
    def __init__(self, date_mode, formats=None):
        self.date_mode = date_mode
        if formats is None:
            self.formats = ('%H:%M:%S',)
        else:
            self.formats = ('%H:%M:%S',) + formats

    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return None
        for format_ins in self.formats:
            try:
                return datetime.datetime.strptime(value, format_ins).time()
            except (ValueError, TypeError, ):
                continue
        return datetime.time(*xlrd.xldate.xldate_as_tuple(float(value), self.date_mode)[3:6])

    def render(self, value, obj=None):
        if not value:
            return ""
        return value.strftime(self.formats[0])


class IntervieweeInformationResource(resources.ModelResource):
    @classmethod
    def field_from_django_field(cls, field_name, django_field, readonly):
        """
        Returns a Resource Field instance for the given Django model field.
        """

        field = super().field_from_django_field(field_name, django_field, readonly)

        # Use the Django Field verbose name for the column name.
        field.column_name = django_field.verbose_name
        _widget = {
            'interviewee_tel': IntegerWidgetCustom(),
            'interview_date': ExcelDateWidget(date_mode=0),
            'position_charge_tel': IntegerWidgetCustom(),
            'interview_time_slot': ExcelTimeWidget(date_mode=0, formats=('%H:%M', )),
                   }
        if len(django_field.choices):
            field.widget = ChoicesWidgetCustom(choices=django_field.choices)
        if field_name in _widget.keys():
            field.widget = _widget[field_name]
        return field

    class Meta:
        model = IntervieweeInformation  # fields = ()  # exclude = ()
        exclude = ('id', )
        import_id_fields = ('interviewee_tel', 'interview_position')


class InterviewResultResource(resources.ModelResource):

    @classmethod
    def field_from_django_field(cls, field_name, django_field, readonly):
        """
        Returns a Resource Field instance for the given Django model field.
        """

        field = super().field_from_django_field(field_name, django_field, readonly)

        # Use the Django Field verbose name for the column name.
        field.column_name = django_field.verbose_name
        _widget = {
            'graduation_status': BooleanWidgetCustom(),
            'interviewee_tel': IntegerWidgetCustom(),
            'interview_date': ExcelDateWidget(date_mode=0),
                   }
        if len(django_field.choices):
            field.widget = ChoicesWidgetCustom(choices=django_field.choices)
        if field_name in _widget.keys():
            field.widget = _widget[field_name]
        return field

    class Meta:
        model = InterviewResult  # fields = ()  # exclude = ()
        report_skipped = False
        exclude = ('id', )
        import_id_fields = ('interview_date', 'interviewee_tel', 'interview_position')

class IntervieweeEnterInformationResource(resources.ModelResource):

    @classmethod
    def field_from_django_field(cls, field_name, django_field, readonly):
        """
        Returns a Resource Field instance for the given Django model field.
        """

        field = super().field_from_django_field(field_name, django_field, readonly)

        # Use the Django Field verbose name for the column name.
        field.column_name = django_field.verbose_name
        _widget = {
            'graduation_status': BooleanWidgetCustom(),
            'interviewee_tel': IntegerWidgetCustom(),
            'interviewee_enter_date': ExcelDateWidget(date_mode=0),
            'position_charge_tel': IntegerWidgetCustom(),
                   }
        if len(django_field.choices):
            field.widget = ChoicesWidgetCustom(choices=django_field.choices)
        if field_name in _widget.keys():
            field.widget = _widget[field_name]
        return field

    class Meta:
        model = IntervieweeEnterInformation  # fields = ()  # exclude = ()
        skip_unchanged = True
        report_skipped = False
        exclude = ('id', )
        import_id_fields = ('interviewee_enter_date', 'interviewee_tel', 'interview_position')
