/* CLEAR AP_MM_SERVICE table */
truncate table AP_MM_SERVICE;
COMMIT;

/* INSERT EXCEL INS QUERY */


COMMIT;
/* COUNT OBJECTS INSERTED */
SELECT COUNT(*) as ROWS_ADDED FROM AP_MM_SERVICE;

/* MIF / SOERF */
INSERT INTO ap_mm_service (
    vkorg,
    werks,
    requester,
    matnr,
    service
)
    SELECT
        '5014'                           AS vkorg,
        '5200'                           AS werks,
        'sea hub'                        AS requester,
        ap.matnr                         AS matnr,
        'Plant and sales org extension'  AS service
    FROM
        ap_mm_service ap
    WHERE
        ap.vkorg IN ( '5000', '5007', '5011', '5012', '5013',
                      '5017' )
        AND (
            SELECT
                mandt
            FROM
                sapecc_dly_librarian.marc
            WHERE
                    marc.matnr = ap.matnr
                AND marc.werks = '5200'
        ) IS NULL
        AND (
            SELECT
                x.matnr
            FROM
                ap_mm_service x
            WHERE
                    x.matnr = ap.matnr
                AND x.vkorg = '5014'
        ) IS NULL
    UNION
    SELECT
        '5008'                           AS vkorg,
        '5070'                           AS werks,
        'pls'                            AS requester,
        ap.matnr                         AS matnr,
        'Plant and sales org extension'  AS service
    FROM
        ap_mm_service ap
    WHERE
            ap.werks = '5080'
        AND (
            SELECT
                mandt
            FROM
                sapecc_dly_librarian.marc
            WHERE
                    marc.matnr = ap.matnr
                AND marc.werks = '5070'
        ) IS NULL
        AND (
            SELECT
                x.matnr
            FROM
                ap_mm_service x
            WHERE
                    x.matnr = ap.matnr
                AND x.werks = '5070'
        ) IS NULL
    UNION
    SELECT
        '5000'             AS vkorg,
        '5150'             AS werks,
        'return'           AS requester,
        ap.matnr           AS matnr,
        'Plant extension'  AS service
    FROM
        ap_mm_service ap
    WHERE
            ap.werks = '5200'
        AND ap.vkorg = '5000'
        AND (
            SELECT
                mandt
            FROM
                sapecc_dly_librarian.marc
            WHERE
                    marc.matnr = ap.matnr
                AND marc.werks = '5150'
        ) IS NULL
        AND (
            SELECT
                x.matnr
            FROM
                ap_mm_service x
            WHERE
                    x.matnr = ap.matnr
                AND x.werks = '5150'
        ) IS NULL
    UNION
    SELECT
        '5007'             AS vkorg,
        '5050'             AS werks,
        'return'           AS requester,
        ap.matnr           AS matnr,
        'Plant extension'  AS service
    FROM
        ap_mm_service ap
    WHERE
            ap.werks = '5200'
        AND ap.vkorg = '5007'
        AND (
            SELECT
                mandt
            FROM
                sapecc_dly_librarian.marc
            WHERE
                    marc.matnr = ap.matnr
                AND marc.werks = '5050'
        ) IS NULL
        AND (
            SELECT
                x.matnr
            FROM
                ap_mm_service x
            WHERE
                    x.matnr = ap.matnr
                AND x.werks = '5050'
        ) IS NULL
    UNION
    SELECT
        '5012'             AS vkorg,
        '5130'             AS werks,
        'return'           AS requester,
        ap.matnr           AS matnr,
        'Plant extension'  AS service
    FROM
        ap_mm_service ap
    WHERE
            ap.werks = '5200'
        AND ap.vkorg = '5012'
        AND (
            SELECT
                mandt
            FROM
                sapecc_dly_librarian.marc
            WHERE
                    marc.matnr = ap.matnr
                AND marc.werks = '5130'
        ) IS NULL
        AND (
            SELECT
                x.matnr
            FROM
                ap_mm_service x
            WHERE
                    x.matnr = ap.matnr
                AND x.werks = '5130'
        ) IS NULL
    UNION
        SELECT
        ap.vkorg              AS vkorg,
        ap.werks              AS werks,
        'cancel - Encompass'  AS requester,
        ap.matnr              AS matnr,
        'cancel - Encompass'  AS service
    FROM
        ap_mm_service ap
    WHERE
        (
            SELECT
                mvke.matnr
            FROM
                sapecc_dly_librarian.mvke
            WHERE
                    mvke.mandt = '400'
                AND mvke.matnr = ap.matnr
                AND mvke.prodh = 'PLSA1343A5784A2902'
                AND ROWNUM = 1
        ) IS NOT NULL
    UNION
    SELECT
        ap.vkorg              AS vkorg,
        ap.werks              AS werks,
        'cancel - S+S brand'  AS requester,
        ap.matnr              AS matnr,
        'cancel - S+S brand'  AS service
    FROM
        ap_mm_service ap
    WHERE
        (
            SELECT
                mvke.matnr
            FROM
                sapecc_dly_librarian.mvke
            WHERE
                    mvke.mandt = '400'
                AND mvke.matnr = ap.matnr
                AND mvke.mvgr1 IN ( '013', '085', '086', '087', '088',
                                    '089', '090' )
                AND ROWNUM = 1
        ) IS NOT NULL
    UNION
    SELECT
        ap.vkorg                      AS vkorg,
        ap.werks                      AS werks,
        'cancel - KMAT not extended'  AS requester,
        ap.matnr                      AS matnr,
        (
        SELECT
        'cancel - KMAT '
        || TRIM(mara.satnr)
        || ' not extended, contact'
        || ' '
        || zcmk_mat_prodh.vorna
        || ' '
        || zcmk_mat_prodh.nachn
        || ' for assistance.'
        FROM
            sapecc_dly_librarian.mara,
            sapecc_librarian.zcmk_mat_prodh zcmk_mat_prodh
        WHERE
                mara.mandt = '400'
            AND zcmk_mat_prodh.mandt = mara.mandt
            AND mara.matnr = ap.matnr
            AND zcmk_mat_prodh.prodh = mara.prdha
        ) AS service
    FROM
        ap_mm_service ap
    WHERE
        (
            SELECT
                TRIM(mara.satnr)
            FROM
                sapecc_dly_librarian.mara
            WHERE
                    mara.mandt = '400'
                AND mara.matnr = ap.matnr
        ) IS NOT NULL
        AND ( (
            SELECT
                mvke.matnr
            FROM
                sapecc_dly_librarian.mara,
                sapecc_dly_librarian.mvke
            WHERE
                    mara.mandt = '400'
                AND mvke.mandt = mara.mandt
                AND mara.matnr = ap.matnr
                AND mvke.matnr = TRIM(mara.satnr)
                AND mvke.vkorg = ap.vkorg
        ) IS NULL
              OR (
            SELECT
                TRIM(mvke.vmsta)
            FROM
                sapecc_dly_librarian.mara,
                sapecc_dly_librarian.mvke
            WHERE
                    mara.mandt = '400'
                AND mvke.mandt = mara.mandt
                AND mara.matnr = ap.matnr
                AND mvke.matnr = TRIM(mara.satnr)
                AND mvke.vkorg = ap.vkorg
        ) IS NOT NULL );

