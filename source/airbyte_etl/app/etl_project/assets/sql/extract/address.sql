{% set config = {
    "extract_type": "full",
    "source_table_name": "address"
} %}

select 
    address_id, 
    address,
    address2, 
    district,
    city_id, 
    postal_code, 
    phone,
    last_update 
from 
    {{ config["source_table_name"] }}
