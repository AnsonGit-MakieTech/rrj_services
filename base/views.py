from django.http import Http404
from django.shortcuts import render


SERVICES = [
    {
        "name": "Condo Renovation",
        "description": "Complete condo renovation and remodeling services including layout changes, finishes, and fixtures.",
        "price": "PHP 50,000 - PHP 500,000",
        "image_url": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=640&q=80",
    },
    {
        "name": "House Renovation",
        "description": "Full house renovation from structural work to interior finishing and exterior improvements.",
        "price": "PHP 100,000 - PHP 1,000,000",
        "image_url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=640&q=80",
    },
    {
        "name": "Cabinet Maker/Design",
        "description": "Custom cabinet design and installation for kitchens, bedrooms, and storage areas.",
        "price": "PHP 15,000 - PHP 120,000",
        "image_url": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?auto=format&fit=crop&w=640&q=80",
    },
    {
        "name": "Wall Partition Maker",
        "description": "Drywall and partition installation for room division and office spaces.",
        "price": "PHP 8,000 - PHP 60,000",
        "image_url": "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?auto=format&fit=crop&w=640&q=80",
    },
    {
        "name": "Landscaping Design",
        "description": "Professional landscape design and garden installation for residential and commercial properties.",
        "price": "PHP 20,000 - PHP 200,000",
        "image_url": "https://images.unsplash.com/photo-1558904541-efa843a96f01?auto=format&fit=crop&w=640&q=80",
    },
    {
        "name": "Repainting",
        "description": "Interior and exterior painting services with premium quality paints and finishes.",
        "price": "PHP 5,000 - PHP 80,000",
        "image_url": "https://images.unsplash.com/photo-1562259949-e8e7689d7828?auto=format&fit=crop&w=640&q=80",
    },
    {
        "name": "Shower Enclosure Install",
        "description": "Custom glass shower enclosure design and installation for modern bathrooms.",
        "price": "PHP 12,000 - PHP 50,000",
        "image_url": "https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?auto=format&fit=crop&w=640&q=80",
    },
    {
        "name": "Glass Door Install",
        "description": "Tempered glass door installation for offices, shops, and residential spaces.",
        "price": "PHP 10,000 - PHP 45,000",
        "image_url": "https://images.unsplash.com/photo-1600566752355-35792bedcfea?auto=format&fit=crop&w=640&q=80",
    },
    {
        "name": "Ceiling Cove Lights Designs",
        "description": "Decorative ceiling cove lighting design and installation for ambient interiors.",
        "price": "PHP 10,000 - PHP 50,000",
        "image_url": "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=640&q=80",
    },
    {
        "name": "Sculpture Maker",
        "description": "Custom decorative sculptures and art pieces for interior and exterior spaces.",
        "price": "PHP 15,000 - PHP 100,000",
        "image_url": "https://images.unsplash.com/photo-1564399579883-451a5d44ec08?auto=format&fit=crop&w=640&q=80",
    },
    {
        "name": "Roofing Renovation",
        "description": "Complete roofing repair, replacement, and waterproofing services.",
        "price": "PHP 20,000 - PHP 150,000",
        "image_url": "https://images.unsplash.com/photo-1632759145351-1d592919f522?auto=format&fit=crop&w=640&q=80",
    },
    {
        "name": "Electrical Services",
        "description": "Licensed electrical work including wiring, panel upgrades, and fixtures.",
        "price": "PHP 3,000 - PHP 50,000",
        "image_url": "https://images.unsplash.com/photo-1621905252507-b35492cc74b4?auto=format&fit=crop&w=640&q=80",
    },
    {
        "name": "Plumbing Services",
        "description": "Complete plumbing solutions from leak repair to full system installation.",
        "price": "PHP 2,000 - PHP 40,000",
        "image_url": "https://images.unsplash.com/photo-1607472586893-edb57bdc0e39?auto=format&fit=crop&w=640&q=80",
    },
    {
        "name": "Waterproofing",
        "description": "Professional waterproofing for roofs, walls, basements, and bathrooms.",
        "price": "PHP 8,000 - PHP 60,000",
        "image_url": "https://images.unsplash.com/photo-1628624747186-a941c476b7ef?auto=format&fit=crop&w=640&q=80",
    },
    {
        "name": "Aircon Installation",
        "description": "Split-type and window AC installation, cleaning, and maintenance services.",
        "price": "PHP 5,000 - PHP 25,000",
        "image_url": "https://images.unsplash.com/photo-1621905252507-b35492cc74b4?auto=format&fit=crop&w=640&q=80",
    },
    {
        "name": "Carpentry",
        "description": "Custom woodworking, furniture repair, and structural carpentry services.",
        "price": "PHP 5,000 - PHP 80,000",
        "image_url": "https://images.unsplash.com/photo-1601058268499-e52658b8bb88?auto=format&fit=crop&w=640&q=80",
    },
]

BOOKINGS = [
    {
        "reference": "BK-MPL5LPV3",
        "service": "Carpentry",
        "status": "Pending Quotation",
        "date": "May 25, 2026",
        "description": "",
        "email": "techmakie@gmail.com",
        "phone": "-",
        "location": "-",
        "sqm": "-",
        "urgency": "High",
        "schedule": "-",
        "attachment_url": "https://images.unsplash.com/photo-1601058268499-e52658b8bb88?auto=format&fit=crop&w=180&q=80",
        "quotation": {
            "materials": "PHP 100",
            "labor": "PHP 400",
            "total": "PHP 500",
            "notes": "Quotation prepared after project assessment.",
        },
    },
    {
        "reference": "BK-MPKPRA6C",
        "service": "Sculpture Maker",
        "status": "Pending Quotation",
        "date": "May 25, 2026",
        "description": "fasdfsdf",
        "email": "techmakie@gmail.com",
        "phone": "09512213004",
        "location": "Manila",
        "sqm": "21",
        "urgency": "Medium",
        "schedule": "-",
        "attachment_url": "",
        "quotation": {
            "materials": "PHP 2,500",
            "labor": "PHP 6,500",
            "total": "PHP 9,000",
            "notes": "Final schedule follows confirmed payment.",
        },
    },
]