COMMIT;

DELETE FROM ap_mm_service ap
WHERE
        ap.requester <> 'cancel - S+S brand'
    AND (
        SELECT
            mvke.matnr
        FROM
            sapecc_dly_librarian.mvke
        WHERE
                mvke.mandt = '400'
            AND mvke.matnr = ap.matnr
            AND mvke.mvgr1 IN ( '013', '085', '086', '087', '088',
                                '089', '090' )
            AND ROWNUM = 1
    ) IS NOT NULL;
DELETE FROM ap_mm_service ap
WHERE
        ap.requester <> 'cancel - Encompass'
    AND (
        SELECT
            mvke.matnr
        FROM
            sapecc_dly_librarian.mvke
        WHERE
                mvke.mandt = '400'
            AND mvke.matnr = ap.matnr
            AND mvke.prodh = 'PLSA1343A5784A2902'
            AND ROWNUM = 1
    ) IS NOT NULL;
DELETE FROM ap_mm_service ap
WHERE
        ap.requester <> 'cancel - KMAT not extended'
    AND (
        SELECT
            TRIM(mara.satnr)
        FROM
            sapecc_dly_librarian.mara
        WHERE
                mara.mandt = '400'
            AND mara.matnr = ap.matnr
    ) IS NOT NULL
    AND ( (
        SELECT
            mvke.matnr
        FROM
            sapecc_dly_librarian.mara,
            sapecc_dly_librarian.mvke
        WHERE
                mara.mandt = '400'
            AND mvke.mandt = mara.mandt
            AND mara.matnr = ap.matnr
            AND mvke.matnr = TRIM(mara.satnr)
            AND mvke.vkorg = ap.vkorg
    ) IS NULL
          OR (
        SELECT
            TRIM(mvke.vmsta)
        FROM
            sapecc_dly_librarian.mara,
            sapecc_dly_librarian.mvke
        WHERE
                mara.mandt = '400'
            AND mvke.mandt = mara.mandt
            AND mara.matnr = ap.matnr
            AND mvke.matnr = TRIM(mara.satnr)
            AND mvke.vkorg = ap.vkorg
    ) IS NOT NULL );

