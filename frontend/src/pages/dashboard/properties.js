import useSWR from 'swr';
import PropertyCard from '../../components/property/PropertyCard';

export default function PropertiesPage() {
  const { data: properties, error } = useSWR('/api/properties');
  
  if (error) return <div>Failed to load</div>;
  if (!properties) return <div>Loading...</div>;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {properties.map(property => (
        <PropertyCard key={property.id} property={property} />
      ))}
    </div>
  );
}