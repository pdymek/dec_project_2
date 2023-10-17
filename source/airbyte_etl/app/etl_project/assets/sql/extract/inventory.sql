{% set config = {
    "extract_type": "incremental", 
    "incremental_column": "last_update",
    "source_table_name": "inventory"
} %}

select 
    inventory_id, 
    film_id,
    store_id, 
    last_update 
from 
    {{ config["source_table_name"] }}

{% if is_incremental %}
    where {{ config["incremental_column"] }} > '{{ incremental_value }}'
{% endif %}
