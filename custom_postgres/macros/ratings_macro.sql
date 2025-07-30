{% macro generate_ratings() %}

CASE
            WHEN f.user_rating >= 4.5 THEN 'Excellent'
            WHEN f.user_rating >= 4.0 THEN 'Good'
            WHEN f.user_rating >= 3.5 THEN 'Average'
            ELSE 'Poor'
        end as rating_category

{% endmacro %}