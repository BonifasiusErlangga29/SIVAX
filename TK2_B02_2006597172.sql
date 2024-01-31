CREATE OR REPLACE FUNCTION CEK_STOK_VAKSIN()
RETURNS TRIGGER AS
$$
DECLARE
STOK_VAKS INTEGER;
EMAIL VARCHAR(50);
BEGIN
SELECT V.STOK, P.EMAIL_ADMIN INTO STOK_VAKS, EMAIL
FROM VAKSIN V, PENJADWALAN P
WHERE P.STATUS = 'pengajuan disetujui' AND
V.KODE = NEW.KODE_VAKSIN;

    IF (TG_OP = 'INSERT') THEN
        IF (STOK_VAKS >= NEW.JUMLAH_VAKSIN) THEN

            INSERT INTO UPDATE_STOK(EMAIL_PEGAWAI, TGL_WAKTU, JUMLAH_UPDATE, KODE_VAKSIN)
            VALUES (EMAIL, NEW.TANGGAL, NEW.JUMLAH_VAKSIN*-1, NEW.KODE_VAKSIN);

            UPDATE VAKSIN
            SET STOK = STOK-NEW.JUMLAH_VAKSIN
            WHERE KODE = NEW.KODE_VAKSIN;

            RETURN NEW;
        ELSE
            RAISE EXCEPTION 'Maaf, stok vaksin tidak mencukupi';
        END IF;
    END IF;
END;
$$
LANGUAGE PLPGSQL;

-- COLABORATOR : 
-- Nyoman Bagus Nuartha Dananjaya 2006597153
-- Robertus Aditya Sukoco 2006523016