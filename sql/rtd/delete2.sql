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
    ) IS NOT NULL