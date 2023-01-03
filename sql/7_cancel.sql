SELECT
    ap_mm_service.*,
    CASE
        WHEN vkorg = '5000'  THEN
            'Australia'
        WHEN vkorg = '5003'  THEN
            'China'
        WHEN vkorg = '5007'  THEN
            'HK'
        WHEN vkorg = '5008'  THEN
            'India'      
        WHEN vkorg = '5010'  THEN
            'Korea' 
        WHEN vkorg = '5011'  THEN
            'Malaysia'             
        WHEN vkorg = '5012'  THEN
            'New Zealand'            
        WHEN vkorg = '5013'  THEN
            'Philippines'            
        WHEN vkorg = '5014'  THEN
            'Singapore'
        WHEN vkorg = '5016'  THEN
            'Taiwan'            
    END AS "location"
FROM
    ap_mm_service
WHERE
    requester IN ( 'sea hub', 'pls', 'cancel - S+S brand','cancel - Encompass', 'cancel - KMAT not extended' );