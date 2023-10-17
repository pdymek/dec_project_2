select f.film_id
	, f.title
	, f.release_year
	, f.rental_duration
	, f.rental_rate
	, f.length
	, f.rating
	, ca.category_id as film_category_id
	, ca.name as film_category_name
from film as f
left outer join film_category as fc
	on f.film_id = fc.film_id
left outer join category as ca
	on fc.category_id = ca.category_id
