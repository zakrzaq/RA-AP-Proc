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