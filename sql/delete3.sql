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
    ) IS NOT NULL )