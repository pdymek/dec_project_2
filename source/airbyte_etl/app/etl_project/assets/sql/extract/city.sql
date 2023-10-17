{% set config = {
    "extract_type": "full",
    "source_table_name": "city"
} %}

select 
    city_id, 
    city, 
    country_id, 
    last_update 
from 
    {{ config["source_table_name"] }}
