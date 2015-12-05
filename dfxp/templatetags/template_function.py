# -*- coding: utf-8 -*-
from django.template import Library
from django.contrib.humanize.templatetags.humanize import intcomma
from datetime import date, timedelta
import pytz
register = Library()

@register.filter
def is_false(arg):
    return arg is False


@register.filter
def comma(arg):
    return "%s" % intcomma(arg)


@register.filter
def none_check(arg):
    if arg is None:
        return ""
    else:
        return arg


@register.filter
def status(arg):
    if arg == "000":
        return "발급"
    elif arg == "001":
        return "사용"
    else:
        return "취소"


@register.filter
def location_none_check(arg):
    if arg is None:
        return "%s" % "선택안함"
    else:
        return arg


@register.filter
def none_check(arg):
    if arg is None:
        return "%s" % "선택안함"
    else:
        return arg


@register.filter
def is_past_due(self):
    if date.today() > self.date:
        return True
    return False


@register.filter
def user_status(arg):
    if arg is True:
        return "%s" % "가입"
    else:
        return "%s" % "탈퇴"


@register.filter
def check_point(var, args):
    if args is False:
        return "%s" % "+"+str(var)
    else:
        return "%s" % "-"+str(var)


@register.filter
def date_format(arg):
    return "%s" % arg.strftime("%Y/%m/%d %H:%M")

@register.filter
def user_list_date_format(arg):
    # arg = arg + timedelta(hours=8) + timedelta(minutes=30)
    arg = arg + timedelta(hours=9)
    return "%s" % arg.strftime("%Y/%m/%d %H:%M")


@register.filter
def date_format_add_time(arg):
    # arg = arg + timedelta(hours=8) + timedelta(minutes=30)
    # return "%s" % arg.strftime("%Y/%m/%d %H:%M")
    print arg



@register.filter
def coupon_status(var, arg):
    if arg == "000":
        return "발급"
    elif arg == "001":
        return "사용"
    else:
        return "취소"

@register.filter
def paginator_index(var, arg):
    return var+((arg-1)*15)

@register.filter
def query_date_format(arg):
    return "%s" % arg.strftime("%Y-%m-%d")


@register.filter
def subtract(value, arg):
    return value - arg


@register.filter
def coupon_title_check(value, arg):
    if arg.find(value) >= 0:
        return arg
    else:
        return value+" "+arg

