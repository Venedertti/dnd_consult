-- Criação do banco de dados root
CREATE DATABASE root;

-- Conectando ao banco root
\c root;

-- Criação do usuário root
DO $$
BEGIN
    CREATE ROLE root WITH LOGIN PASSWORD 'ImRoot_2024';
    ALTER ROLE root CREATEDB;
END $$;

\c dnd_consult;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'classes') THEN
        CREATE TABLE public.classes (
            "name" varchar(100) NOT NULL,
            "type" varchar(100) NOT NULL,
            "source" varchar(255) NOT NULL,
            CONSTRAINT classes_pkey PRIMARY KEY ("name")
        );
    END IF;

    IF NOT EXISTS (SELECT 1 FROM public.classes) THEN
        INSERT INTO public.classes
            ("name", "type", "source")
        VALUES 
            ('Artificer', 'Hybrid', 'Tasha'),
            ('Barbarian', 'Martial', 'BHB'),
            ('Bard', 'Magical', 'BHB'),
            ('Cleric', 'Magical', 'BHB'),
            ('Druid', 'Magical', 'BHB'),
            ('Fighter', 'Martial', 'BHB'),
            ('Monk', 'Martial', 'BHB'),
            ('Paladin', 'Hybrid', 'BHB'),
            ('Ranger', 'Hybrid', 'BHB'),
            ('Rogue', 'Martial', 'BHB'),
            ('Sorcerer', 'Magical', 'BHB'),
            ('Warlock', 'Magical', 'BHB'),
            ('Wizard', 'Magical', 'BHB');
    END IF;
END $$;

GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.classes TO root;

GRANT ALL PRIVILEGES ON DATABASE dnd_consult TO root;
