async def search_properties(
    self,
    min_price: float = None,
    max_price: float = None,
    bedrooms: int = None,
    location: str = None
):
    query = self.session.query(Property)
    
    if min_price:
        query = query.filter(Property.price >= min_price)
    if max_price:
        query = query.filter(Property.price <= max_price)
    if bedrooms:
        query = query.filter(Property.bedrooms == bedrooms)
    if location:
        query = query.filter(Property.address.ilike(f"%{location}%"))
    
    return query.all()