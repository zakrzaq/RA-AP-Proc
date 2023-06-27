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
        ) IS NOT NULL )
