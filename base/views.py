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
    },
    {
        "reference": "BK-MPKPRA6C",
        "service": "Sculpture Maker",
        "status": "Pending Quotation",
        "date": "May 25, 2026",
        "description": "fasdfsdf",
    },
]


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
            "bookings": BOOKINGS,
            "booking_stats": [
                {"label": "Total", "value": "2", "kind": "total"},
                {"label": "Pending", "value": "2", "kind": "pending"},
                {"label": "Active", "value": "0", "kind": "active"},
                {"label": "Completed", "value": "0", "kind": "completed"},
            ],
        },
    )
