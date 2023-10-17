## DEC - project 2
## OpenSky Network API

This project consisting of implementation ETL process for getting DVD RENTAL data.

---

| Author          | GitHub profile |
| ---           | --- |
|Pawel Dymek    | [pdymek](https://github.com/pdymek)|


The solutions is done with help of:
- Postrgres tutorial - https://www.postgresqltutorial.com/postgresql-getting-started/postgresql-sample-database/
- Postgres wiki - https://wiki.postgresql.org/
- Resources provided during DEC courses - https://dataengineercamp.com/


---
### Source database diagram
![dvd-rental-sample-database-diagram](/docs/dvd-rental-sample-database-diagram.png)


---

Tables for ingestion:
- CATEGORY
- FILM_CATEGORY
- FILM
- INVENTORY
- RENTAL
- CUSTOMER
- ADDRESS
- CITY
- COUNTRY

---

Running Airbyte on AWS

![aribyte_aws](/docs/airbyte_aws.png)

Tables after igestion through Airbyte

![airbyte_table](/docs/airbyte_tables.png)

Using AWS cmd client

![aws_client](/docs/aws_client.png)

![dwh](/docs/dwh.drawio.svg)

![dvd_rental_dwh](/docs/dvd_rental_dwh.png)


Sample sql report on DWH:

``` sql
WITH cte_base AS (
	select dd.yearmonth
		, cu.country
		, count(1) as rental_amount
	from fact_rental as fr
	inner join dim_dates as dd
		on fr.rental_date = dd.date
	inner join dim_customers as cu
		on fr.customer_id = cu.customer_id
	group by dd.yearmonth
		, cu.country	
)
select *
	, sum(cb.rental_amount) over (partition by cb.country order by cb.yearmonth asc) as cumulative_rental_amount
from cte_base as cb
```

---

Template `.env` file:

```
TARGET_DATABASE_NAME=
TARGET_SERVER_NAME=
TARGET_DB_USERNAME=
TARGET_DB_PASSWORD=
TARGET_PORT=

LOGGING_SERVER_NAME=
LOGGING_DATABASE_NAME=
LOGGING_USERNAME=
LOGGING_PASSWORD=
LOGGING_PORT=

AIRBYTE_USERNAME=
AIRBYTE_PASSWORD=
AIRBYTE_SERVER_NAME=
```