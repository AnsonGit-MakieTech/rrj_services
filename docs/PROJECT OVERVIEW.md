# RRJ Services Booking System - Project Overview

## Product Summary

RRJ Services is a web-based booking and project tracking system for construction,
renovation, and maintenance services in the Philippines. The public-facing landing
page promotes professional service delivery, estimated price ranges, transparent
quotations, and real-time project tracking.

The product turns website visitors into qualified service inquiries, converts
approved quotations into booked projects, and gives staff a structured way to
manage requests, schedules, progress, and customer communication.

**Working brand note:** The supplied landing page uses the name `BuildPro
Services`. The implementation should use one final brand consistently before
launch. Until confirmed, `RRJ Services` is the system/project name and
`BuildPro` is treated as draft landing-page copy.

## Real Problem

Construction and home-service bookings are commonly handled through chat,
phone calls, and manual spreadsheets. This causes:

- Slow quotation turnaround and lost inquiries.
- Unclear pricing expectations before site inspection.
- Double bookings or poor schedule visibility.
- Customers repeatedly asking for project updates.
- No reliable history of client requests, quotations, and completed work.

RRJ Services solves this by capturing structured booking requests online,
managing quotation approval, and tracking the work from inquiry to completion.

## Target Users

| User | Need |
| --- | --- |
| Homeowners and condo owners | Request renovation or repair work and understand estimated cost. |
| Commercial property owners/managers | Book reliable work and track active projects. |
| Office administrator/sales staff | Review leads, schedule visits, prepare quotations, and confirm bookings. |
| Operations/project staff | Update schedule and job progress. |
| Business owner | Monitor leads, conversion, revenue pipeline, and completed projects. |

## Best Strategy

Launch an inquiry-to-booking MVP first. Do not initially build a full
construction ERP, complex materials inventory, contractor payroll, or automated
pricing engine.

The highest-value workflow is:

1. Customer finds a service through the landing page.
2. Customer submits project details and requests a free quotation.
3. Admin reviews the request and arranges a site inspection if required.
4. Admin sends a formal quotation.
5. Customer accepts the quotation and the job is scheduled.
6. Staff updates project status so the customer can track progress.

This workflow directly supports revenue and establishes operational data before
adding automation.

## Landing Page Direction

### Hero Message

- Trust indicator: `Trusted by 500+ clients`
- Headline: `Build Better. Maintain Smarter.`
- Supporting copy: Professional construction and maintenance services available
  through online booking, quotations, and real-time project tracking.
- Primary CTA: `Book a Service`
- Secondary CTA: `Browse Services`
- Trust points: `Licensed & Insured`, `On-Time Delivery`, `Quality Guarantee`

### Featured Services

| Service | Description | Displayed Estimate |
| --- | --- | ---: |
| Condo Renovation | Layout changes, finishes, and fixtures for condominium units. | PHP 50,000 - PHP 500,000 |
| House Renovation | Structural work, interior finishing, and exterior improvements. | PHP 100,000 - PHP 1,000,000 |
| Cabinet Maker/Design | Custom cabinets for kitchens, bedrooms, and storage. | PHP 15,000 - PHP 120,000 |
| Wall Partition Maker | Drywall and partition installation for rooms and offices. | PHP 8,000 - PHP 60,000 |
| Landscaping Design | Landscape design and garden installation. | PHP 20,000 - PHP 200,000 |
| Repainting | Interior and exterior professional painting work. | PHP 5,000 - PHP 80,000 |
| Shower Enclosure Install | Custom glass shower enclosure design and installation. | PHP 12,000 - PHP 50,000 |
| Glass Door Install | Tempered glass door installation for homes and commercial spaces. | PHP 10,000 - PHP 45,000 |

These values are marketing estimates only. The booking flow must make clear that
the final price depends on measurements, materials, design, location, and site
inspection.

### Trust and Conversion Sections

