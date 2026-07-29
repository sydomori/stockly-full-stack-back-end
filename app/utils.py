from app.extensions import db
from app.models.Activity_log import ActivityLog

# create activity log helper function to create activity logs
#every route calls log_activity with its own details
def log_activity(user_id, action, details, product_id=None):
    log = ActivityLog(
        user_id=user_id,
        action=action,
        details=details,
        product_id=product_id
    )
    db.session.add(log)
    db.session.commit()