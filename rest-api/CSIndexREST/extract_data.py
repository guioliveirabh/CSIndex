import csv
import pathlib

from rest_api.models import Area, Conference, Department, Researcher, Paper, Score


class DataExtractor:
    AREAS_FILE = 'research-areas-config.csv'
    CONFERENCES_FILE = '{0}-out-confs.csv'
    PAPERS_FILE = 'profs/search/{0}.csv'
    DEPARTMENTS_FILE = '{0}-out-scores.csv'

    def __init__(self, data_dir: pathlib.Path):
        self.data_dir = data_dir

    def run(self):
        self.extract_areas()
        self.extract_conferences()
        self.extract_departments()
        self.extract_researchers()
        self.extract_papers()
        self.extract_department_scores()

        print(list(Area.objects.all()))
        print(len(Conference.objects.all()))
        print(len(Department.objects.all()))
        print(len(Researcher.objects.all()))
        print(len(Paper.objects.all()))
        print(len(Score.objects.all()))

    def extract_areas(self):
        with open(self.data_dir / self.AREAS_FILE) as csv_file:
            reader = csv.reader(csv_file)
            areas = [Area(name=row[0], researcher_file=row[1]) for row in reader]
            Area.objects.bulk_create(areas)

    def extract_conferences(self):
        for area in Area.objects.all():
            with open(self.data_dir / self.CONFERENCES_FILE.format(area.name)) as csv_file:
                reader = csv.reader(csv_file)
                conferences = [Conference(area=area, name=row[0]) for row in reader]
                Conference.objects.bulk_create(conferences)

    def extract_departments(self):
        department_names = set()
        for area in Area.objects.all():
            with open(self.data_dir / area.researcher_file) as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    department_names.add(row[1])
        departments = [Department(name=name) for name in department_names]
        Department.objects.bulk_create(departments)

    def extract_researchers(self):
        departments = {department.name: department for department in Department.objects.all()}
        department_names = departments.keys()
        researchers = []
        researchers_set = set()

        for area in Area.objects.all():
            with open(self.data_dir / area.researcher_file) as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    if row[1] not in department_names:
                        continue

                    if row[2] in researchers_set:
                        continue

                    researchers.append(Researcher(name=row[0], department=departments[row[1]], pid=row[2]))
                    researchers_set.add(row[2])
        Researcher.objects.bulk_create(researchers)

    def extract_papers(self):
        conferences = {conference.name: conference for conference in Conference.objects.all()}
        conference_names = conferences.keys()
        papers = []

        for researcher in Researcher.objects.all():
            file_name = self.data_dir / self.PAPERS_FILE.format(researcher.name.replace(' ', '-'))
            if not file_name.is_file():
                continue

            with open(file_name) as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    if row[1] not in conference_names:
                        continue

                    papers.append(Paper(year=row[0], conference=conferences[row[1]], title=row[2],
                                        authors=row[3], url=row[4], researcher=researcher))
        Paper.objects.bulk_create(papers)

    def extract_department_scores(self):
        departments = {department.name: department for department in Department.objects.all()}
        department_names = departments.keys()
        scores = []

        for area in Area.objects.all():
            with open(self.data_dir / self.DEPARTMENTS_FILE.format(area.name)) as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    if row[0] not in department_names:
                        print(row)
                        continue

                    scores.append(Score(area=area, department=departments[row[0]], score=float(row[1])))
            Score.objects.bulk_create(scores)
