{% set film_title = "Dunkirk" %}

SELECT * 
FROM {{ ref('films') }} f
WHERE f.title = '{{ film_title }}' 