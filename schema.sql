BEGIN;
TRUNCATE "service_serviceorder", "auth_group_permissions", "inventory_employee", "django_content_type", "django_session", "inventory_client", "service_serviceitem", "auth_group", "inventory_car", "inventory_company", "service_service_service_items", "finance_serviceinvoice", "finance_invoiceserviceitem", "service_service", "service_serviceitemorder", "auth_permission" RESTART IDENTITY;
COMMIT;
