select iv.inventory_id
	, iv.film_id
	, iv.store_id
	, rt.rental_id
	, rt.customer_id
	, DATE(rt.rental_date) as rental_date
	, DATE(rt.return_date) as return_date
	, 1 as count_rental
from rental as rt
inner join inventory as iv
	on rt.inventory_id = iv.inventory_id