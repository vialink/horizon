# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import iso8601

from django.template.defaultfilters import register  # noqa
from django.template.defaultfilters import timesince  # noqa
from django.utils.safestring import mark_safe  # noqa
from django.utils import timezone


@register.filter
def replace_underscores(string):
    return string.replace("_", " ")


@register.filter
def parse_isotime(timestr):
    """This duplicates oslo timeutils parse_isotime but with a
    @register.filter annotation.
    """
    try:
        return iso8601.parse_date(timestr)
    except iso8601.ParseError as e:
        raise ValueError(e.message)
    except TypeError as e:
        raise ValueError(e.message)


@register.filter
def timesince_sortable(dt):
    delta = timezone.now() - dt
    # timedelta.total_seconds() not supported on python < 2.7
    seconds = delta.seconds + (delta.days * 24 * 3600)
    return mark_safe("<span data-seconds=\"%d\">%s</span>" %
                     (seconds, timesince(dt)))
