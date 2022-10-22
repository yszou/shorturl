CREATE TABLE public.user_tab (
        id BIGSERIAL NOT NULL, 
        user_type VARCHAR(16) NOT NULL, 
        user_status VARCHAR(16) NOT NULL, 
        user_parent_id BIGINT NOT NULL, 
        user_name VARCHAR(32) NOT NULL, 
        user_avatar VARCHAR(128) NOT NULL, 
        user_mobile VARCHAR(24) NOT NULL, 
        user_email VARCHAR(128) NOT NULL, 
        user_create BIGINT NOT NULL, 
        PRIMARY KEY (id)
);


CREATE INDEX idx_user_status ON public.user_tab (user_status);
CREATE INDEX idx_user_parent_id ON public.user_tab (user_parent_id);
CREATE INDEX idx_user_type ON public.user_tab (user_type);


CREATE TABLE public.system_tab (
        id SERIAL NOT NULL, 
        system_update BIGINT NOT NULL, 
        system_name VARCHAR(32) NOT NULL, 
        system_value TEXT NOT NULL, 
        PRIMARY KEY (id)
);


CREATE INDEX idx_system_name ON public.system_tab (system_name);

CREATE TABLE public.session_tab (
        id BIGSERIAL NOT NULL, 
        session_sid VARCHAR(32) NOT NULL, 
        session_user_id BIGINT, 
        session_create BIGINT NOT NULL, 
        session_ip VARCHAR(64) NOT NULL, 
        session_other TEXT NOT NULL, 
        session_token VARCHAR(32) NOT NULL, 
        session_token_expire BIGINT NOT NULL, 
        session_captcha VARCHAR(16) NOT NULL, 
        session_captcha_create BIGINT NOT NULL, 
        PRIMARY KEY (id)
);


CREATE INDEX idx_session_sid ON public.session_tab (session_sid);
CREATE INDEX idx_session_user_id ON public.session_tab (session_user_id);
CREATE INDEX idx_session_token ON public.session_tab (session_token);


CREATE TABLE public.account_tab (
        id BIGSERIAL NOT NULL, 
        account_user_id BIGINT NOT NULL, 
        account_type VARCHAR(16) NOT NULL, 
        account_status VARCHAR(16) NOT NULL, 
        account_username VARCHAR(32) NOT NULL, 
        account_password VARCHAR(80) NOT NULL, 
        account_create BIGINT NOT NULL, 
        account_other TEXT NOT NULL, 
        PRIMARY KEY (id)
);


CREATE INDEX idx_account_user_id ON public.account_tab (account_user_id);
CREATE INDEX idx_account_status ON public.account_tab (account_status);
CREATE INDEX idx_account_type ON public.account_tab (account_type);


INSERT INTO system_tab (system_update, system_name, system_value) VALUES (extract(epoch from now()), 'SQL', '000.sql');
