{% set config = {
    "extract_type": "full",
    "source_table_name": "film"
} %}

select 
    film_id, 
    title, 
    description, 
    release_year, 
    language_id, 
    rental_duration, 
    rental_rate, 
    length, 
    replacement_cost, 
    rating, 
    last_update, 
    special_features,
    fulltext
from 
    {{ config["source_table_name"] }}