from django.db import models
from django.urls import reverse

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=30, unique=False)
    number = models.IntegerField(primary_key=True, unique=True)
    frc_key = models.CharField(max_length=10, unique=True)

    robot_report = models.OneToOneField('Robot', null=True, on_delete=models.CASCADE, related_name='team')

    def __str__(self):
        return f"Team {self.number}: {self.name}"
    

class Robot(models.Model):
    NONE = 'None'
    LOW = 'Low Goal'
    HIGH = 'High Goal'
    BOTH = 'Both Goals'

    LOWBAR = 'Low Bar'
    MIDBAR = 'Mid Bar'
    HIGHBAR = 'High Bar'
    TRAVERSE = 'Traversal Bar'

    frc_team = models.OneToOneField(Team, related_name='robot', null=True, on_delete=models.CASCADE)

    tele_goal = ((LOW, 'Low'), (HIGH, 'High'), (BOTH, 'Both'), (NONE, 'None'))
    climb_level = ((LOWBAR, 'Low Bar'), (MIDBAR, 'Middle Bar'), (HIGHBAR, 'High Bar'), (TRAVERSE, 'Traversal Bar'), (NONE, 'No Climb'))

    # auto points (int field)
    auto_points = models.IntegerField(default=0)

    # drive train type
    drive_type = models.CharField(max_length=45)
    # goal (low/high/both)
    target = models.CharField(choices=tele_goal, max_length=11)

    # climb bar (none, low, mid, high, traverse)
    climb = models.CharField(choices=climb_level, max_length=13)

    def get_absolute_url(self):
        return reverse('scout:team_summary', kwargs={'number': self.frc_team.number})
    
    def __str__(self):
        return f"Expected Auto Score: {self.auto_points}, Drive Train: {self.drive_type}, Preferred Target: {self.target}, Climb Height: {self.climb}"


class MatchResult(models.Model):
    NONE = 'None'
    
    AUTOLOW = 'Low Goal'
    AUTOHIGH = 'High Goal'

    TELELOW = 'Low Goal'
    TELEHIGH = 'High Goal'
    TELECLOSE = 'Close'
    TELEFAR = 'Far'
    TELEANYWHERE = 'Anywhere'

    CLIMBLOW = 'Low Bar'
    CLIMBMID = 'Mid Bar'
    CLIMBHIGH = 'High Bar'
    TRAVERSE = 'Traversal Bar'

    ONE = 'Really Bad'
    TWO = 'Bad'
    THREE = 'Moderate'
    FOUR = 'Good'
    FIVE = 'Really Good'
    
    auto_target_field = ((AUTOHIGH, 'High Goal'), (AUTOLOW, 'Low Goal'), (NONE, 'No Auto'))
    tele_target_field = ((TELEHIGH, 'High Goal'), (TELELOW, 'Low Goal'), (NONE, 'No Teleop Shooting'))
    tele_distance_field = ((TELECLOSE, 'Inside Tarmac Only'), (TELEFAR, 'Outside Tarmac Only'), (TELEANYWHERE, 'Anywhere'), (NONE, 'N/A'))
    climb_height_field = ((CLIMBLOW, 'Low Bar'), (CLIMBMID, 'Mid Bar'), (CLIMBHIGH, 'High Bar'), (TRAVERSE, 'Traversal Bar'), (NONE, 'No Climb'))
    driver_rating_field = ((ONE, 'Really Bad'), (TWO, 'Bad'), (THREE, 'Moderate'), (FOUR, 'Good'), (FIVE, 'Really Good'))

    frc_team = models.ForeignKey(Team, related_name='matches', null=True , on_delete=models.CASCADE)

    match_number = models.IntegerField(default=0)
    # Auto taxi (T/F)
    auto_taxi = models.BooleanField(default=False)
    # Auto ball count (int field)
    auto_ball = models.IntegerField(default=0, max_length=1)
    # Auto target (high/low/none)
    auto_target = models.CharField(choices=auto_target_field, default=NONE, max_length=13)
    
    # Teleop target (high/low/both/none)
    tele_target = models.CharField(choices=tele_target_field, default=NONE, max_length=13)
    # Teleop cargo count (int field)
    tele_cargo = models.IntegerField(default=0, max_length=2)
    # Teleop shot distances (close only, far only, anywhere, no shooting)
    tele_distance = models.CharField(choices=tele_distance_field, default=NONE, max_length=13)

    # Climb location (low, mid, high, traverse, none)
    climb_height = models.CharField(choices=climb_height_field, default=NONE, max_length=13)
    # climb time (int field)
    climb_time = models.IntegerField(default=0, max_length=2)

    # Driver skill rating (1 - 5)
    driver_rating = models.CharField(choices=driver_rating_field, default=ONE, max_length=13)
    # Addtitonal Comments
    comments = models.CharField(max_length=250, default='No comments')

    def get_absolute_url(self):
        return reverse('scout:team_summary', kwargs={'number': self.frc_team.number})