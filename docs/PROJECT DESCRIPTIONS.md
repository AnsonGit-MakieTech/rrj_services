# RRJ Services Project Description

## Project Summary

RRJ Services is a Django web application for managing construction, renovation,
repair, and maintenance service bookings. It gives customers a structured way to
request services, upload project images, receive quotations, submit payment
proof, and track project progress. It gives admins a centralized dashboard for
reviewing incoming bookings, managing services, sending quotations, verifying
payments, updating job status, and chatting with customers.

The project is built as a practical MVP for a service business. The core goal is
to replace scattered phone/chat/manual booking workflows with a database-backed
system that preserves customer history, quotation history, payment state, and
project status.

## Business Purpose

The system supports the real revenue workflow of a service company:

1. Customer registers or logs in using name and contact number.
2. Customer browses available services.
3. Customer submits a booking request with details and multiple images.
4. Admin reviews the request and sends a quotation.
5. Customer accepts or rejects the quotation.
6. Customer submits payment proof after accepting.
7. Admin verifies payment.
8. Admin schedules and updates project progress.
9. Customer and admin communicate through the booking message thread.

This is an inquiry-to-booking platform, not a full ERP. The current scope is
correct for MVP validation because it focuses on bookings, quotations, payments,
communication, and operational visibility.

## Target Users

| User Type | Purpose |
| --- | --- |
| Customer | Request a service, upload project details, approve quotation, submit payment proof, track status, and chat with admin. |
| Admin staff | Manage service catalog, review bookings, send quotations, verify payments, update project status, and respond to customers. |
| Business owner | Monitor service demand, active bookings, revenue pipeline, completed jobs, and customer communication. |

## Tech Stack

| Layer | Technology |
| --- | --- |
| Backend | Django 4.2 |
| Database | SQLite by default |
| Authentication | Django auth with custom `AuthenticatedUser` model |
| Frontend | Django templates, static CSS, vanilla JavaScript |
| Static files | Django static files plus WhiteNoise |
| Media uploads | Django `MEDIA_ROOT` and `MEDIA_URL` |
| Testing | Django `TestCase` suite |

## Project Structure

```text
rrj_services/
  rrj_services/
    settings.py
    urls.py
    wsgi.py
    asgi.py

  base/
    models.py
    views.py
    urls.py
    admin.py
    booking_context.py
    service_context.py
    system_context.py
    user_context.py
    tests.py

  apis/
    authentications.py
    manage_booking.py
    manage_service.py
    manage_system_settings.py
    admin_dashboard.py
    my_booking.py
    booking_messaging.py
    booking_transactions.py

  templates/
    404.html
    base/
      home.html
      login.html
      register.html
      services.html
      add_booking.html
      my_bookings.html
      view_booking.html
      admin.html
      admin_view_booking.html
      settings.html
      includes/
        header.html
        footer.html
        booking_messages_panel.html

  static/
    css/home.css
    js/
      authentication.js
      home.js
      services.js
      add_booking.js
      my_booking.js
      admin.js
      settings.js
      booking_messaging.js
      booking_transactions.js
      dashboard-charts.js
    assets/

  media/
    attachments/
    receipts/
    services/
```

## Architecture

The application uses a simple Django architecture with separated responsibilities:

| Area | Responsibility |
| --- | --- |
| `base/models.py` | Database models and model-level display helpers. |
| `base/views.py` | Page rendering and route-level access control. |
| `base/*_context.py` | Page context helpers for users, services, system settings, and booking workflow state. |
| `apis/*.py` | POST endpoints and business actions. |
| `templates/base/*.html` | Page templates. |
| `static/js/*.js` | Page-specific frontend behavior. |
| `static/css/home.css` | Shared UI styling for the full site. |

This keeps page rendering thin while moving business actions into dedicated API
modules. It also keeps JavaScript separated by page, which makes the frontend
easier to maintain as more features are added.

## Core Models

### `AuthenticatedUser`

Extends Django `AbstractUser`.

Important fields:

- `full_name`
- `contact_number`
- `full_address`
- inherited `is_staff`

Admin separation is based on Django staff status:

- `is_staff=True` means the user is an admin and can access admin pages.
- `is_staff=False` means the user is a customer.

### `SystemSettings`

Stores homepage marketing copy.

Fields:

- `tagline`
- `description`

The home page uses database values when present. Empty fields fall back to the
default text. Admins can update this from `/settings/` through the Homepage
Content modal.

### `Service`

Stores services shown to customers and managed by admins.

Fields:

- `name`
- `description`
- `min_price`
- `max_price`
- `is_active`
- `image`
- `image_url`
- `is_deleted`
- `status`

Important behavior:

