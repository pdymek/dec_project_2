{% set config = {
    "extract_type": "full",
    "source_table_name": "country"
} %}

select 
    country_id,
    country, 
    last_update
from    
    {{ config["source_table_name"] }}
