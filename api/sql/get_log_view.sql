CREATE VIEW log_view
    AS
    SELECT 
        "Active", 
        "Date Added", 
        "target sorg",
        "target plant",
        "email prefix (from request form)",
        "SAP MATNR (from request form)",
        "Service Requested (from request form)",
        "Location (from request form)",
        (SELECT mara.[Material Description] FROM mara 
        WHERE 
            mara.Material = log.[SAP MATNR (from request form)]
        ) as 'Description',
        (SELECT ausp.ATWRT FROM ausp 
        WHERE
            ausp.OBJEK = log.[SAP MATNR (from request form)] AND
            ausp.ATINN LIKE 'CATALOG_STRING1'
        ) as 'Catalog',
        (SELECT ausp.ATWRT FROM ausp 
        WHERE
            ausp.OBJEK = log.[SAP MATNR (from request form)] AND
            ausp.ATINN LIKE 'SERIES_DESIGNATOR'
        ) as 'Ser',
        (SELECT mara.[Material Type] FROM mara 
        WHERE 
            mara.Material = log.[SAP MATNR (from request form)]
        ) AS 'MTART',
        (SELECT VMSTA FROM mvke 
	    WHERE 
            VKORG = 1000 AND
	        mvke.MATNR = log.[SAP MATNR (from request form)]) as '1K D-CHAIN',
        (SELECT PRAT4 FROM mvke 
	    WHERE 
            VKORG = 1000 AND
	        mvke.MATNR = log.[SAP MATNR (from request form)]) as '1K CS',
        (SELECT PRAT8 FROM mvke 
	    WHERE 
            VKORG = 1000 AND
	        mvke.MATNR = log.[SAP MATNR (from request form)]) as '1K PUB',
        (SELECT VMSTA FROM mvke 
	    WHERE 
            VKORG = 4000 AND
	        mvke.MATNR = log.[SAP MATNR (from request form)]) as '4K D-CHAIN',
        (SELECT PRAT4 FROM mvke 
	    WHERE 
            VKORG = 4000 AND
	        mvke.MATNR = log.[SAP MATNR (from request form)]) as '4K CS',
        (SELECT Amount FROM price 
	    WHERE 
	        price.Material = log.[SAP MATNR (from request form)] AND
            price.[SOrg.] = log.[target sorg]) as 'target sorg price',
        (SELECT VMSTA FROM mvke 
	    WHERE 
	        mvke.MATNR = log.[SAP MATNR (from request form)] AND
            mvke.VKORG = log.[target sorg]) as 'target sorg dchain',
        (SELECT DWERK FROM mvke 
	    WHERE 
	        mvke.MATNR = log.[SAP MATNR (from request form)] AND
            mvke.VKORG = log.[target sorg]) as 'target sorg DWERK',
        (SELECT PRAT4 FROM mvke 
	    WHERE 
	        mvke.MATNR = log.[SAP MATNR (from request form)] AND
            mvke.VKORG = log.[target sorg]) as 'target sorg cs',
        (SELECT PRAT8 FROM mvke 
	    WHERE 
	        mvke.MATNR = log.[SAP MATNR (from request form)] AND
            mvke.VKORG = log.[target sorg]) as 'target sorg pub',
        (SELECT MMSTA FROM marc 
	    WHERE 
	        marc.MATNR = log.[SAP MATNR (from request form)] AND
            marc.WERKS = log.[target plant]) as 'target plant status',
        (SELECT DISMM FROM marc 
	    WHERE 
	        marc.MATNR = log.[SAP MATNR (from request form)] AND
            marc.WERKS = log.[target plant]) as 'target plant mrp type',
        (SELECT MMSTA FROM marc 
	    WHERE 
	        marc.MATNR = log.[SAP MATNR (from request form)] AND
            marc.WERKS = (SELECT DWERK FROM mvke 
                            WHERE 
                                mvke.MATNR = log.[SAP MATNR (from request form)] AND
                                mvke.VKORG = log.[target sorg])) as 'DWERK plant status',
        (SELECT DISMM FROM marc 
	    WHERE 
	        marc.MATNR = log.[SAP MATNR (from request form)] AND
            marc.WERKS = (SELECT DWERK FROM mvke 
                            WHERE 
                                mvke.MATNR = log.[SAP MATNR (from request form)] AND
                                mvke.VKORG = log.[target sorg])) as 'DWERK plant mrp type',
        CASE 
            WHEN (
            ((SELECT MMSTA FROM marc 
                        WHERE 
                            marc.MATNR = log.[SAP MATNR (from request form)] AND
                            marc.WERKS = log.[target plant]) = 0) OR
            ((SELECT DWERK FROM mvke 
                        WHERE 
                            mvke.MATNR = log.[SAP MATNR (from request form)] AND
                            mvke.VKORG = log.[target sorg]) = 0) 
            ) THEN 'x'
            ELSE
            null
        END as 'mif/soerf check'                      
    

    FROM log
    -- LEFT JOIN mara ON
    --     log.[SAP MATNR (from request form)] = mara.Material -- AND
    -- LEFT JOIN price ON
    --     log.[SAP MATNR (from request form)] = price.Material AND
    --     log.[target sorg] = price.[SOrg.]