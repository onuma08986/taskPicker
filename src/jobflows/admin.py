from django.contrib import admin
from .models import (
    Service,
    Authenticate,
    Action,
    Condition,
    Key,
    ActionKey,
    ActionCondition,
    Schedule,
    Flow,
    FlowDetail,
    IndividualKeys,
    IndividualConditions,
)

admin.site.register(Service)
admin.site.register(Authenticate)
admin.site.register(Action)
admin.site.register(Condition)
admin.site.register(Key)
admin.site.register(ActionKey)
admin.site.register(ActionCondition)
admin.site.register(Schedule)
admin.site.register(Flow)
admin.site.register(FlowDetail)
admin.site.register(IndividualKeys)
admin.site.register(IndividualConditions)
