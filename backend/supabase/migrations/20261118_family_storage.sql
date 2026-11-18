begin;
-- The bucket is provisioned through the Storage API, not by changing its tables.
create policy family_portrait_insert on storage.objects for insert to authenticated
 with check(bucket_id='family-portraits' and (storage.foldername(name))[1]=auth.uid()::text and public.family_can_upload());
create policy family_portrait_own_select on storage.objects for select to authenticated
 using(bucket_id='family-portraits' and (storage.foldername(name))[1]=auth.uid()::text and public.family_can_upload());
-- No client overwrite or deletion: older photographs must remain recoverable.
commit;
