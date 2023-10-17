{% set config = {
    "extract_type": "full",
    "source_table_name": "category"
} %}

select 
    category_id,
    name,
    last_update
from 
    {{ config["source_table_name"] }}