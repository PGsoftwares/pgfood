from typing import Any, Dict


class DashboardService:
    """Service providing dashboard metrics, charts, tables, and recent activity feeds.
    
    Designed to easily plug into real business models in future phases.
    """

    @classmethod
    def get_summary_statistics(cls) -> Dict[str, Any]:
        """Provides key performance indicator metrics for the top cards."""
        return {
            "total_orders": {
                "value": "1,428",
                "change": "+12.5%",
                "trend": "up",
                "subtitle": "vs. previous 30 days",
            },
            "total_revenue": {
                "value": "₹3,84,520",
                "change": "+8.2%",
                "trend": "up",
                "subtitle": "vs. previous 30 days",
            },
            "total_restaurants": {
                "value": "86",
                "change": "+4 new",
                "trend": "up",
                "subtitle": "78 currently active",
            },
            "total_delivery_partners": {
                "value": "142",
                "change": "+18 online",
                "trend": "up",
                "subtitle": "115 active on duty",
            },
        }

    @classmethod
    def get_sales_overview_data(cls) -> Dict[str, Any]:
        """Provides datasets for Daily, Weekly, and Monthly sales overview charts."""
        return {
            "daily": {
                "categories": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                "revenue": [28400, 34200, 31800, 42100, 56300, 68900, 72500],
                "orders": [112, 134, 126, 168, 224, 276, 288],
            },
            "weekly": {
                "categories": ["Week 1", "Week 2", "Week 3", "Week 4"],
                "revenue": [184500, 212400, 198600, 245200],
                "orders": [740, 850, 790, 980],
            },
            "monthly": {
                "categories": ["Jun", "Jul", "Aug", "Sep", "Oct", "Nov"],
                "revenue": [620000, 710000, 680000, 830000, 920000, 1050000],
                "orders": [2480, 2840, 2720, 3320, 3680, 4200],
            },
        }

    @classmethod
    def get_order_statistics(cls) -> Dict[str, Any]:
        """Distribution of orders by status for donut chart."""
        return {
            "labels": ["Delivered", "In Transit", "Preparing", "Cancelled"],
            "series": [68, 14, 12, 6],
            "colors": ["#2fb344", "#206bc4", "#f59f00", "#d63939"],
        }

    @classmethod
    def get_recent_orders(cls) -> list:
        """Recent order records formatted for Tabler data table."""
        return [
            {
                "order_id": "#PGF-9042",
                "customer": {"name": "Arjun Sharma", "avatar": "static/tabler/static/avatars/001m.jpg"},
                "restaurant": "Royal Biryani House",
                "items": "2x Hyderabadi Dum Biryani, 1x Raita",
                "amount": "₹640",
                "status": "In Transit",
                "status_badge": "bg-primary-lt",
                "status_dot": "bg-primary",
                "time": "12 mins ago",
            },
            {
                "order_id": "#PGF-9041",
                "customer": {"name": "Priya Nair", "avatar": "static/tabler/static/avatars/002f.jpg"},
                "restaurant": "Kovai Woodlands",
                "items": "3x Masala Dosa, 2x Filter Coffee",
                "amount": "₹320",
                "status": "Preparing",
                "status_badge": "bg-warning-lt",
                "status_dot": "bg-warning",
                "time": "24 mins ago",
            },
            {
                "order_id": "#PGF-9040",
                "customer": {"name": "Vikram Patel", "avatar": "static/tabler/static/avatars/003m.jpg"},
                "restaurant": "Spice Route Tandoor",
                "items": "1x Butter Chicken, 4x Garlic Naan",
                "amount": "₹780",
                "status": "Delivered",
                "status_badge": "bg-success-lt",
                "status_dot": "bg-success",
                "time": "45 mins ago",
            },
            {
                "order_id": "#PGF-9039",
                "customer": {"name": "Ananya Sen", "avatar": "static/tabler/static/avatars/000f.jpg"},
                "restaurant": "The Gourmet Crust",
                "items": "1x Farmhouse Pizza (Large), 1x Garlic Bread",
                "amount": "₹590",
                "status": "Delivered",
                "status_badge": "bg-success-lt",
                "status_dot": "bg-success",
                "time": "1 hour ago",
            },
            {
                "order_id": "#PGF-9038",
                "customer": {"name": "Rohan Deshmukh", "avatar": "static/tabler/static/avatars/006m.jpg"},
                "restaurant": "Dragon Wok Kitchen",
                "items": "1x Schezwan Fried Rice, 1x Veg Manchurian",
                "amount": "₹450",
                "status": "Cancelled",
                "status_badge": "bg-danger-lt",
                "status_dot": "bg-danger",
                "time": "2 hours ago",
            },
        ]

    @classmethod
    def get_recent_activities(cls) -> list:
        """Recent platform activities for timeline feed."""
        return [
            {
                "title": "New Restaurant Onboarded",
                "description": "'Flavors of Chettinad' completed merchant verification.",
                "time": "18 minutes ago",
                "badge_color": "bg-success",
                "icon": "building-store",
            },
            {
                "title": "Delivery Partner Approved",
                "description": "Karthik R. was onboarded with verified DL and Aadhaar.",
                "time": "42 minutes ago",
                "badge_color": "bg-blue",
                "icon": "motorbike",
            },
            {
                "title": "High Order Volume Alert",
                "description": "Zone 'Velachery Central' reached 80 concurrent orders.",
                "time": "1 hour ago",
                "badge_color": "bg-yellow",
                "icon": "flame",
            },
            {
                "title": "Payout Settlement Processed",
                "description": "Weekly automated payout of ₹1,42,800 initiated to 24 restaurants.",
                "time": "3 hours ago",
                "badge_color": "bg-purple",
                "icon": "credit-card",
            },
        ]