# Change this value and refresh a booking detail page to preview a workflow state.
# Available values: pending_quotation, quotation_sent, waiting_for_payment,
# payment_verification, booking_confirmed, scheduled, in_progress, completed,
# cancelled.
SIMULATED_VIEW_BOOKING_STATUS = "waiting_for_payment"

PROGRESS_STEPS = [
    "Pending Quotation",
    "Quotation Sent",
    "Waiting for Payment",
    "Payment Verification",
    "Booking Confirmed",
    "Scheduled",
    "In Progress",
    "Completed",
]

BOOKING_VIEW_STATES = {
    "pending_quotation": {
        "label": "Pending Quotation",
        "variant": "pending",
        "step": 0,
        "show_quotation": False,
        "allow_decision": False,
        "show_payment": False,
    },
    "quotation_sent": {
        "label": "Quotation Sent",
        "variant": "sent",
        "step": 1,
        "show_quotation": True,
        "allow_decision": True,
        "show_payment": False,
    },
    "waiting_for_payment": {
        "label": "Waiting for Payment",
        "variant": "payment",
        "step": 2,
        "show_quotation": True,
        "allow_decision": False,
        "show_payment": True,
    },
    "payment_verification": {
        "label": "Payment Verification",
        "variant": "active",
        "step": 3,
        "show_quotation": True,
        "allow_decision": False,
        "show_payment": False,
    },
    "booking_confirmed": {
        "label": "Booking Confirmed",
        "variant": "active",
        "step": 4,
        "show_quotation": True,
        "allow_decision": False,
        "show_payment": False,
    },
    "scheduled": {
        "label": "Scheduled",
        "variant": "active",
        "step": 5,
        "show_quotation": True,
        "allow_decision": False,
        "show_payment": False,
    },
    "in_progress": {
        "label": "In Progress",
        "variant": "active",
        "step": 6,
        "show_quotation": True,
        "allow_decision": False,
        "show_payment": False,
    },
    "completed": {
        "label": "Completed",
        "variant": "completed",
        "step": 7,
        "show_quotation": True,
        "allow_decision": False,
        "show_payment": False,
    },
    "cancelled": {
        "label": "Cancelled",
        "variant": "cancelled",
        "step": None,
        "show_quotation": True,
        "allow_decision": False,
        "show_payment": False,
    },
}


def _simulated_state():
    return BOOKING_VIEW_STATES.get(
        SIMULATED_VIEW_BOOKING_STATUS,
        BOOKING_VIEW_STATES["pending_quotation"],
    )


def _progress_steps(state):
    if state["variant"] == "cancelled":
        return [{"label": "Cancelled", "phase": "cancelled"}]

    steps = []
    for index, label in enumerate(PROGRESS_STEPS):
        if index < state["step"]:
            phase = "complete"
        elif index == state["step"]:
            phase = "current"
        else:
            phase = "upcoming"
        steps.append({"label": label, "phase": phase})
    return steps


def _bookings_for_dashboard():
    bookings = [booking.copy() for booking in BOOKINGS]
    if bookings:
        bookings[0]["status"] = _simulated_state()["label"]
    return bookings


def _display_name(request):
    if request.user.is_authenticated:
        return request.user.get_full_name() or request.user.username
    return "Makie Tech"


def home(request):
    return render(
        request,
        "base/home.html",
        {
            "active_page": "home",
            "display_name": _display_name(request),
            "services": SERVICES[:8],
        },
    )


def login_page(request):
    return render(request, "base/login.html")


def register_page(request):
    return render(request, "base/register.html")


def services(request):
    return render(
        request,
        "base/services.html",
        {
            "active_page": "services",
            "display_name": _display_name(request),
            "services": SERVICES,
        },
    )


def my_bookings(request):
    return render(
        request,
        "base/my_bookings.html",
        {
            "active_page": "bookings",
            "display_name": _display_name(request),
            "bookings": _bookings_for_dashboard(),
            "booking_stats": [
                {"label": "Total", "value": "2", "kind": "total"},
                {"label": "Pending", "value": "2", "kind": "pending"},
                {"label": "Active", "value": "0", "kind": "active"},
                {"label": "Completed", "value": "0", "kind": "completed"},
            ],
        },
    )


def add_booking(request):
    selected_service = request.GET.get("service", "")
    service_names = {service["name"] for service in SERVICES}
    if selected_service not in service_names:
        selected_service = ""

    return render(
        request,
        "base/add_booking.html",
        {
            "active_page": "",
            "display_name": _display_name(request),
            "services": SERVICES,
            "selected_service": selected_service,
        },
    )


def view_booking(request, reference):
    booking = next((booking.copy() for booking in BOOKINGS if booking["reference"] == reference), None)
    if booking is None:
        raise Http404("Booking not found")

    state = _simulated_state()
    booking["status"] = state["label"]

    return render(
        request,
        "base/view_booking.html",
        {
            "active_page": "bookings",
            "display_name": _display_name(request),
            "booking": booking,
            "state": state,
            "progress_steps": _progress_steps(state),
        },
    )
