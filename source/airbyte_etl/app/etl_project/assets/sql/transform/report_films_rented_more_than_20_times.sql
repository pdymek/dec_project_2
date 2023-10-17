select df.title
	, count(1) as rental_amount
from fact_rental as fr
inner join dim_films as df
	on fr.film_id = df.film_id
group by df.title
having count(1) > 20
order by rental_amount desc