- Why choose us: expert craftsmen, transparent pricing, real-time tracking.
- Testimonials: initial landing page has three draft customer testimonials.
- Closing CTA: free quotation request with phone, email, and service location.
- Contact placeholders to validate before launch:
  `+63 912 345 6789`, `info@buildpro.com`, `Manila, Philippines`.

## Website Color Palette

The website visual identity must be based on the existing RRJ logo at
`static/assets/rrj-logo.png`. The logo uses a high-energy violet-to-magenta
gradient, communicating modern service, cleanliness, and visible transformation.
The website should use the colors deliberately rather than flooding every
surface with saturated color.

### Brand Colors Derived From Logo

| Token | Color | Hex | Website Use |
| --- | --- | --- | --- |
| `brand-violet` | Electric Violet | `#6018F0` | Primary brand color, links, selected states, service icons, primary buttons. |
| `brand-pink` | Hot Magenta Pink | `#F00078` | Brand accent, badges, highlights, decorative shapes, gradient endpoint. |
| `brand-purple` | Transition Purple | `#9030C0` | Gradient bridge, illustrations, subtle decorative accents. |
| `brand-plum` | Deep Magenta | `#B0005A` | Accessible pink-based button/hover color with white text. |
| `brand-indigo` | Deep Violet | `#40138F` | Dark brand surfaces, footer accents, hover states, high-contrast headings on light surfaces. |

### Neutral and Interface Colors

The logo does not contain enough neutral interface colors for a readable booking
platform. Use these support colors for content-heavy screens and forms:

| Token | Hex | Website Use |
| --- | --- | --- |
| `text-primary` | `#111827` | Headings and body text. |
| `text-secondary` | `#4B5563` | Supporting descriptions, labels, metadata. |
| `surface` | `#FFFFFF` | Main page and card background. |
| `surface-soft` | `#FAF7FF` | Light violet-tinted section backgrounds. |
| `border` | `#E9DFF7` | Card and form borders. |
| `success` | `#15803D` | Successful bookings and completed-status messaging. |
| `warning` | `#B45309` | Pending quotation or action-needed status. |
| `error` | `#B91C1C` | Form validation and failed actions. |

### Color Usage Rules

- Use `brand-violet` as the primary interaction color for `Book a Service`,
  navigation emphasis, selected controls, and links.
- Use `brand-pink` primarily for visual accents and gradient endpoints. Its
  white-text contrast is below the preferred AA threshold for ordinary button
  text, so use `brand-plum` for solid pink buttons.
- Use the logo gradient only for prominent conversion surfaces such as the hero
  headline accent, CTA banner, icon treatments, or small decorative elements.
- Keep service cards, quotation forms, and tracking screens mostly white or
  `surface-soft`; users need fast readability and trust more than decoration.
- Use semantic status colors for project states. Do not use pink or violet alone
  to communicate success, delays, errors, or cancellations.
- Preserve generous white space around the logo. Do not place the full-color
  logo on busy gradients or dark backgrounds unless a tested alternate logo is
  provided.

### Recommended Component Mapping

| Component | Color Treatment |
| --- | --- |
| Header/navigation | White background, `text-primary` copy, `brand-violet` active link and CTA. |
| Hero section | White or `surface-soft` background with violet-to-pink accent gradient. |
| Primary button | `brand-violet` background with white text; `brand-indigo` hover state. |
| Secondary CTA | White background, `brand-violet` text and border; soft violet hover background. |
| Accent badge | Pale violet background with `brand-indigo` text. |
| Service card icon | Violet/pink gradient or `brand-violet` on a light tinted tile. |
| Quotation price highlight | `brand-indigo` or `brand-violet`; avoid using pink for long text. |
| Footer | `brand-indigo` background with white text and subtle pink accent. |

### CSS Design Tokens

Use these variables as the initial website theme:

