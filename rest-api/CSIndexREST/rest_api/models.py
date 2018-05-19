from django.db import models


class Area(models.Model):
    name = models.CharField(max_length=200)
    researcher_file = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)


class Conference(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return '{0} - {1}'.format(self.area, self.name)


class Department(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)


class Researcher(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    pid = models.CharField(max_length=200)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.name, self.department, self.pid)


class Paper(models.Model):
    year = models.CharField(max_length=4)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    authors = models.CharField(max_length=500)
    url = models.CharField(max_length=200)
    researcher = models.ForeignKey(Researcher, on_delete=models.CASCADE)

    def __str__(self):
        return '{0} - {1} - {2} - {3} - {4}'.format(self.year, self.conference, self.title, self.researcher, self.url)