COMMIT;

SELECT DISTINCT
    user                                                AS user_name,
    'AP MIF ' || sysdate                                AS project_name,
    CASE
        WHEN user = 'MVANWEE'   THEN
            'MVANWEE'
        WHEN user = 'DLFERGUS'  THEN
            'DLFERGUSON'
        WHEN user = 'JZAKRZE'  THEN
            'JAKUB.ZAKRZEWSKI'
        ELSE
            'OES-DQM'
    END                                                 AS user_email,
    mara.matnr                                          AS material,
    soerf.werks                                         AS plant,
    CASE
        WHEN mara.mtart IN ( 'ZRAW', 'ZNV', 'ZSFG' )
             AND soerf.service = 'Component extension to repair hub' THEN
            'PLS'
        ELSE
            substr(mara.prdha, 0, 3)
    END                                                 AS business_unit,
    'NO'                                                AS prototype,
    ' '                                                 AS old_material,
    'F'                                                 AS procurement_type,
    CASE
        WHEN mara.mtart = 'ZNFG' THEN
            NULL
        WHEN soerf.werks IN ( '5050', '5130', '5150', '5120', '5160',
                              '5190' ) THEN
            '5200'
        ELSE
            marc.werks
    END                                                 AS special_procurement_type,
    decode(soerf.werks, '5120', '001', '5160', '001',
           '5190', '001', '5130', '001', '5140',
           '001',
           '5150',
           '001',
           '5200',
           '002',
           '5070',
           '001',
           '5080',
           '001',
           '5040',
           '005',
           '5050',
           '005',
           '5100',
           '002',
           '5110',
           '002')                                       AS mrp_controller,
    CASE
        WHEN mara.mtart = 'ZNFG' THEN
            decode(soerf.werks, '5120', '092', '5160', '098',
                   '5190', '080', '5130', '613', '5140',
                   '610',
                   '5150',
                   '610',
                   '5200',
                   '047',
                   '5070',
                   '631',
                   '5080',
                   '631',
                   '5040',
                   '596',
                   '5050',
                   '596',
                   '5100',
                   '602',
                   '5110',
                   '600')
        ELSE
            '999'
    END                                                 AS purchasing_group,
    '999'                                               AS production_scheduler,
    decode(mvke.aumng, '1', '0', mvke.aumng)            AS min_order_size,
    decode(mvke.scmng, '1', '0', mvke.scmng)            AS rounding_value,
    CASE
        WHEN marc.beskz = 'F' THEN
            marc.plifz + 10
        ELSE
            marc.dzeit + 10
    END                                                 AS lead_time,
    '0001'                                              AS storage_location,
    '301'                                               AS wm_storage_type,
    marc.sernp                                          AS serial_number_profile,
    ' '                                                 AS eau,
    ' '                                                 AS eau3,
    ''                                                  AS sourcing_project_manager,
    ''                                                  AS purchasing_priority,
    ''                                                  AS preferred_supplier,
    CASE
        WHEN soerf.werks IN ( '3770', '5070', '5080', '8035' ) THEN
            'DLFXGST'
    END                                                 AS material_notes,
    '38'                                                AS version
FROM
    sapecc_dly_librarian.mara    mara,
    sapecc_dly_librarian.marc    marc,
    sapecc_dly_librarian.mvke    mvke,
    sapecc_dly_librarian.mvke    mvke1000,
    sapecc_dly_librarian.marc    marc1090,
    sapecc_dly_librarian.marc    marc1140,
    sapecc_dly_librarian.marc    marc1130,
    sapecc_dly_librarian.marc    marc4000,
    ap_mm_service                soerf
