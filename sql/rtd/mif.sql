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
                                        'COMPONENT EXTENSION TO REPAIR HUB' )