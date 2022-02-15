from apis.condition import Condition
from jobflows.models import IndividualConditions, IndividualKeys


class BaseLogic(Condition):
    def __init__(self, name):
        self.name = name

    def get_next_exec_no(self, user, detail, params):
        conditions = self.__get_individual_conditions(user.user_id, detail.id)
        next_execno = detail.next_execno
        for row in conditions:
            ret = getattr(self, row.condition.method)(detail, params)
            if ret:
                return row.next_execno
        return next_execno

    def __get_individual_conditions(self, user_id, detail_id):
        return (
            IndividualConditions.objects.all()
            .filter(user_id=user_id, flowdetail_id=detail_id)
            .order_by("priority")
        )

    def get_individual_keys(self, user_id, detail_id):
        return IndividualKeys.objects.all().filter(
            user_id=user_id, flowdetail_id=detail_id
        )
