import requests
from bs4 import BeautifulSoup
import argparse


def scrape_jobs(location=None):
    if location:
        URL = (
            f"https://www.monster.com/jobs/search/"
            f"?q=Software-Developer&where={location}"
        )
    else:
        URL = "https://www.monster.com/jobs/search/?q=Software-Developer"
    page = requests.get(URL)

    bs = BeautifulSoup(page.content, "html.parser")
    results = bs.find(id="ResultsContainer")
    return results

def print_all_jobs(results):
    #Print details of jobs
    jobs = results.find_all("section", class_="card-content")

    for job in jobs:
        job_title = job.find("h2", class_="title")
        job_companyName = job.find("div", class_="company")
        job_location = job.find("div", class_="location")
        if None in (job_title, job_companyName, job_location):
            continue
        print("\033[1m" + job_title.text.strip() + "\033[0m")
        job_link = job_title.find("a")["href"]
        print(job_companyName.text.strip())
        print(job_location.text.strip())
        print("\033[4m" + f"Apply here: {job_link}\n" + "\033[0m")
        print()


# COMMAND-LINE INTERFACE
my_parser = argparse.ArgumentParser(
    prog="jobs", usage=f"\npython <filename.py> -l chicago | -l san+diego"
)
my_parser.add_argument(
    "-l", metavar="location", type=str, help="The location of the job"
)
args = my_parser.parse_args()
location = args.l

results = scrape_jobs(location)

print_all_jobs(results)