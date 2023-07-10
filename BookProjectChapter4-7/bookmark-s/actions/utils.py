import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Action

# وظيفة الاختصار التي تسمح لك بإنشاء كائنات عمل جديدة بطريقة بسيطة
# تسمح لك الوظيفة create_action () بإنشاء إجراءات تتضمن اختياريًا كائنًا مستهدفًا.
# يمكنك استخدام هذه الوظيفة في أي مكان في التعليمات البرمجية الخاصة بك كاختصار لإضافة إجراءات جديدة إلى تدفق النشاط.

# لقد قمت بتغيير وظيفة create_action () لتجنب حفظ الإجراءات المكررة وإرجاع قيمة منطقية
def create_action(user, verb, target=None):
    # check for any similar action made in the last minute
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user_id=user.id, 
                                            verb=verb,
                                            created__gte=last_minute)
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct, target_id=target.id)
        
    if not similar_actions:
        # no existing actions found
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False