- `price_range` formats service pricing for display.
- `display_image_url` prioritizes uploaded image, then external image URL.
- `is_deleted=True` hides deleted services without removing historical booking data.
- `is_active=False` hides services from customer-facing lists.

### `BookingRequest`

Stores customer booking requests and transaction state.

Main field groups:

- System fields: `owner`, `progress`, `reference_number`, timestamps.
- Customer fields: `full_name`, `email`, `contact_number`, `full_address`.
- Service fields: `service`, `urgency_level`, `preferred_date`, `square_meters`,
  `project_location`, `service_description`, `problem_description`.
- Quotation fields: `material_cost`, `labor_cost`, `total_cost`,
  `transaction_notes`.
- Payment fields: `amount_paid`, `payment_method`,
  `payment_reference_number`, `receipt_screenshot`, `approved_payment`.

### `BookingAttachment`

Stores multiple uploaded project images/files per booking.

Fields:

- `booking_request`
- `file`
- timestamps

### `ChatMessage`

Stores booking-level conversation between customer and admin.

Fields:

- `booking_request`
- `message`
- `sender`
- `receiver`
- timestamps

## Main Pages

| URL | Page | Access |
| --- | --- | --- |
| `/login/` | Login page | Guest only |
| `/register/` | Registration page | Guest only |
| `/` | Home page | Logged-in users |
| `/services/` | Service catalog | Logged-in users |
| `/add-booking/` | Create booking | Logged-in users |
| `/my-bookings/` | Booking list | Customers see own bookings; admins see all received bookings |
| `/my-bookings/<reference>/` | Customer booking detail | Booking owner only |
| `/admin-dashboard/` | Admin dashboard | Staff only |
| `/admin-dashboard/bookings/<reference>/` | Admin booking detail | Staff only |
| `/settings/` | Service and system settings | Staff only |
| Unknown URL | Custom 404 page | Guest or logged-in users |

## API Endpoints

### Authentication

| Endpoint | Purpose |
| --- | --- |
| `POST /api/login/` | Login using full name and contact number. |
| `POST /api/register/` | Register a customer and automatically log them in. |
| `/logout/` | Logout and return to login page. |

### Booking

| Endpoint | Purpose |
| --- | --- |
| `POST /api/bookings/create/` | Create booking request with multiple attachments. |
| `GET/POST /api/bookings/<reference>/messages/` | Load or send booking messages. |
| `POST /api/bookings/<reference>/quotation/` | Admin submits quotation. |
| `POST /api/bookings/<reference>/quotation/decision/` | Customer accepts or rejects quotation. |
| `POST /api/bookings/<reference>/payment/` | Customer submits payment proof. |
| `POST /api/bookings/<reference>/payment/verify/` | Admin approves or rejects payment. |
| `POST /api/bookings/<reference>/status/` | Admin updates operational status. |

### Service and System Settings

| Endpoint | Purpose |
| --- | --- |
| `POST /api/services/create/` | Admin creates a service. |
| `POST /api/services/update/` | Admin edits a service. |
| `POST /api/services/<id>/toggle/` | Admin toggles service visibility. |
| `POST /api/services/<id>/delete/` | Admin soft-deletes a service. |
| `POST /api/system-settings/update/` | Admin updates homepage tagline and description. |

## Booking Lifecycle

The booking lifecycle is implemented through `BookingRequest.progress`.

```text
pending_quotation
  -> quotation_sent
  -> waiting_for_payment
  -> payment_verification
  -> booking_confirmed
  -> scheduled
  -> in_progress
  -> completed
```

Important branch behavior:

- Customer rejects a quotation: `quotation_sent -> pending_quotation`
- Admin rejects payment: `payment_verification -> waiting_for_payment`
- Admin can schedule confirmed booking: `booking_confirmed -> scheduled`
- Admin can start work: `scheduled -> in_progress`
- Admin can complete work from scheduled or in progress.
- Admin can move `in_progress -> scheduled` for rescheduling.

Allowed operational status updates are intentionally restricted in
`apis/booking_transactions.py` to avoid invalid project states.

## Admin Dashboard

The admin dashboard summarizes live booking operations:

- Total bookings
- Pending quotation count
- Payment verification count
- Confirmed/active work count
- Completed count
- Recent bookings
- Status filters
- Monthly and service-based chart data

The dashboard is based on real `BookingRequest` database records.

## Messaging

Messaging is booking-scoped, not global.

Rules:

- Customers can message admins inside their own booking.
- Admins can message customers inside any booking.
- Customers cannot access another customer's booking messages.
- Messages are stored in `ChatMessage`.
- Shared UI lives in `templates/base/includes/booking_messages_panel.html`.
- Frontend behavior lives in `static/js/booking_messaging.js`.

