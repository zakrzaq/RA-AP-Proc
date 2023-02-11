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
    ) IS NOT NULL