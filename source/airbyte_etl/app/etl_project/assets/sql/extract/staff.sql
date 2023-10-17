{% set config = {
    "extract_type": "full",
    "source_table_name": "staff"
} %}


select 
    staff_id, 
    first_name, 
    last_name, 
    address_id, 
    email, 
    store_id, 
    active, 
    username, 
    last_update 
from 
    {{ config["source_table_name"] }}
