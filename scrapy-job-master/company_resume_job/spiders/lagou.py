import time
from urllib import parse
import requests
import scrapy
from bs4 import BeautifulSoup
from scrapy_redis.spiders import RedisSpider

from company_resume_job.items import JobItem


class JobSpider(RedisSpider):
    name = 'lagou'
    allowed_domains = ['lagou.com']

    city = parse.quote('全国')
    salary = ''
    kds = ['java', r'python', r'产品经理', r'技术经理']

    def get_ref_url(self, kd, salary, city):
        return 'https://www.lagou.com/jobs/list_{}?px=new&yx={}&city={}#order&cl=false&fromSearch=true' \
               '&labelWords=&suginput='.format(parse.quote(kd), salary, city)

    def get_headers(self, ref_url):
        my_headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/72.0.3626.119 Safari/537.36",
            "Referer": ref_url,
            "Content-Type": "application/x-www-form-urlencoded;charset = UTF-8"
        }
        return my_headers

    def start_requests(self):
        yield scrapy.Request(url="https://www.lagou.com", callback=self.parse, dont_filter=True)

    def parse(self, response, **kwargs):
        x = 0
        while True:
            x = x + 1
            for kd in self.kds:
                job_list = self.parse_page(kd, x)
                if not job_list:
                    continue

                for job in job_list:
                    yield job
        # print('end')

    def parse_page(self, kd, page):

        url = 'https://www.lagou.com/jobs/positionAjax.json?px=new&needAddtionalResult=false'
        data = {
            'first': 'false',
            'pn': page,
            'kd': kd,
            'sid': ''
        }
        try:
            job_list = self.get_json(url, data)
            # print("第%s页正常采集 %s" % (page, parse.unquote(kd)))
            return job_list
        except Exception as msg:
            # print("第%s页出现问题 %s , error: %s" % (page, parse.unquote(kd), msg))
            pass

    def get_json(self, url, data):

        time.sleep(5)
        ses = requests.session()  # 获取session
        ref_url = self.get_ref_url(data['kd'], self.salary, self.city)
        ses.headers.update(self.get_headers(ref_url))  # 更新
        ses.get(ref_url)
        content = ses.post(url=url, data=data)
        result = content.json()
        info = result['content']['positionResult']['result']
        show_id = result['content']['showId']
        info_list = []
        for job in info:
            job_url = 'https://www.lagou.com/jobs/{}.html'.format(job["positionId"])

            try:
                info = self.parse_job(job, ses, show_id)
                info_list.append(info)
            except Exception as msg:
                # print("job 采集失败 %s -> %s" % (job_url, msg))
                pass

        return info_list

    def parse_job(self, re, session, show_id):
        job = JobItem()
        # job id
        job['id'] = re["positionId"]
        # job website
        job['website'] = self.name
        # job time
        job['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # job url
        job['url'] = 'https://www.lagou.com/jobs/{}.html?show={}'.format(re["positionId"], show_id)

        # 职位名称
        job['name'] = re["positionName"]
        # 公司名称
        job['co_name'] = re['companyFullName']
        # 区域
        job['area'] = re['district']
        # 工资
        job['salary'] = re['salary'].replace('k', '') + '千/月'
        job['exp'] = re['workYear']
        job['edu'] = re['education']
        job['num'] = "招1人"

        job['pub_time'] = re['createTime'].split('-', 1)[1].split(' ')[0]
        job['otherq'] = re['formatCreateTime']
        # 福利
        job['welfare'] = re['positionAdvantage']

        # 上班地址
        if re['businessZones'] is not None and len(re['businessZones']) > 0:
            job['local'] = ' '.join(re['businessZones'])

        # 公司类型
        job['co_type'] = re['financeStage']
        # 公司行业
        job['co_trade'] = re['industryField']

        time.sleep(1)
        html_doc = session.get(job['url'])
        soup = BeautifulSoup(html_doc.text, 'html.parser', from_encoding='utf-8')

        job_info = soup.find_all('div', class_='job-detail')
        if job_info and len(job_info) > 0:
            # 职位信息
            job['info'] = job_info[0].get_text().strip()


        job_local = soup.find('div', class_='work_addr')
        if job_local and len(job_local) > 0:
            job['local'] = job_local.text.replace(' ', '').replace('\n', '').replace('查看地图', '')

        job_home = soup.find_all('i', class_='icon-glyph-home')
        if job_home and len(job_home) > 0:
            # 公司网址
            href = job_home[0].parent.find('a')
            if href:
                job['co_url'] = href.attrs['href']

        return job
