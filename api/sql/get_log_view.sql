-- CREATE VIEW log_view 
-- AS
SELECT 
    'target sorg',
    'target plant',
    "email prefix (from request form)",
    "SAP MATNR(from request form)",
    "Service Requested (from request form)",
    "Location (from request form)"
FROM log
-- WHERE 'Active' = 1