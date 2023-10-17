select cu.customer_id
	, cu.first_name
	, cu.last_name
	, cu.activebool
	, ad.address_id
	, ad.address
	, ad.address2
	, ad.district
	, ad.postal_code
	, ci.city_id
	, ci.city
	, co.country_id
	, co.country
from customer as cu
left outer join address as ad
	on cu.address_id = ad.address_id
left outer join city as ci
	on ad.city_id = ci.city_id
left outer join country as co
	on ci.country_id = co.country_id