from django.db import models

class Violation(models.Model):
    student_name = models.CharField(max_length=100)
    violation_type = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.violation_type}"