WHERE
        mara.mandt = '400'
    AND mvke1000.mvgr1 (+) NOT IN ( '013', '085', '086', '087', '088',
                                    '089', '090' )
    AND marc.mandt = '400'
    AND marc1090.mandt (+) = '400'
    AND marc1140.mandt (+) = '400'
    AND marc1130.mandt (+) = '400'
    AND marc4000.mandt (+) = '400'
    AND mvke.mandt (+) = '400'
    AND mvke1000.mandt (+) = '400'
  --AND soerf.werks <> 'n/a'
    AND marc1090.matnr (+) = mara.matnr
    AND marc1140.matnr (+) = mara.matnr
    AND marc1130.matnr (+) = mara.matnr
    AND marc4000.matnr (+) = mara.matnr
    AND mvke.matnr (+) = mara.matnr
    AND marc.matnr = mara.matnr
    AND mvke1000.matnr (+) = mara.matnr
    AND mara.matnr = decode(translate(soerf.matnr, '-0123456789', '-'), '', lpad(soerf.matnr, 18, '0'), soerf.matnr)
    AND marc1090.werks (+) = '1090'
    AND marc1140.werks (+) = '1140'
    AND marc1130.werks (+) = '1130'
    AND marc4000.werks (+) = '4000'
    AND mvke1000.vkorg (+) = '1000'
    AND mvke.vkorg = CASE
        WHEN (
            SELECT
                mvke2.mandt
            FROM
                sapecc_dly_librarian.mvke mvke2
            WHERE
                    mvke2.mandt = '400'
                AND mvke2.matnr = mara.matnr
                AND mvke2.mvgr1 NOT IN ( '013', '085', '086', '087', '088',
                                         '089', '090' )
                AND mvke2.vmsta IN ( ' ', 'Z5', 'ZR', 'ZG', 'ZN',
                                     'ZM' )
                AND mvke2.dwerk NOT IN ( ' ', '1010' )
                AND mvke2.vkorg = '1000'
        ) IS NOT NULL THEN
            '1000'
        WHEN (
            SELECT
                mvke2.mandt
            FROM
                sapecc_dly_librarian.mvke mvke2
            WHERE
                    mvke2.mandt = '400'
                AND mvke2.matnr = mara.matnr
                AND mvke2.mvgr1 NOT IN ( '013', '085', '086', '087', '088',
                                         '089', '090' )
                AND mvke2.vmsta IN ( ' ', 'Z5', 'ZR', 'ZG', 'ZN',
                                     'ZM' )
                AND mvke2.dwerk = '4000'
                AND mvke2.vkorg = '4000'
        ) IS NOT NULL THEN
            '4000'
        WHEN (
            SELECT
                mvke2.mandt
            FROM
                sapecc_dly_librarian.mvke mvke2
            WHERE
                    mvke2.mandt = '400'
                AND mvke2.matnr = mara.matnr
                AND mvke2.mvgr1 NOT IN ( '013', '085', '086', '087', '088',
                                         '089', '090' )
                AND mvke2.vmsta IN ( ' ', 'Z5', 'ZR', 'ZG', 'ZN',
                                     'ZM' )
                AND mvke2.dwerk <> ' '
                AND mvke2.vkorg = '5003'
        ) IS NOT NULL THEN
            '5003'
        WHEN (
            SELECT
                mvke2.mandt
            FROM
                sapecc_dly_librarian.mvke mvke2
            WHERE
                    mvke2.mandt = '400'
                AND mvke2.matnr = mara.matnr
                AND mvke2.mvgr1 NOT IN ( '013', '085', '086', '087', '088',
                                         '089', '090' )
                AND mvke2.vmsta IN ( ' ', 'Z5', 'ZR', 'ZG', 'ZN',
                                     'ZM' )
                AND mvke2.dwerk = '1130'
                AND mvke2.vkorg = '2000'
        ) IS NOT NULL THEN
            '2000'
        ELSE
            NULL
      --
                     END
    AND marc.werks = CASE
        WHEN mvke1000.dwerk NOT IN ( '1010', ' ', '1110', '1150', '1070',
                                     '1160', '1050', '1030' )
             AND mvke1000.prat1 = 'X'
             AND mvke.vkorg = '1000' THEN
            mvke1000.dwerk
        WHEN marc1090.strgr = '40'
             AND marc1090.mmsta IN ( ' ', '03', 'ZG', 'ZN', 'ZP' )
             AND mvke.vmsta IN ( ' ', 'Z5', 'ZR', 'ZG', 'ZN',
                                 'ZM' )
             AND mvke.vkorg = '1000' THEN
            '1090'
        WHEN marc1140.strgr = '40'
             AND marc1140.mmsta IN ( ' ', '03', 'ZG', 'ZN', 'ZP' )
             AND mvke.vmsta IN ( ' ', 'Z5', 'ZR', 'ZG', 'ZN',
                                 'ZM' )
             AND mvke.vkorg = '1000' THEN
            '1140'
      --
        WHEN marc4000.strgr = '40'
             AND mvke.vmsta IN ( ' ', 'Z5', 'ZR', 'ZG', 'ZN',
                                 'ZM' )
             AND mvke.vkorg = '4000'
             AND marc4000.mmsta IN ( ' ', '03', 'ZG', 'ZN', 'ZP' ) THEN
            '4000'
        WHEN marc1140.mmsta IN ( ' ', '03', 'ZG', 'ZN', 'ZP' )
             AND mvke.vmsta IN ( ' ', 'Z5', 'ZR', 'ZG', 'ZN',
                                 'ZM' )
             AND mvke.vkorg = '1000' THEN
            '1140'
        WHEN marc1090.mmsta IN ( ' ', '03', 'ZG', 'ZN', 'ZP' )
             AND mvke.vmsta IN ( ' ', 'Z5', 'ZR', 'ZG', 'ZN',
                                 'ZM' )
             AND mvke.vkorg = '1000' THEN
            '1090'
      --
        WHEN mvke1000.dwerk NOT IN ( '1010', ' ', '1150', '1160', '1050',
                                     '1030' ) THEN
            mvke1000.dwerk
        WHEN marc4000.mmsta IN ( ' ', '03', 'ZG', 'ZN', 'ZP' ) THEN
            '4000'
        WHEN mvke1000.dwerk = '1050'
             AND mara.mtart = 'ZNFG' THEN
            '1050'
        WHEN marc1130.mmsta IN ( ' ', '03', 'ZG', 'ZN', 'ZP' )
             AND mvke.vmsta IN ( ' ', 'Z5', 'ZR', 'ZG', 'ZN',
                                 'ZM' )
             AND mvke.vkorg = '2000' THEN
            '1130'
        ELSE
            NULL
                     END
    AND (
        SELECT
            decode(marc1.mmsta, ' ', 'OK', marc1.mmsta)
        FROM
            sapecc_dly_librarian.marc marc1
        WHERE
                marc1.mandt = '400'
            AND marc1.werks = soerf.werks
            AND marc1.matnr = mara.matnr
    ) IS NULL
  --       AND soerf.matnr IN ('PN-145508', 'PN-145586')
    AND soerf.werks NOT LIKE '3%'
    AND soerf.werks NOT LIKE '8%'
    AND upper(TRIM(soerf.service)) IN ( 'PLANT EXTENSION', 'SALES ORG EXTENSION', 'PLANT AND SALES ORG EXTENSION',
                                        'COMPONENT EXTENSION TO REPAIR HUB' );

