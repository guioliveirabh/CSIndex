from django.db import models


class Area(models.Model):
    name = models.CharField(max_length=10, db_index=True, unique=True)
    label = models.CharField(max_length=200)
    researcher_file = models.CharField(max_length=200)

    def __str__(self):
        return '{0} - {1}'.format(self.name, self.label)

    class Meta:
        ordering = ['name']


class Conference(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)

    def __str__(self):
        return '{0} - {1}'.format(self.area, self.name)

    class Meta:
        ordering = ['name']
        unique_together = ('area', 'name')


class Department(models.Model):
    name = models.CharField(max_length=200, db_index=True, unique=True)
    areas = models.ManyToManyField(Area, through='DepartmentScore')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Researcher(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    pid = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.name, self.department, self.pid)

    class Meta:
        ordering = ['name']


class Paper(models.Model):
    year = models.SmallIntegerField(db_index=True)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    authors = models.CharField(max_length=500)
    url = models.CharField(max_length=200, unique=True)
    researchers = models.ManyToManyField(Researcher)

    def __str__(self):
        return '{0} - {1} - {2} - {3} - {4}'.format(self.year, self.conference, self.title, self.researchers, self.url)

    class Meta:
        ordering = ['-year', 'title']


class DepartmentScore(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    value = models.FloatField()

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.department, self.area, self.value)

    class Meta:
        unique_together = ('area', 'department')