```css
:root {
  --color-brand-violet: #6018F0;
  --color-brand-pink: #F00078;
  --color-brand-purple: #9030C0;
  --color-brand-plum: #B0005A;
  --color-brand-indigo: #40138F;

  --color-text-primary: #111827;
  --color-text-secondary: #4B5563;
  --color-surface: #FFFFFF;
  --color-surface-soft: #FAF7FF;
  --color-border: #E9DFF7;
  --color-success: #15803D;
  --color-warning: #B45309;
  --color-error: #B91C1C;

  --gradient-brand: linear-gradient(135deg, #6018F0 0%, #9030C0 50%, #F00078 100%);
  --shadow-brand-soft: 0 12px 32px rgba(96, 24, 240, 0.14);
}
```

### Accessibility Requirement

All production UI must meet WCAG AA color contrast for readable text and
controls. White text on `brand-violet`, `brand-indigo`, and `brand-plum` is
appropriate for normal-size buttons. Do not use white normal-size text directly
on `brand-pink`; reserve the bright pink for non-text accents, large display
treatments where verified, or use its darker `brand-plum` variant.

## Website Typography

The website will use two modern sans-serif typefaces:

| Font | CSS Family | Primary Use |
| --- | --- | --- |
| Plus Jakarta Sans | `"Plus Jakarta Sans", sans-serif` | Brand-facing typography: hero heading, section headings, navigation emphasis, CTA labels, and key figures. |
| Inter | `"Inter", sans-serif` | Functional/readability typography: body text, service descriptions, form labels, input content, quotation details, status timelines, and dashboard tables. |

### Typography Rules

- Use `Plus Jakarta Sans` for headings to establish a modern, premium brand
  identity that complements the violet-and-pink logo.
- Use `Inter` for content and booking workflows because forms, quotations, and
  project updates must be highly readable at smaller sizes.
- Keep heading weights between `600` and `700`; avoid excessively heavy text
  that competes with the colorful logo.
- Keep body text at a minimum of `16px` on public pages and use comfortable line
  height for service descriptions and quotation explanations.
- Load only the required font weights initially to reduce landing-page load time:
  `Plus Jakarta Sans` weights `600`, `700`; `Inter` weights `400`, `500`, `600`.

### CSS Typography Tokens

```css
:root {
  --font-display: "Plus Jakarta Sans", sans-serif;
  --font-body: "Inter", sans-serif;
}

body {
  font-family: var(--font-body);
  color: var(--color-text-primary);
}

h1,
h2,
h3,
.brand,
.button-label {
  font-family: var(--font-display);
}
```

## Core Features

### MVP Features

| Area | Capability |
| --- | --- |
| Marketing website | Responsive landing page, service cards, testimonials, and contact CTA. |
| Service catalog | Admin-managed services, descriptions, price ranges, and active/inactive status. |
| Booking request | Customer form for service, contact details, address, preferred visit date, budget, project details, and optional photos. |
| Reference tracking | Generate a booking reference number after submission. |
| Admin dashboard | View, filter, assign, and update booking requests. |
| Quotation management | Create quotation with line items, validity date, notes, and totals; record accepted or rejected status. |
| Scheduling | Record site visits and confirmed project schedule. |
| Status tracking | Customer views booking/project progress using a reference number and verified contact detail or secure link. |
| Notifications | Email acknowledgement on booking submission and status changes. |
| Basic reporting | Count of inquiries, pending quotations, accepted bookings, and completed jobs. |

### Not in Initial MVP

- Online payments and installment management.
- Inventory and materials procurement.
- Worker payroll and subcontractor portal.
- AI-generated quotations.
- Native mobile app.
- Full live chat.

These can be added only after the booking pipeline is used consistently and
actual operational pain points are measured.

## System Design

### Architecture

Use the existing Django application as a server-rendered monolith for the MVP:

| Layer | Initial Choice | Reason |
| --- | --- | --- |
| Backend | Django 4.2 | Already initialized; built-in auth, admin, forms, and security. |
| Frontend | Django templates + CSS/JavaScript | Fast delivery for marketing and booking workflow. |
| Database | SQLite in local development; PostgreSQL in production | Reliable production relational data and reporting. |
| Admin operations | Django Admin plus focused staff views where needed | Avoid building unnecessary back-office UI too early. |
| Static/media files | WhiteNoise for static assets; cloud object storage for customer uploads in production | Simple deployment with safe media storage. |
| Email | Transactional email provider through SMTP/API | Booking receipts and status updates must be dependable. |
| Deployment | Managed Python hosting with PostgreSQL and HTTPS | Low operational burden for the MVP. |

