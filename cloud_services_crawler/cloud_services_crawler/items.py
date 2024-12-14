# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# cloud_services_crawler/items.py

import scrapy

class CloudServiceItem(scrapy.Item):
    provider = scrapy.Field()         # Tên nhà cung cấp (ví dụ: Amazon AWS)
    service_name = scrapy.Field()     # Tên dịch vụ (ví dụ: Amazon S3)
    category = scrapy.Field()         # Loại dịch vụ (Storage, Compute, Database, ...)
    description = scrapy.Field()      # Mô tả ngắn về dịch vụ
    features = scrapy.Field()         # Danh sách các tính năng, lưu trữ dưới dạng list
    price_info = scrapy.Field()       # Thông tin giá cả, lưu trữ dưới dạng string hoặc dict
    official_page = scrapy.Field()    # URL trang chính thức của dịch vụ
    gartner_reviews_url = scrapy.Field()   # URL để crawl review từ Gartner

class ServiceReviewItem(scrapy.Item):
    service_name = scrapy.Field()     # Tên dịch vụ (liên kết với CloudServiceItem)
    user_name = scrapy.Field()        # Tên người dùng đã đánh giá
    rating = scrapy.Field()           # Điểm đánh giá (1-5 hoặc theo hệ thống Gartner)
    review_text = scrapy.Field()      # Nội dung đánh giá
    review_source = scrapy.Field()    # URL nguồn đánh giá (trang Gartner)
    review_date = scrapy.Field()      # Ngày đánh giá