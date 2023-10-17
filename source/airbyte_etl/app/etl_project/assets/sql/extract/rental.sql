{% set config = {
    "extract_type": "incremental", 
    "incremental_column": "last_update",
    "source_table_name": "rental",
} %}

select 
    rental_id,
    rental_date, 
    inventory_id, 
    customer_id, 
    return_date, 
    staff_id, 
    last_update 
from 
    {{ config["source_table_name"] }}

{% if is_incremental %}
    where {{ config["incremental_column"] }} > '{{ incremental_value }}'
{% endif %}