### Data Models

| Model | Important Fields | Purpose |
| --- | --- | --- |
| `Service` | `name`, `slug`, `description`, `min_price`, `max_price`, `icon`, `is_featured`, `is_active` | Public service offerings. |
| `Customer` | `full_name`, `email`, `phone` | Customer identity and repeat inquiry history. |
| `BookingRequest` | `reference_number`, `customer`, `service`, `property_type`, `address`, `details`, `budget`, `preferred_date`, `status`, `created_at` | Initial customer inquiry. |
| `BookingAttachment` | `booking_request`, `file`, `caption`, `uploaded_at` | Photos or reference files supplied by customer. |
| `SiteVisit` | `booking_request`, `scheduled_at`, `assigned_to`, `notes`, `status` | Inspection/measurement scheduling. |
| `Quotation` | `booking_request`, `version`, `subtotal`, `discount`, `total`, `valid_until`, `status`, `sent_at`, `accepted_at` | Formal price proposal and approval state. |
| `QuotationItem` | `quotation`, `description`, `quantity`, `unit`, `unit_price`, `line_total` | Transparent labor/material breakdown. |
| `Project` | `booking_request`, `quotation`, `start_date`, `end_date`, `status`, `progress_percent` | Confirmed paid/approved work execution record. |
| `ProjectUpdate` | `project`, `status`, `message`, `progress_percent`, `created_by`, `created_at` | Timeline displayed to customer and staff. |
| `ContactInquiry` | `name`, `email`, `phone`, `message`, `created_at` | General requests that are not service bookings. |

Recommended booking statuses:

`submitted`, `under_review`, `site_visit_scheduled`, `quoted`, `accepted`,
`declined`, `scheduled`, `in_progress`, `completed`, `cancelled`.

### User Flow

#### Customer Booking Flow

1. Customer lands on the website and reviews services and indicative pricing.
2. Customer chooses `Book Service` on a service card.
3. Booking form opens with the selected service prefilled.
4. Customer supplies contact and project information and uploads photos if available.
5. System creates a booking reference and sends confirmation.
6. Customer receives quotation or site-visit scheduling communication.
7. Customer approves the quotation through staff confirmation or a secure approval page.
8. Customer tracks scheduled and active project status online.

#### Staff Workflow

1. Admin receives a new inquiry notification.
2. Admin checks requirements and marks the request `under_review`.
3. Admin schedules an inspection or directly drafts a quotation.
4. Admin records the accepted quote and creates a scheduled project.
5. Assigned staff post progress updates until completion.
6. Owner reviews conversion and completion reporting.

### API / Integration Flow

The MVP can use Django form views for public submission and staff operations.
JSON endpoints should only be introduced where asynchronous UI or integrations
require them.

| Endpoint / Action | Method | Purpose |
| --- | --- | --- |
| `/` | `GET` | Landing page and featured services. |
| `/services/` | `GET` | Browse all active services. |
| `/services/<slug>/book/` | `GET`, `POST` | Create a booking request for a selected service. |
| `/booking/success/<reference>/` | `GET` | Confirmation and next steps. |
| `/track/` | `GET`, `POST` | Secure booking reference lookup. |
| `/track/<secure-token>/` | `GET` | Customer project status timeline. |
| `/admin/` | Django Admin | Initial business operations dashboard. |

Initial integrations:

- Email provider: acknowledgement, quotation notice, booking/status notifications.
- Cloud media storage: uploaded customer photos in production.
- Optional later: SMS notification provider once customer demand is proven.

### Deployment Notes

