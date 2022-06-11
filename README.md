# scrap

Requirements
=============
- bs4
- sqlalchemy
- psycopg2
- python-dotenv

To access to some website with authentication. We must have the cookies and the headers of the page call or the api call.

Get cookies / headers
=====================
The first step, access the admin page, after login.
By clicking on the "Products" option in the left menu.
In the "Inspection" functionality in the browser (Chrome or Firefox) go to the "Network" panel, look for the called "products", right click and select "Copy - curl bash"
On the "https://curlconverter.com/" website, paste the curl bash, then copy the results in the value of the "product_cookies" and "product_headers" variables respectively.
Then, to get the cookies and headers of API, you clicking on the link of product, in the in the "Inspection" functionality in the browser (Chrome or Firefox) go to the "Network" panel, look for the called "categories", right click and select "Copy - curl bash"
On the "https://curlconverter.com/" website, paste the curl bash, then copy the results in the value of the "api_cookies" and "api_headers" variables respectively

Constants
=========
Change the constants if necessary
DATABASE_URI = os.getenv(database_uri) (get the connection string from the .env file)
CREATED_BY = 'scrapy' (creation user)
PAGES = 5 (pagination: amount of pages)
INITIAL_PAGE = 1 (pagination: initial page)
PRODUCT_PAGE = 'https://app.kajabi.com/admin/sites/46190/products?page=' (product url base)
WEBSITE_URL = 'https://app.kajabi.com' (kajabi website)
API_URL_BASE = 'https://app.kajabi.com/api/admin/products/' (api url base)

Run
===
- From main folder go to ./venv/Scripts/
- run activate
- in venv environment go to main folder: \scrap
- run python main.py

Database
========

CREATE TABLE public."Kajabi_Product" (
	"id" varchar(64),
	"title" varchar(512) NULL,
	"description" varchar(1024) NULL,
	"thumbnail" varchar(1024) null,
	"json_data" json,
	"created_by" varchar(64),
	"created" timestamp NOT null default current_timestamp,
	CONSTRAINT "PK_Kajabi_Product" PRIMARY KEY ("id")
);

CREATE TABLE public."Kajabi_Category" (
	"id" varchar(64),
	"product_id" varchar(64),
	"title" varchar(512) NULL,
	"description" varchar(1024) NULL,
	"poster_image" varchar(1024) null,
	"json_data" json,
	"created_by" varchar(64),
	"created" timestamp NOT null default current_timestamp,
	CONSTRAINT "PK_Kajabi_Category" PRIMARY KEY ("id")
);

CREATE TABLE public."Kajabi_Post" (
	"id" varchar(64),
	"category_id" varchar(64),
	"title" varchar(512) NULL,
	"publishing_status" varchar(32) NULL,
	"body" text,
	"poster_image" varchar(1024) null,
	"json_data" json,
	"created_by" varchar(64),
	"created" timestamp NOT null default current_timestamp,
	CONSTRAINT "PK_Kajabi_Post" PRIMARY KEY ("id")
);

ALTER TABLE public."Kajabi_Category" ADD CONSTRAINT kajabi_category_fk FOREIGN KEY (product_id) REFERENCES public."Kajabi_Product"(id);

ALTER TABLE public."Kajabi_Post" ADD CONSTRAINT kajabi_post_fk FOREIGN KEY (category_id) REFERENCES public."Kajabi_Category"(id);