SELECT DISTINCT
    user                                                  AS user_name,
    CASE
        WHEN user = 'DLFERGUS'  THEN
            'dlferguson'
        WHEN user = 'MVANWEE'   THEN
            'MVANWEE'
        WHEN user = 'JZAKRZE'   THEN
            'JAKUB.ZAKRZEWSKI'
        ELSE
            'OES-DQM'
    END                                                   AS user_email,
    'AP  SOERF ' || sysdate                               AS project_name,
    soerf.matnr                                           AS material,
    cat.catlg_no                                          AS catalog_no,
    soerf.vkorg                                           AS sales_org,
    decode((
        SELECT
            konp.kbetr
        FROM
            sapecc_dly_librarian.a304    a304,
            sapecc_dly_librarian.konp    konp
        WHERE
                a304.mandt = '400'
            AND a304.mandt = konp.mandt
            AND a304.matnr = mara.matnr
            AND a304.vkorg = mvke.vkorg
            AND a304.knumh = konp.knumh
            AND to_date(a304.datbi, 'YYYYMMDD') > sysdate
            AND to_date(a304.datab, 'YYYYMMDD') < sysdate
            AND ROWNUM = 1
    ),
           NULL,
           1,
           (
        SELECT
            konp.kbetr
        FROM
            sapecc_dly_librarian.a304    a304,
            sapecc_dly_librarian.konp    konp
        WHERE
                a304.mandt = '400'
            AND a304.mandt = konp.mandt
            AND a304.matnr = mara.matnr
            AND a304.vkorg = mvke.vkorg
            AND a304.knumh = konp.knumh
            AND to_date(a304.datbi, 'YYYYMMDD') > sysdate
            AND to_date(a304.datab, 'YYYYMMDD') < sysdate
            AND ROWNUM = 1
    ))                                                    AS list_price,
    mvke.scmng                                            AS packaging_quantity,
    mvke.mvgr1                                            AS brand,
    mvke.mvgr4                                            AS price_grp,
    decode(mvke.mvgr2, ' ', '000', mvke.mvgr2)            AS available_services,
    CASE
        WHEN mara.mtart = 'ZNFG'
             AND mara.mtpos_mara LIKE 'ZRS%' THEN
            'Y'
        ELSE
            'N'
    END                                                   AS ship_from_plant,
    decode(mvke.prat2, 'X', 'Y', 'N')                     AS cancelable,
    decode(mvke.prat5, 'X', 'Y', 'N')                     AS scheduled_return,
    decode(mvke.prat6, 'X', 'Y', 'N')                     AS preauthorized_return,
    decode(mvke.prat7, 'X', 'Y', 'N')                     AS npsr_required,
    decode(mvke.prat8, 'X', 'Y', 'N')                     AS published,
    decode(mvke.prata, 'X', 'Y', 'N')                     AS sys_auth,
    ''                                                    AS sales_text,
    '11'                                                  AS version
