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
]


def home(request):
    if request.user.is_authenticated:
        display_name = request.user.get_full_name() or request.user.username
    else:
        display_name = "Makie Tech"

    return render(
        request,
        "base/home.html",
        {
            "display_name": display_name,
            "services": SERVICES,
        },
    )
