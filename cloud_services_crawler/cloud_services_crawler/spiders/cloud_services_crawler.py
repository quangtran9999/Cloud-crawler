import scrapy
from urllib.parse import urljoin
from cloud_services_crawler.items import CloudServiceItem, ServiceReviewItem
from scrapy_selenium import SeleniumRequest
import time

class CloudServicesSpider(scrapy.Spider):
    name = "cloud_services"
    allowed_domains = [
        'aws.amazon.com',
        'cloud.google.com',
        'azure.microsoft.com',
        'gartner.com'
    ]
    start_urls = [
        # AWS Cloud Storage Services
        'https://aws.amazon.com/products/storage/',
        # Google Cloud Storage Services
        'https://cloud.google.com/products/storage',
        # Microsoft Azure Storage Services
        'https://azure.microsoft.com/en-us/products/storage/',
        # Gartner Strategic Cloud Platform Services
        'https://www.gartner.com/reviews/market/strategic-cloud-platform-services'
    ]

    def start_requests(self):
        for url in self.start_urls:
            if 'gartner.com' in url:
                yield SeleniumRequest(url=url, callback=self.parse_gartner, wait_time=10)
            else:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if 'aws.amazon.com' in response.url:
            yield from self.parse_aws(response)
        elif 'cloud.google.com' in response.url:
            yield from self.parse_gcp(response)
        elif 'azure.microsoft.com' in response.url:
            yield from self.parse_azure(response)

    ## AWS Parsing
    def parse_aws(self, response):
        # Cập nhật selector theo cấu trúc thực tế của trang AWS
        services = response.css('div.lbS-v4Z')  # Ví dụ selector, hãy kiểm tra lại
        for svc in services:
            service_name = svc.css('h3::text').get()
            if service_name:
                service_name = service_name.strip()
                detail_url = svc.css('a::attr(href)').get()
                if detail_url:
                    detail_url = urljoin(response.url, detail_url)
                    yield scrapy.Request(detail_url, callback=self.parse_aws_service_detail, meta={'provider': 'Amazon Web Services', 'service_name': service_name})

    def parse_aws_service_detail(self, response):
        item = CloudServiceItem()
        item['provider'] = response.meta['provider']
        item['service_name'] = response.meta['service_name']
        item['category'] = 'Storage'  # Vì chúng ta chỉ thu thập dịch vụ lưu trữ
        item['description'] = response.css('div.lbS-v4Z p::text').get(default='').strip()
        features = response.css('ul.feature-list li::text').getall()
        item['features'] = [feature.strip() for feature in features]
        price_info = response.css('div.pricing-info::text').getall()
        item['price_info'] = ' '.join(price_info).strip()
        item['official_page'] = response.url

        # Tạo URL để tìm kiếm trên Gartner (Nếu cần thiết)
        search_query = '+'.join(item['service_name'].split())
        gartner_search_url = f"https://www.gartner.com/reviews/search/products?query={search_query}&category=Strategic+Cloud+Platform+Services"
        item['gartner_reviews_url'] = gartner_search_url

        yield item

        # Lấy review từ Gartner
        yield SeleniumRequest(url=gartner_search_url, callback=self.parse_gartner_reviews, meta={'service_name': item['service_name']}, wait_time=10)

    ## Google Cloud Parsing
    def parse_gcp(self, response):
        # Cập nhật selector theo cấu trúc thực tế của trang GCP
        services = response.css('div.devsite-article')  # Ví dụ selector, hãy kiểm tra lại
        for svc in services:
            service_name = svc.css('h3::text').get()
            if service_name:
                service_name = service_name.strip()
                detail_url = svc.css('a::attr(href)').get()
                if detail_url:
                    detail_url = urljoin(response.url, detail_url)
                    yield scrapy.Request(detail_url, callback=self.parse_gcp_service_detail, meta={'provider': 'Google Cloud', 'service_name': service_name})

    def parse_gcp_service_detail(self, response):
        item = CloudServiceItem()
        item['provider'] = response.meta['provider']
        item['service_name'] = response.meta['service_name']
        item['category'] = 'Storage'
        item['description'] = response.css('div.devsite-article-body p::text').get(default='').strip()
        features = response.css('ul.feature-list li::text').getall()
        item['features'] = [feature.strip() for feature in features]
        price_info = response.css('div.pricing-info::text').getall()
        item['price_info'] = ' '.join(price_info).strip()
        item['official_page'] = response.url

        # Tạo URL để tìm kiếm trên Gartner (Nếu cần thiết)
        search_query = '+'.join(item['service_name'].split())
        gartner_search_url = f"https://www.gartner.com/reviews/search/products?query={search_query}&category=Strategic+Cloud+Platform+Services"
        item['gartner_reviews_url'] = gartner_search_url

        yield item

        # Lấy review từ Gartner
        yield SeleniumRequest(url=gartner_search_url, callback=self.parse_gartner_reviews, meta={'service_name': item['service_name']}, wait_time=10)

    ## Azure Parsing
    def parse_azure(self, response):
        # Cập nhật selector theo cấu trúc thực tế của trang Azure
        services = response.css('div.product-list-item')  # Ví dụ selector, hãy kiểm tra lại
        for svc in services:
            service_name = svc.css('h3::text').get()
            if service_name:
                service_name = service_name.strip()
                detail_url = svc.css('a::attr(href)').get()
                if detail_url:
                    detail_url = urljoin(response.url, detail_url)
                    yield scrapy.Request(detail_url, callback=self.parse_azure_service_detail, meta={'provider': 'Microsoft Azure', 'service_name': service_name})

    def parse_azure_service_detail(self, response):
        item = CloudServiceItem()
        item['provider'] = response.meta['provider']
        item['service_name'] = response.meta['service_name']
        item['category'] = 'Storage'
        item['description'] = response.css('div.product-description p::text').get(default='').strip()
        features = response.css('ul.feature-list li::text').getall()
        item['features'] = [feature.strip() for feature in features]
        price_info = response.css('div.pricing-info::text').getall()
        item['price_info'] = ' '.join(price_info).strip()
        item['official_page'] = response.url

        # Tạo URL để tìm kiếm trên Gartner (Nếu cần thiết)
        search_query = '+'.join(item['service_name'].split())
        gartner_search_url = f"https://www.gartner.com/reviews/search/products?query={search_query}&category=Strategic+Cloud+Platform+Services"
        item['gartner_reviews_url'] = gartner_search_url

        yield item

        # Lấy review từ Gartner
        yield SeleniumRequest(url=gartner_search_url, callback=self.parse_gartner_reviews, meta={'service_name': item['service_name']}, wait_time=10)

    ## Gartner Parsing
    def parse_gartner(self, response):
        # Phân tích trang danh sách các dịch vụ trên Gartner
        services = response.css('div.review-list__item')  # Cập nhật selector theo cấu trúc thực tế của trang Gartner
        for service in services:
            service_name = service.css('h3.review-card__title::text').get()
            if service_name:
                service_name = service_name.strip()
                service_url = service.css('a.review-card__link::attr(href)').get()
                if service_url:
                    service_url = urljoin(response.url, service_url)
                    yield SeleniumRequest(url=service_url, callback=self.parse_gartner_service_detail, meta={'service_name': service_name}, wait_time=10)

        # Phân trang (nếu có)
        next_page = response.css('a.pagination__next::attr(href)').get()
        if next_page:
            next_page_url = urljoin('https://www.gartner.com', next_page)
            yield SeleniumRequest(url=next_page_url, callback=self.parse_gartner, wait_time=10)

    def parse_gartner_service_detail(self, response):
        service_name = response.meta['service_name']
        reviews = response.css('div.review')  # Cập nhật selector theo cấu trúc thực tế của trang Gartner

        for review in reviews:
            review_item = ServiceReviewItem()
            review_item['service_name'] = service_name
            review_item['user_name'] = review.css('span.user-name::text').get(default='').strip()
            review_item['rating'] = review.css('span.rating::attr(data-rating)').get()
            review_item['review_text'] = review.css('div.review-content p::text').get(default='').strip()
            review_item['review_source'] = response.url
            review_item['review_date'] = review.css('span.review-date::text').get(default='').strip()
            yield review_item

        # Phân trang đánh giá (nếu có)
        next_page = response.css('a.pagination__next::attr(href)').get()
        if next_page:
            next_page_url = urljoin('https://www.gartner.com', next_page)
            yield SeleniumRequest(url=next_page_url, callback=self.parse_gartner_service_detail, meta={'service_name': service_name}, wait_time=10)