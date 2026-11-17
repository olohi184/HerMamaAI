-- Run in a new Supabase project SQL editor. Do not use a service-role key in the app.
create table if not exists public.wellness_checkins (
 user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
 date date not null,
 goal text not null,
 context text not null,
 energy text not null check (energy in ('Low','Moderate','High')),
 restart boolean not null,
 completed boolean not null,
 sleep text not null check (sleep in ('Restful','Interrupted','Poor')),
 stress text not null check (stress in ('Low','Moderate','High')),
 primary key(user_id,date,goal)
);
alter table public.wellness_checkins enable row level security;
revoke all on public.wellness_checkins from anon;
grant select,insert,update,delete on public.wellness_checkins to authenticated;
create policy "own wellness records" on public.wellness_checkins for all to authenticated using (auth.uid() = user_id) with check (auth.uid() = user_id);
