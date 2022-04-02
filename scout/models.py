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
    NONE = 0
    LOW = 1
    HIGH = 2
    BOTH = 3

    LOWBAR = 4
    MIDBAR = 6
    HIGHBAR = 10
    TRAVERSE = 15

    frc_team = models.OneToOneField(Team, related_name='robot',null=False, on_delete=models.CASCADE)

    tele_goal = ((LOW, 'Low'), (HIGH, 'High'), (BOTH, 'Both'), (NONE, 'None'))
    climb_level = ((LOWBAR, 'Low Bar'), (MIDBAR, 'Middle Bar'), (HIGHBAR, 'High Bar'), (TRAVERSE, 'Traversal Bar'), (NONE, 'No Climb'))

    # auto points (int field)
    auto_points = models.IntegerField(default=0)

    # drive train type
    drive_type = models.CharField(max_length=45)
    # goal (low/high/both)
    target = models.PositiveSmallIntegerField(choices=tele_goal)

    # climb bar (none, low, mid, high, traverse)
    climb = models.PositiveSmallIntegerField(choices=climb_level)

    def get_absolute_url(self):
        return reverse('scout:team_summary', kwargs={'number': self.frc_team.number})
    
    def __str__(self):
        return f"{self.frc_team}"


class MatchResult(models.Model):
    NONE = 0
    
    AUTOLOW = 2
    AUTOHIGH = 4

    TELELOW = 1
    TELEHIGH = 2
    TELECLOSE = 1
    TELEFAR = 2
    TELEANYWHERE = 3

    CLIMBLOW = 4
    CLIMBMID = 6
    CLIMBHIGH = 10
    TRAVERSE = 15

    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    
    auto_target_field = ((AUTOHIGH, 'High Goal'), (AUTOLOW, 'Low Goal'), (NONE, 'No Auto'))
    tele_target_field = ((TELEHIGH, 'High Goal'), (TELELOW, 'Low Goal'), (NONE, 'No Teleop Shooting'))
    tele_distance_field = ((TELECLOSE, 'Inside Tarmac Only'), (TELEFAR, 'Outside Tarmac Only'), (TELEANYWHERE, 'Anywhere'), (NONE, 'N/A'))
    climb_height_field = ((CLIMBLOW, 'Low Bar'), (CLIMBMID, 'Mid Bar'), (CLIMBHIGH, 'High Bar'), (TRAVERSE, 'Traversal Bar'), (NONE, 'No Climb'))
    driver_rating_field = ((ONE, 'Really Bad'), (TWO, 'Bad'), (THREE, 'Moderate'), (FOUR, 'Good'), (FIVE, 'Really Good'))

    frc_team = models.ForeignKey(Team, related_name='matches',null=True , on_delete=models.CASCADE)

    # Auto taxi (T/F)
    auto_taxi = models.BooleanField(default=False)
    # Auto ball count (int field)
    auto_ball = models.IntegerField(default=0, max_length=1)
    # Auto target (high/low/none)
    auto_target = models.SmallIntegerField(choices=auto_target_field, default=NONE)
    
    # Teleop target (high/low/both/none)
    tele_target = models.SmallIntegerField(choices=tele_target_field, default=NONE)
    # Teleop cargo count (int field)
    tele_cargo = models.IntegerField(default=0, max_length=2)
    # Teleop shot distances (close only, far only, anywhere, no shooting)
    tele_distance = models.SmallIntegerField(choices=tele_distance_field, default=NONE)

    # Climb location (low, mid, high, traverse, none)
    climb_height = models.SmallIntegerField(choices=climb_height_field, default=NONE)
    # climb time (int field)
    climb_time = models.IntegerField(default=0, max_length=2)

    # Driver skill rating (1 - 5)
    driver_rating = models.SmallIntegerField(choices=driver_rating_field, default=ONE)
    # Addtitonal Comments
    comments = models.CharField(max_length=250)