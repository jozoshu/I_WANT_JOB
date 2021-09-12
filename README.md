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

- [Table Scheme](https://github.com/jozoshu/I_WANT_JOB/wiki/Database#table-scheme)

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

## 1.4 Add command to crontab
~~~bash
$> crontab -e

# 루트경로
ROOTPATH=/root/project/path

# 매일 자정마다 돌아가도록 설정
0 15 * * * $ROOTPATH/venv/bin/python $ROOTPATH/main.py
~~~
