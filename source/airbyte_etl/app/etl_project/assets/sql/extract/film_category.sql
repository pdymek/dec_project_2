{% set config = {
    "extract_type": "full",
    "source_table_name": "film_category"
} %}

select 
    film_id, 
    category_id, 
    last_update 
from 
    {{ config["source_table_name"] }}
