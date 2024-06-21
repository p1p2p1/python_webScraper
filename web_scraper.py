import requests
from bs4 import BeautifulSoup

# url = "https://berlinstartupjobs.com/engineering/"

#회사 이름, 직무 제목, 설명 및 직무 링크 추출


class web_scraper:

    def __init__(self, headers):
        self.headers = headers

    #첫 번째 URL 스크랩핑
    #berlinstartupjobs.com
    def berlin_web_scrape(self, url, search, all_jobs):
        url = url + f"/skill-areas/{search}"
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, "html.parser")

        #None Exception Control
        if soup.find("ul", class_ = "jobs-list-items") is None:
            print("구인 정보를 포함한 목록을 찾을 수 없습니다.")
            return #예외 처리 페이지 설정 필요

        jobs = soup.find("ul",
                         class_="jobs-list-items").find_all("li",
                                                            class_="bjs-jlid")
        

        
        for job in jobs:
            #company name
            company = job.find("a", class_="bjs-jlid__b").text.strip()

            #hire title
            title = job.find("h4", class_="bjs-jlid__h").find("a").text.strip()

            #hire description
            description = job.find(
                "div", class_="bjs-jlid__description").text.strip()

            #hire url
            url = job.find("h4", class_="bjs-jlid__h").find("a")["href"]

            job_data = {
                "title": title,
                "company": company,
                "description": description,
                "url": url,
            }
            all_jobs.append(job_data)

   #두 번째 URL 스크랩핑
    #weworkremotely.com
    def wwr_web_scrape(self, url, search, all_jobs):
        url_search = url + f"/remote-jobs/search?utf8=%E2%9C%93&term={search}"
        response = requests.get(url_search, headers=self.headers)
        soup = BeautifulSoup(response.content, "html.parser")

        #None Exception Control
        if soup.find("section", class_ = "jobs") is None:
            print("구인 정보를 포함한 목록을 찾을 수 없습니다.")
            return #예외 처리 페이지 설정 필요

        jobs = soup.find("section", class_="jobs").find("article").find("ul").find_all("li")


        for job in jobs:
            company_list = job.find_all("a")
            if len(company_list) >= 2:
                #company name
                company_name = company_list[1].find("span", class_ = "company").text

                #hire title
                company_title = company_list[1].find("span", class_ = "title").text

                #hire description
                company_description = company_list[1].find_all("span", class_ = "company")[1].text
                company_description2 = company_list[1].find_all("span", class_ = "company")[2].text

                #hire url
                company_url = url + company_list[1]['href']

                job_data = {
                    "title": company_title,
                    "company": company_name,
                    "description": f"{company_description}, {company_description2}",
                    "url": company_url,
                }
                all_jobs.append(job_data)


   #세 번째 URL 스크랩핑
   #https://web3.career/java-jobs
    def web3_web_scrape(self, url, search, all_jobs):
        url_search = url + f"/?search={search}"
        response = requests.get(url_search, headers=self.headers)
        soup = BeautifulSoup(response.content, "html.parser")

        #None Exception Control
        if soup.find("tbody", class_ = "tbody") is None:
            print("구인 정보를 포함한 목록을 찾을 수 없습니다.")
            return #예외 처리 페이지 설정 필요

        jobs = soup.find("tbody", class_ = "tbody").find_all("tr")

        for job in jobs:
            #compnay information
            company = job.find_all("td")

            #company name
            company_name = company[1].find("h3")
            
            if company_name == None:
                continue
            else:
                company_name = company_name.text

            #hire title
            company_title = company[0].find("h2", class_ = "my-primary")

            if company_title == None:
                continue
            else:
                company_title = company_title.text

            #hire description
            ##location
            company_location = company[3].find("a")
            if company_location == None:
                continue
            else:
                company_location = company_location.text

            ##salary
            company_salary = company[4].find("p")
            if company_salary == None:
                continue
            else:
                company_salary = company_salary.text

            #hire url
            company_url = company[0].find("div", class_ = "d-flex").find("a")['href']

            job_data = {
                "title": company_title,
                "company": company_name,
                "description": f"{company_location}, {company_salary}",
                "url": url + company_url,
            }

            all_jobs.append(job_data)


