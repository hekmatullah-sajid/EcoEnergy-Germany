{{
    config(
        materialized='table',
        partition_by={
            "field": "commissioning_date",
            "data_type": "date",
            "granularity": "month"
        }
    )
}}


select
    electrical_capacity,
    energy_source_level_1, -- Constant value across all rows, currently not useful for dashboard but retained for clarity and potential future utilization
    energy_source_level_2,
    energy_source_level_3,
    technology,
    data_source,
    nuts_1_region,
    nuts_2_region,
    nuts_3_region,
    lon,
    lat,
    municipality,
    REPLACE(postcode, '.0', '') as postcode, -- remove trailing ".0" from postcode values
    address,
    -- TRIM(federal_state) as federal_state,
    CASE WHEN TRIM(federal_state) = 'Baden-Würtemberg' THEN 'Baden-Württemberg' -- state name miss-spelled
       ELSE TRIM(federal_state) -- trim leading or trainling spaces
    END AS federal_state,
    commissioning_date,
    decommissioning_date,
    voltage_level,
    dso,
    tso
from {{ ref('staging_ecoenergy_data') }}
WHERE 
    commissioning_date > '1995-12-31' -- records before are sparse and have insufficient data.