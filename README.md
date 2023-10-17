## DEC - project 2
## OpenSky Network API

This project consisting of implementation ETL process for getting DVD RENTAL data.


The project is done with Airbyte/Python, published on AWS. The database/dwh engine is Posgres.

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
The synhronization is done for following tables:

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

RENTAL and INVENTORY have delta load strategy, other are loaded as full load.

Tables after igestion through Airbyte

![airbyte_table](/docs/airbyte_tables.png)

---


### AWS publishing

Running Airbyte on AWS

AWS tech stack:

- Source postgres database - RDS
- Airbyte connection - EC2
- Running docker & transorm - ECS
- Target postgres database - RDS

![aribyte_aws](/docs/airbyte_aws.png)

Using AWS cmd client

![aws_client](/docs/aws_client.png)


---

### Output DWH

DWH shema:
- fact_rental
- dim_films - films & categories
- dim customers - customers & regions
- dim dates - auto-generated dates


![dwh](/docs/dwh.drawio.svg)

![dvd_rental_dwh](/docs/dvd_rental_dwh.png)

---

### Output reports

Reports are refreshed after tansform and loading stage. The sequence is kept with dag.

```  python
        dag.add(dim_films)
        dag.add(dim_dates)
        dag.add(dim_customers)
        dag.add(fact_rental)
        dag.add(report_monthly_cumulative_amount_by_country, fact_rental, dim_dates, dim_customers)
        dag.add(report_top_10_rented_films, fact_rental, dim_films)
        dag.add(report_films_rented_more_than_20_times, fact_rental, dim_films)
```

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
### Docker & config files

The `.env` file should be located in `cd` folder, with listed paramter

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

The local docker is run with commands:

Build:
> docker build . -t dvd_rental:2.0


Run:
> docker run --env-file .env dvd_rental:2.0