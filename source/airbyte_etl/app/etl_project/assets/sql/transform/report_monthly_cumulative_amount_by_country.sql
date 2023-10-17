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