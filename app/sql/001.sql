 CREATE TABLE public.shorturl_tab (
        id BIGSERIAL NOT NULL, 
        shorturl_status SMALLINT NOT NULL, 
        shorturl_user_id BIGINT NOT NULL, 
        shorturl_origin VARCHAR(1024) NOT NULL, 
        shorturl_code VARCHAR(64) NOT NULL, 
        PRIMARY KEY (id)
);


CREATE INDEX idx_shorturl_status ON public.shorturl_tab (shorturl_status);
CREATE INDEX idx_shorturl_code ON public.shorturl_tab (shorturl_code);
CREATE INDEX idx_shorturl_user_id ON public.shorturl_tab (shorturl_user_id);


INSERT INTO system_tab (system_update, system_name, system_value) VALUES (extract(epoch from now()), 'SQL', '001.sql');


