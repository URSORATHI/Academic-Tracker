# -*- coding: utf-8 -*-

from import_export import resources
from accounts.models import attendance

class attendanceResource(resources.ModelResource):
    class Meta:
        model = attendance