from django.db import models
from datetime import datetime

class ReportPost(models.Model):
    last_updated = models.TextField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    responsible_team = models.TextField(default="OTHER")
    issue_number = models.TextField(unique=True,default="N/A")
    job_type = models.TextField(default="N/A")
    build_type = models.TextField(default="N/A")
    failed_at = models.TextField(default="N/A")
    status = models.TextField(default="N/A")
    reported_by = models.TextField(default="N/A")
    reported_to = models.TextField(default="N/A")
    priority = models.TextField(default="N/A")
    final_comment = models.TextField(default="N/A")
    reason = models.TextField(unique=True,default="N/A")
    solution = models.TextField(default="Not Yet Solved")


