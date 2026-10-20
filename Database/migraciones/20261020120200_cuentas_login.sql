-- Cuentas del login de Leadify (backend: Demo/backend/api/acceso.py).
--
-- El login lo maneja NUESTRO backend (FastAPI) y las cuentas viven en Postgres: no se usa Supabase Auth.
-- Una cuenta = una empresa (constructora o inmobiliaria).
--
-- SIN CONFIRMACIÓN DE CORREO NI REVISIÓN: la cuenta nace 'aprobada' y entra en el acto. 'pendiente' y
-- 'rechazada' existen para poder cerrar una cuenta a mano desde la base.
--
-- SEGURIDAD
--   * Esquema propio `acceso`: la API pública de Supabase (PostgREST) solo expone `public`, así que estas
--     tablas no son alcanzables con la clave publicable aunque alguien la tenga.
--   * Además, RLS activado sin políticas y todo privilegio revocado a anon/authenticated.
--   * El ÚNICO que entra es el backend, por conexión directa de Postgres con `DATABASE_URL`, que vive solo
--     en las variables de entorno de Render.
--   * Nada en claro que sirva para entrar: la contraseña va con scrypt (sal propia por cuenta) y de las
--     sesiones solo se guarda el SHA-256 del token.
--
-- Las tablas de leads no se tocan.

create schema if not exists acceso;

revoke all on schema acceso from public, anon, authenticated;

-- ---------------------------------------------------------------------------
-- 1. CUENTAS
-- ---------------------------------------------------------------------------

create table acceso.cuentas (
  id             uuid primary key default gen_random_uuid(),
  usuario        text not null unique
                   check (char_length(usuario) between 3 and 30 and usuario ~ '^[a-z0-9]([a-z0-9._-]*[a-z0-9])?$'),
  correo         text not null unique
                   check (correo = lower(correo) and char_length(correo) <= 254 and correo ~ '^[^@\s]+@[^@\s]+\.[^@\s]{2,}$'),
  clave_hash     text not null,
  estado         text not null default 'aprobada'
                   check (estado in ('pendiente', 'aprobada', 'rechazada')),
  tipo           text check (tipo in ('constructora', 'inmobiliaria')),
  creada_en      timestamptz not null default now(),
  actualizada_en timestamptz not null default now()
);

comment on table acceso.cuentas is
  'Una fila por empresa con cuenta en el login. La contraseña va con scrypt en clave_hash; '
  'el backend nunca la devuelve.';

create function acceso.tocar_actualizada_en()
returns trigger
language plpgsql
set search_path = acceso, pg_temp
as $$
begin
  new.actualizada_en := now();
  return new;
end;
$$;

create trigger cuentas_actualizada_en
  before update on acceso.cuentas
  for each row
  execute function acceso.tocar_actualizada_en();

-- ---------------------------------------------------------------------------
-- 2. SESIONES
-- ---------------------------------------------------------------------------

create table acceso.sesiones (
  hash       text primary key check (hash ~ '^[0-9a-f]{64}$'),   -- SHA-256 del valor de la cookie
  cuenta_id  uuid not null references acceso.cuentas (id) on delete cascade,
  recordar   boolean not null default false,
  expira     timestamptz not null,
  creada_en  timestamptz not null default now()
);

create index sesiones_cuenta_idx on acceso.sesiones (cuenta_id);
create index sesiones_expira_idx on acceso.sesiones (expira);

-- ---------------------------------------------------------------------------
-- 3. INTENTOS FALLIDOS (tope de 5 por correo en 15 minutos)
-- ---------------------------------------------------------------------------
-- En la base y no en memoria: sobrevive a un redespliegue y sirve si hay más de una instancia.

create table acceso.intentos (
  id     bigint generated always as identity primary key,
  correo text not null,
  en     timestamptz not null default now()
);

create index intentos_correo_en_idx on acceso.intentos (correo, en desc);

-- ---------------------------------------------------------------------------
-- 4. CERRADO PARA TODOS MENOS EL BACKEND
-- ---------------------------------------------------------------------------

alter table acceso.cuentas  enable row level security;
alter table acceso.sesiones enable row level security;
alter table acceso.intentos enable row level security;

revoke all on all tables    in schema acceso from public, anon, authenticated;
revoke all on all sequences in schema acceso from public, anon, authenticated;
revoke all on all functions in schema acceso from public, anon, authenticated;
