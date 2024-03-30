{{
    config(
        materialized='view'
    )
}}

with ecoenergy_data as (
      select * from {{ source('staging', 'ecoenergy_data') }}
),
staging_ecoenergy_data as (
    select
        {{ dbt.safe_cast("electrical_capacity", api.Column.translate_type("float")) }} as electrical_capacity,
        {{ adapter.quote("energy_source_level_1") }},
        {{ adapter.quote("energy_source_level_2") }},
        {{ adapter.quote("energy_source_level_3") }},
        {{ adapter.quote("technology") }},
        {{ adapter.quote("data_source") }},
        {{ adapter.quote("nuts_1_region") }},
        {{ adapter.quote("nuts_2_region") }},
        {{ adapter.quote("nuts_3_region") }},
        {{ dbt.safe_cast("lon", api.Column.translate_type("float")) }} as lon,
        {{ dbt.safe_cast("lat", api.Column.translate_type("float")) }} as lat,
        {{ adapter.quote("municipality") }},
        {{ adapter.quote("municipality_code") }},
        {{ adapter.quote("postcode") }},
        {{ adapter.quote("address") }},
        {{ adapter.quote("federal_state") }},
        {{ dbt.safe_cast("commissioning_date", api.Column.translate_type("date")) }} as commissioning_date,
        {{ dbt.safe_cast("decommissioning_date", api.Column.translate_type("date")) }} as decommissioning_date,
        {{ adapter.quote("voltage_level") }},
        {{ adapter.quote("eeg_id") }},
        {{ adapter.quote("dso") }},
        {{ adapter.quote("dso_id") }},
        {{ adapter.quote("tso") }}

    from ecoenergy_data
)
select * from staging_ecoenergy_data


-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

  limit 1000

{% endif %}