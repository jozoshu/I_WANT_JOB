# I WANT A JOB!
채용 사이트의 공고들을 수집하여 저장한다.

### 개발환경 
- OS: Mac on M1 (local)
- Language: [Python 3.9.2](https://www.python.org/downloads/release/python-392/)
- Database: PostgreSQL 12.7

### 프로젝트 구조
~~~bash
$> git clone https://github.com/jozoshu/I_WANT_JOB.git

.
├── config             # 환경 모듈
│   ├── connections
│   └── logging
├── logs               # 로그
├── modules            # 실행 모듈
│   ├── crawlers
│   └── handlers
├── venv               # python 가상환경
├── .env               # 환경변수 파일
├── main.py            # 메인 실행파일
└── requirements.txt   # 패키지 관리
~~~

# 1. Environment

## 1.1 Set .env file
~~~bash
$> vim .env

## - Wanted - ##

# 거주국가
COUNTRY=kr
# 직무 pk (872: 서버개발자, 899: 파이썬개발자, 895: Node.JS 개발자, 655: 데이터엔지니어)
TAG_TYPE_ID=872
# 정렬순서
JOB_SORT=job.latest_order
# 지역
LOCATIONS=seoul.all
# 경력
YEAR=3


## - DB Connection - ##

DB_HOST=localhost
DB_NAME=...
DB_USER=...
DB_PASSWORD=...
DB_PORT=5432
~~~

### 1.1.1 Sample DDL
~~~sql
CREATE TABLE public.tb_wtd_position
(
    id bigserial NOT NULL,
    company_id integer NOT NULL,
    company character varying(50) NOT NULL,
    position_id integer NOT NULL,
    position character varying(250) NOT NULL,
    thumbnail text,
    logo text,
    created_dtm timestamp with time zone DEFAULT now(),
    CONSTRAINT tb_wtd_position_pkey PRIMARY KEY (id)
);

CREATE TABLE public.tb_wtd_position_detail
(
    id bigserial NOT NULL,
    position_id integer NOT NULL,
    position character varying(250) NOT NULL,
    company_id integer NOT NULL,
    company character varying(50),
    intro text NOT NULL,
    main_tasks text NOT NULL,
    requirements text NOT NULL,
    preferred_points text NOT NULL,
    benefits text NOT NULL,
    crawl_date date DEFAULT now(),
    created_dtm timestamp with time zone DEFAULT now(),
    CONSTRAINT tb_wtd_position_detail_pkey PRIMARY KEY (id)
);

CREATE UNIQUE INDEX tb_wtd_position_detail_crawl_date_idx
    ON public.tb_wtd_position_detail USING btree
    (crawl_date, position_id);

CREATE TABLE public.tb_op_process_listing
(
    id bigserial NOT NULL,
    handler_type character varying(10) NOT NULL,
    idx smallint NOT NULL,
    status smallint NOT NULL,
    created_dtm timestamp with time zone DEFAULT now(),
    CONSTRAINT tb_op_process_listing_pkey PRIMARY KEY (id)
);

CREATE TABLE public.tb_op_process_collecting
(
    id bigserial NOT NULL,
    handler_type character varying(10) NOT NULL,
    position_id integer NOT NULL,
    position character varying(250) NOT NULL,
    company character varying(50),
    status smallint NOT NULL DEFAULT 0,
    created_dtm timestamp with time zone DEFAULT now(),
    updated_dtm timestamp with time zone DEFAULT now(),
    CONSTRAINT tb_op_process_publish_pkey PRIMARY KEY (id)
);

CREATE TABLE public.tb_op_last_crawl_date
(
    id serial NOT NULL,
    handler_type character varying(10) NOT NULL,
    last_crawl_date date DEFAULT now(),
    created_dtm timestamp with time zone DEFAULT now(),
    CONSTRAINT tb_op_last_crawl_date_pkey PRIMARY KEY (id)
);
~~~

## 1.2 Set virtual environment
~~~bash
$> virtualenv venv --python=python3.9
$> source venv/bin/activate
(venv) $> pip install -r requirements.txt
~~~

## 1.3 Run~!
~~~bash
(venv) $> python main.py
~~~