- Keep `.env` outside source control and provide a safe `.env.example`.
- Use PostgreSQL in production; SQLite is suitable only for local development.
- Configure `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, HTTPS redirects, and secure cookies.
- Store uploaded files outside the application server filesystem in production.
- Run database backups automatically and test recovery.
- Configure error monitoring and basic uptime monitoring before public launch.

### Security Considerations

- Customer tracking must not expose data using an easily guessed sequential ID.
  Use a secure random token and confirm contact details where appropriate.
- Validate and restrict upload file types and sizes; never trust customer uploads.
- Keep administrative functions behind authenticated staff accounts and use
  least-privilege permissions.
- Protect forms with CSRF handling, spam prevention, and rate limiting on public
  submission and tracking endpoints.
- Treat quotations, addresses, phone numbers, and uploaded property images as
  private customer data.
- Keep audit timestamps and user attribution on quotation and progress updates.

## Execution Steps

### Phase 1 - Marketing and Lead Capture

1. Finalize brand name, contact details, logo, service prices, and legal/trust claims.
2. Build responsive landing page matching the supplied content.
3. Create the `Service` model and load the eight featured services.
4. Implement booking request submission and admin notification.
5. Make service estimates clearly non-binding until quotation approval.

### Phase 2 - Operations and Conversion

1. Implement admin booking management with statuses.
2. Add site visit scheduling.
3. Add quotation and line-item creation.
4. Send quotation and acceptance notifications.
5. Track inquiry-to-accepted-booking conversion.

### Phase 3 - Project Tracking

1. Create project records from accepted bookings.
2. Implement secure customer tracking page and update timeline.
3. Add email alerts for meaningful status updates.
4. Add dashboard totals for active and completed projects.

### Phase 4 - Validated Enhancements

1. Add online deposits only when payment handling is operationally ready.
2. Add SMS if customers miss email updates.
3. Add review collection and approved testimonials after completed jobs.
4. Add service-area and revenue reporting from real booking data.

## Monetization

This is primarily a revenue-generation and operations platform for an actual
services business, not a standalone SaaS product in the MVP.

| Revenue Path | Description |
| --- | --- |
| Project contracts | Revenue from accepted renovation, installation, and maintenance quotations. |
| Consultation/design fees | Optional fee for detailed plans or consultations, deductible from an approved project if desired. |
| Maintenance packages | Recurring property maintenance contracts for residential or commercial customers. |
| Upsells | Premium materials, additional rooms, landscaping maintenance, and after-service care. |

Key metrics:

- Visitor-to-booking-request conversion rate.
- Response time from inquiry to first contact.
- Quotation acceptance rate.
- Average accepted project value.
- Lead source and service category revenue.
- Repeat customer rate.

## Scaling Plan

1. Start with one region and a manageable service catalog.
2. Standardize quotation templates and status workflows using real completed jobs.
3. Add staff roles, job assignment, and calendar visibility as bookings grow.
4. Move notifications and document generation to background tasks when volume
   justifies it.
5. Add payment/deposit collection, supplier coordination, and repeat-maintenance
   plans after operational processes are stable.
6. Consider a multi-company SaaS version only after the internal workflow is
   proven and other service firms show willingness to pay.

## Brutal Feedback

- A polished landing page does not create a booking business by itself. Fast
  response, accurate quotations, and reliable execution determine conversion
  and referrals.
- `Trusted by 500+ clients`, `Licensed & Insured`, testimonials, and guarantee
  statements must be factual before public release. Unsupported claims create
  credibility and legal risk.
- Construction work cannot realistically be given an "instant quotation" for
  many categories without detailed scope or inspection. Use instant estimates
  and fast formal quotations instead.
- Real-time tracking only matters if staff consistently update project status.
  The workflow must be simple enough that operations actually use it.
- Building payment, inventory, workforce, or AI features before proving the
  inquiry-to-booking process would slow launch without improving early revenue.

## MVP Success Definition

The first release is successful when a customer can discover a service, submit
a qualified booking request, receive a quotation, confirm a scheduled job, and
track project progress while staff can manage the entire workflow through the
system without relying on scattered messages or spreadsheets.
