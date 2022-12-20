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