export default function PropertyCard({ property }) {
  return (
    <div className="border rounded-lg overflow-hidden shadow-sm">
      <img 
        src={property.image || '/images/property-placeholder.jpg'} 
        alt={property.address}
        className="w-full h-48 object-cover"
      />
      <div className="p-4">
        <h3 className="font-semibold text-lg">{property.address}</h3>
        <div className="flex justify-between mt-2">
          <span>${property.price.toLocaleString()}</span>
          <span>{property.bedrooms} beds</span>
        </div>
      </div>
    </div>
  );
}