## File Uploads

The project supports uploaded media:

- Service images: `media/services/`
- Booking attachments: `media/attachments/`
- Payment receipts: `media/receipts/`

Development serving is configured in `rrj_services/urls.py` when `DEBUG=True`.
Production deployments must serve media files through the web server or object
storage. WhiteNoise is for static assets, not user-uploaded media.

## Authentication and Access Control

The application uses Django sessions.

Important access rules:

- Most pages require login through `@login_required`.
- Admin pages require `request.user.is_staff`.
- Customers only view their own booking detail pages.
- Admins can view all bookings from the admin dashboard and admin booking page.
- Management endpoints raise 404 for unauthorized users.

This approach hides admin-only surfaces from customers without exposing whether
specific admin resources exist.

## Frontend Organization

JavaScript is separated by page or feature:

| File | Purpose |
| --- | --- |
| `authentication.js` | Login/register async handling and loading states. |
| `home.js` | Shared navigation/header interactions. |
| `services.js` | Service search/filter behavior. |
| `add_booking.js` | Booking form, custom selects, date UX, image uploads, confirmation modal. |
| `my_booking.js` | Booking list search and status filtering. |
| `admin.js` | Admin dashboard filters and controls. |
| `settings.js` | Settings page modals, service CRUD UI, homepage content modal. |
| `booking_messaging.js` | Booking chat send/load behavior. |
| `booking_transactions.js` | Quotation, payment, and status action submissions. |
| `dashboard-charts.js` | Dashboard chart rendering. |

This structure should be preserved. New page-specific behavior should get its
own JS file unless it is truly shared across multiple pages.

## Styling

Most styling is currently centralized in:

```text
static/css/home.css
```

The design uses:

- RRJ violet/pink brand colors.
- White and soft violet surfaces.
- Compact admin tables.
- Modal-based management forms.
- Responsive layouts for mobile and desktop.

Future improvement: split CSS by feature or page after the system stabilizes,
because `home.css` is now serving as a global stylesheet.

## Deployment Notes

Current deployment-relevant settings:

- `STATIC_ROOT = BASE_DIR / "staticfiles"`
- `STATICFILES_DIRS = [BASE_DIR / "static"]`
- `STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"`
- `MEDIA_URL = "/media/"`
- `MEDIA_ROOT = BASE_DIR / "media"`
- `DEBUG` and `ALLOWED_HOSTS` come from `.env`

Production checklist:

1. Set `DEBUG=False`.
2. Set a real `SECRET_KEY`.
3. Set correct `ALLOWED_HOSTS`.
4. Run `python manage.py collectstatic`.
5. Configure persistent media storage.
6. Use a production database instead of SQLite when traffic and operational risk grow.
7. Enable HTTPS.
8. Add error monitoring and backup strategy.

## Testing

The project includes Django tests in:

```text
base/tests.py
```

Covered areas include:

- Authentication pages and APIs.
- Page protection.
- Home/system settings behavior.
- Custom 404 page.
- Admin dashboard.
- Service settings and service CRUD.
- Add booking with multiple images.
- My bookings page.
- Customer/admin booking detail pages.
- Messaging.
- Quotation, payment, and status transitions.

Run tests with:

```bash
python manage.py test
```

Run Django system checks with:

```bash
python manage.py check
```

## Current Strengths

- Real booking lifecycle exists from request to completion.
- Admin and customer access are separated using `is_staff`.
- Service catalog is database-backed.
- Homepage copy is database-backed through `SystemSettings`.
- Booking detail pages no longer rely on hard-coded sample data.
- Messaging and transaction history are tied to bookings.
- The test suite covers major workflows.

## Known Technical Debt

- SQLite is acceptable for local/MVP use, but not ideal for production scale.
- CSS is centralized in one large stylesheet and should eventually be split.
- The current login model is convenient but weak because it uses full name and
  contact number without password or OTP verification.
- Uploaded media is stored locally. Production needs persistent media storage.
- Payment proof verification is manual. This is acceptable for MVP but can be
  integrated with payment provider APIs later.
- Admin permissions are currently binary through `is_staff`. More granular roles
  may be needed if operations staff, sales staff, and owners need different
  permissions.

## Recommended Next Improvements

1. Add OTP verification for login/register to secure contact-number auth.
2. Add notification delivery through SMS, email, or Messenger for quotation and
   payment updates.
3. Add admin assignment for bookings so staff can own requests.
4. Add audit log entries for quotation, payment, and status changes.
5. Move production media to cloud storage.
6. Add export/reporting for bookings and revenue.
7. Split CSS into page-level files after the UI stabilizes.
8. Add a business-facing dashboard for monthly revenue, conversion rate, and
   service demand.

