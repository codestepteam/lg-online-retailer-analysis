WITH candidates(row_no, url_key) AS (
    VALUES
    (1502, 'amazon.it/dp/b0hdtjkcgd'),
    (2555, 'amazon.it/dp/b0hkzjvj7c'),
    (2556, 'amazon.it/dp/b0hkzv7r3y'),
    (5977, 'amazon.de/dp/b0hkk5ltxw'),
    (5978, 'amazon.de/dp/b0hnt2d6fj'),
    (5979, 'amazon.de/dp/b0hnt5kc6n'),
    (5980, 'amazon.de/dp/b0hnt6zljc'),
    (5981, 'amazon.de/dp/b0hnt9q1jb'),
    (5982, 'amazon.de/dp/b0hntb2lt4'),
    (5983, 'amazon.de/dp/b0hntb3tgl'),
    (5984, 'amazon.de/dp/b0hntcx4dz'),
    (5985, 'amazon.de/dp/b0hntfzjlm'),
    (6141, 'amazon.de/dp/b0d41lwyy7'),
    (6283, 'mediamarkt.de/de/product/_siemens-wg-44-g-2-zem-wq-43-g-2-d-0-em-3066916.html'),
    (8791, 'falabella.com/falabella-cl/product/80744156/apilable-de-lavadora-secado/80744156'),
    (57337, 'momoshop.com.tw/product/12305064'),
    (57414, 'momoshop.com.tw/product/13434867'),
    (12706, 'mediamarkt.nl/nl/product/_samsung-ww90dg6u25lku3-6000-serie-samsung-dv90dg6845lku3-samsung-stapelkit-wasmaschine-droogkast-bundel-1897575.html'),
    (21409, 'alza.cz/lg-fsr7a04wc-lg-rc91v9avsn-d12448707.htm'),
    (21410, 'alza.cz/lg-fsr7a04wc-lg-rc91v5av6n-d12448706.htm'),
    (21411, 'alza.cz/lg-fsr7a04wc-lg-rc91v9av4n-d13196651.htm'),
    (21412, 'alza.cz/lg-fsr7a04wc-lg-rc81v9av3n-d13550734.htm'),
    (21413, 'alza.cz/lg-fsr5a94wl-lg-rc8tv9avhn-d13590198.htm'),
    (21414, 'alza.cz/lg-fpsr5a14wl-lg-rc8tv9avhn-d13196649.htm'),
    (21415, 'alza.cz/samsung-dv90dg52a0able-samsung-ecobubble-ww11dg5b25able-d13597707.htm'),
    (21417, 'alza.cz/lg-fsr5a94wh-lg-rc91v5av6n-d13196648.htm'),
    (21420, 'alza.cz/bosch-wgg242z2cs-serie-6-bosch-wqg243d9cs-serie-6-d13191272.htm'),
    (21425, 'alza.cz/samsung-ww11dg6b85lku4-samsung-dv90dg6845lhu4-d13095726.htm'),
    (21426, 'alza.cz/aeg-7000-prosteam-lfr73964cc-aeg-9000-absolutecare-plus-3dscan-tr9394c-d13004427.htm'),
    (21427, 'alza.cz/lg-fsr7a04pg-lg-rc91v9ev2n-d8609133.htm'),
    (21429, 'alza.cz/lg-fasr3a04ww-lg-rc81v9av3n-d13550733.htm'),
    (21430, 'alza.cz/lg-fasr3a04ww-lg-rc91v9avsn-d13196650.htm'),
    (21432, 'alza.cz/aeg-7000-prosteam-lfr73964cc-aeg-7000-prosteam-lfr71862sbc-d13476143.htm'),
    (21433, 'alza.cz/aeg-7000-prosteam-lfr73964cc-aeg-7000-prosteam-lfr73964cc-d13476142.htm'),
    (21434, 'alza.cz/aeg-7000-prosteam-lfr73964cc-aeg-6000-prosense-lfr61864bc-d13476144.htm'),
    (21435, 'alza.cz/bosch-wgg244f2by-serie-6-bosch-wqg243d9cs-serie-6-d13191273.htm'),
    (21436, 'alza.cz/aeg-6000-prosense-lfr61942bc-aeg-8000-absolutecare-tr8182c-d12958646.htm'),
    (21438, 'alza.cz/bosch-wgb25602cs-serie-8-bosch-wqb246dmby-serie-8-d13191275.htm'),
    (21440, 'alza.cz/samsung-ww80cgc04dable-samsung-dv90dg52a0able-d13095724.htm'),
    (21442, 'alza.cz/lg-f4x7513tlb-lg-rhx7009tlb-d13368087.htm'),
    (21444, 'alza.cz/bosch-wgg244zreu-serie-6-bosch-wqg245dreu-serie-6-d13191266.htm'),
    (21446, 'alza.cz/bosch-wgb24410by-serie-8-bosch-wqb246dmby-serie-8-d13191271.htm'),
    (21447, 'alza.cz/lg-f4x5013tlc-lg-rhx5008tlb-d13550736.htm'),
    (21448, 'alza.cz/samsung-ww10fg5u34aele-samsung-dv90dg52a0tele-d13095735.htm'),
    (21449, 'alza.cz/samsung-ww11dg5b25aele-samsung-dv90dg52a0tele-d12920996.htm'),
    (21450, 'alza.cz/samsung-ww90cgc04dtele-samsung-dv90dg52a0tele-d12920994.htm'),
    (21451, 'alza.cz/samsung-ww80cgc04daele-samsung-dv90dg52a0tele-d12920995.htm'),
    (21457, 'alza.cz/samsung-wf90f09c4su4-samsung-dv90f09f4su4-d13095728.htm'),
    (21458, 'alza.cz/samsung-bespoke-ai-dv90f09f4su4-samsung-bespoke-ai-wf90f09c4su4-d13355589.htm'),
    (21459, 'alza.cz/lg-f0p3cyv2w-lg-rh18u8avcw-d13196652.htm'),
    (21460, 'alza.cz/samsung-bespoke-ai-wf90h11c4st2-11-kg-samsung-bespoke-ai-dv90f09f4su4-d13597706.htm'),
    (21461, 'alza.cz/lg-f4x5009tbb-lg-rhx5008tbb-d13368088.htm'),
    (21462, 'alza.cz/lg-f4x7011tsb-lg-rhx7009tsb-d13368090.htm'),
    (21463, 'alza.cz/bosch-wgg244z9by-serie-6-bosch-wqg24591by-serie-6-d13191277.htm'),
    (23438, 'mediaexpert.pl/agd/pralki-i-suszarki/pralki/pralka-bosch-serie-6-wgj244a9pl-9kg-1400-obr-polska-produkcja-autodozowanie-minipranie-homeconnect-program-parowy-suszar-1'),
    (23442, 'mediaexpert.pl/agd/pralki-i-suszarki/pralki/pralka-hisense-wf7s1247bb-seria-7s-12kg-1400-obr-wi-fi-connectlife-autodozowanie-ai-superwash-ekran-tft-smart-assist-sus'),
    (23596, 'mediaexpert.pl/agd/pralki-i-suszarki/pralki/pralka-hisense-wf7s1247bw-seria-7s-12kg-1400-obr-wi-fi-connectlife-autodozowanie-ai-superwash-ekran-tft-smart-assist-sus'),
    (46400, 'falabella.com.pe/falabella-pe/product/155297471/combo-samsung-centro-de-lavado-10-5kg-9kg-f-dv90cgc2a-01/155297472'),
    (55545, 'electroplanet.ma/p1368760-siera-c1049s.html')
), operation_urls AS (
    SELECT o.revision, u.retailer, u.retailer_product_id, u.url,
           u.page_summary->>'final_url' AS final_url,
           u.page_summary->>'captured_at' AS captured_at,
           u.page_summary->>'http_status' AS http_status
    FROM lg_registry.operation_urls u
    JOIN lg_registry.operations o ON o.operation_id = u.operation_id
    WHERE u.operation_id = 'op-20261029-01' AND u.scenario = 'pdp'
)
SELECT DISTINCT c.row_no, u.revision, u.retailer, u.retailer_product_id,
       u.url, u.final_url, u.captured_at, u.http_status
FROM candidates c
JOIN operation_urls u ON c.url_key IN (
    lower(rtrim(regexp_replace(split_part(u.url, '?', 1), '^https?://(www[.])?', '', 'i'), '/')),
    lower(rtrim(regexp_replace(split_part(u.final_url, '?', 1), '^https?://(www[.])?', '', 'i'), '/')),
    CASE WHEN u.retailer = 'momoshop' THEN 'momoshop.com.tw/product/' || u.retailer_product_id END
)
ORDER BY c.row_no, u.url
