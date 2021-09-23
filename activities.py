import inspect
import sys

from exceptions import InvalidActivityError

activities = {}

def register_activity(activity):
    if not getattr(activity, 'type', None):
        raise InvalidActivityError('Activity is missing `type` attribute')
    if activity.type in activities.keys():
        raise InvalidActivityError('Activity type `{}` is already registered'.format(activity.code))

    activities[activity.type] = activity


class Activity:
    def __init__(self, activity_data):
        self.activity_data = activity_data

    def get_embed(self):
        sorted_activity_data_keys = sorted(self.activity_data.keys())
        fields = []
        for key in sorted_activity_data_keys:
            fields.append({
                'name': key,
                'value': self.activity_data[key],
                'inline': False
            })
        return {'fields': fields}
    
    def get_embeds(self):
        return [self.get_embed()]

    
    def get_request_body(self):
        return {'embeds': self.get_embeds()}



class_members = inspect.getmembers(sys.modules[__name__], inspect.isclass)
for name, klass in class_members:
    if issubclass(klass, Activity) and klass != Activity:
        register_activity(klass)

def get_activity(activity_data):
    return activities.get(activity_data.get('Type'), Activity)(activity_data)