FROM
    sapecc_dly_librarian.mvke                 mvke,
    sapecc_dly_librarian.mara                 mara,
    dqmmfg_librarian.sap_matnr_catlg_no_ax    cat,
    ap_mm_service                             soerf
WHERE
        mvke.mandt (+) = '400'
    AND mara.mandt = '400'
    AND mara.matnr = decode(translate(soerf.matnr, '-0123456789', '-'), '', lpad(soerf.matnr, 18, '0'), soerf.matnr)
    AND mvke.matnr (+) = mara.matnr
    AND mara.mtart IN ( 'ZFG', 'ZTG', 'ZNFG' )
    AND mvke.vkorg = CASE
        WHEN (
            SELECT
                mandt
            FROM
                sapecc_dly_librarian.mvke
            WHERE
                    mandt = '400'
                AND matnr = mara.matnr
                AND vmsta IN ( ' ', 'Z5', 'ZR', 'ZG', 'ZN' )
                AND dwerk <> ' '
                AND vkorg = '1000'
        ) IS NOT NULL THEN
            '1000'
        WHEN (
            SELECT
                mandt
            FROM
                sapecc_dly_librarian.mvke
            WHERE
                    mandt = '400'
                AND matnr = mara.matnr
                AND vmsta IN ( ' ', 'Z5', 'ZR', 'ZG', 'ZN' )
                AND dwerk <> ' '
                AND vkorg = '4000'
        ) IS NOT NULL THEN
            '4000'
        WHEN (
            SELECT
                mandt
            FROM
                sapecc_dly_librarian.mvke
            WHERE
                    mandt = '400'
                AND matnr = mara.matnr
                AND vmsta IN ( ' ', 'Z5', 'ZR', 'ZG', 'ZN' )
                AND dwerk <> ' '
                AND vkorg = '5003'
        ) IS NOT NULL THEN
            '5003'
        ELSE
            '1000'
                     END
    AND cat.matnr (+) = mara.matnr
    AND soerf.vkorg <> '5006'
    AND (
        SELECT
            COUNT(mvke.vkorg)
        FROM
            sapecc_dly_librarian.mvke mvke
        WHERE
                mvke.mandt = '400'
            AND mvke.matnr = mara.matnr
            AND mvke.vkorg = soerf.vkorg
    ) = 0
    AND upper(TRIM(soerf.service)) IN ( 'SALES ORG EXTENSION', 'PLANT AND SALES ORG EXTENSION', 'COMPONENT EXTENSION TO REPAIR HUB' );

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